import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from pydantic import BaseModel, Field
from typing import List
import PyPDF2
import requests

# ==========================================
# 1. DATA MODELS (PYDANTIC)
# ==========================================
class RiskItem(BaseModel):
    clause_text: str = Field(description="Exact text of the suspicious clause found in the document")
    risk_level: str = Field(description="Strictly output: HIGH or MEDIUM")
    category: str = Field(description="Financial, Career, Privacy, Legal, or Freedom")
    baseline: str = Field(description="What is the standard, fair industry practice for this? (The Baseline)")
    deviation: str = Field(description="Why does this specific clause deviate from the baseline? Why is it one-sided?")
    suggestion: str = Field(description="Actionable advice on what to negotiate")

class SafeItem(BaseModel):
    clause_summary: str = Field(description="Short summary of the standard clause found (e.g., '30-Day Notice Period')")
    reason: str = Field(description="Why this is considered standard and safe")

class ContractAnalysis(BaseModel):
    risks: List[RiskItem]
    safe_clauses: List[SafeItem] = Field(description="List of clauses checked that are standard/fair and NOT red flags.")

# ==========================================
# 2. MULTI-LLM FAILOVER ENGINE
# ==========================================
@st.cache_resource
def get_gemini_llm():
    my_api_key = st.secrets["GEMINI_API_KEY"]
    return ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0, google_api_key=my_api_key)

@st.cache_resource
def get_groq_llm():
    my_groq_key = st.secrets["GROQ_API_KEY"]
    return ChatGroq(model="llama3-70b-8192", temperature=0, groq_api_key=my_groq_key)

def analyze_contract(text: str, rules_text: str, language: str) -> ContractAnalysis:
    prompt = PromptTemplate(
        template="""You are RedFlag.ai, an enterprise-grade contract risk analyzer. 
        RULEBOOK: {rules_text}
        
        TASK:
        1. Identify RED FLAGS (deviations from baselines). Extract exact quoted text. Explain the standard baseline and how this clause deviates.
        2. Identify GREEN FLAGS (standard, fair clauses). List them to prove you are analyzing the document without 'alert fatigue'. Do not flag standard clauses as risks.
        
        LANGUAGE: Write the 'baseline', 'deviation', 'suggestion', 'clause_summary', and 'reason' strictly in {language}. (clause_text must remain in original language).
        Contract: {contract_text}""",
        input_variables=["rules_text", "contract_text", "language"]
    )
    
    try:
        # First Attempt: Gemini
        llm = get_gemini_llm()
        structured_llm = llm.with_structured_output(ContractAnalysis)
        return (prompt | structured_llm).invoke({"rules_text": rules_text, "contract_text": text, "language": language})
    except Exception:
        # Second Attempt: Groq Llama-3
        st.toast("⚠️ Gemini network busy. Switching to high-speed Llama-3 backup engine...", icon="⚡")
        try:
            fallback_llm = get_groq_llm()
            structured_fallback = fallback_llm.with_structured_output(ContractAnalysis)
            return (prompt | structured_fallback).invoke({"rules_text": rules_text, "contract_text": text, "language": language})
        except Exception:
            # 🚨 GRACEFUL FAIL: Agar dono crash ho jayein toh clean error raise karo
            raise RuntimeError("Both primary and backup engines are currently unavailable due to high traffic.")

def generate_email(risks, doc_type):
    risk_descriptions = "\n".join([f"- Clause: '{r.clause_text}'\n  Request: {r.suggestion}" for r in risks])
    prompt = f"""You are an elite negotiator. Write a highly professional, polite email regarding a {doc_type} to negotiate these red flags:\n{risk_descriptions}\nKeep it concise and corporate. Start with "Dear [Name],". No subject line."""
    
    try:
        llm = get_gemini_llm()
        return llm.invoke(prompt).content
    except Exception:
        try:
            fallback_llm = get_groq_llm()
            return fallback_llm.invoke(prompt).content
        except Exception:
            # 🚨 GRACEFUL FAIL FOR EMAIL
            raise RuntimeError("Email generation service is busy.")

# ==========================================
# 3. HELPER FUNCTIONS 
# ==========================================
def extract_text_from_pdf(uploaded_file):
    try:
        reader = PyPDF2.PdfReader(uploaded_file)
        text = ""
        for page in reader.pages:
            extracted = page.extract_text()
            if extracted: text += extracted + "\n"
        return text
    except Exception:
        # 🚨 GRACEFUL FAIL FOR PDF
        raise ValueError("Could not read this PDF format.")

def calculate_score(risks):
    return min(sum(30 if r.risk_level.upper() == "HIGH" else 15 for r in risks), 100)

def generate_report_text(analysis, score, verdict):
    report = f"🚩 REDFLAG.AI AUDIT REPORT 🚩\n\nToxicity Score: {score}%\nVerdict: {verdict}\n" + "-"*40 + "\n\n"
    if analysis.risks:
        report += "⚠️ IDENTIFIED RISKS & DEVIATIONS:\n\n"
        for r in analysis.risks:
            report += f"[{r.risk_level.upper()} RISK] | Category: {r.category}\nFound Clause: \"{r.clause_text}\"\nBaseline: {r.baseline}\nDeviation: {r.deviation}\nSuggestion: {r.suggestion}\n" + "-"*40 + "\n\n"
    if analysis.safe_clauses:
        report += "✅ CLAUSES CHECKED & PASSED (STANDARD):\n\n"
        for s in analysis.safe_clauses:
            report += f"- {s.clause_summary}: {s.reason}\n"
        report += "-"*40 + "\n\n"
    return report + "Generated by RedFlag.ai (Not Legal Advice)"

def send_feedback(feedback_text):
    # Seedha crash hone do agar koi error hai, taaki humein error dikhe!
    webhook_url = st.secrets["DISCORD_WEBHOOK_URL"]
    
    payload = {
        "username": "TrueClause User", 
        "content": f"🛡️ **New Feedback from TrueClause:**\n\n> {feedback_text}"
    }
    
    response = requests.post(webhook_url, json=payload, timeout=5)
    
    if response.status_code not in [200, 204]:
        raise Exception(f"Discord rejected with Status {response.status_code}: {response.text}")
        
    return response
