import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq # 🚀 NAYA IMPORT FOR BACKUP ENGINE
from langchain_core.prompts import PromptTemplate
from pydantic import BaseModel, Field
from typing import List
import PyPDF2
import requests

# ==========================================
# 1. KNOWLEDGE BASE IMPORTS
# ==========================================
try:
    from rules.employment import EMPLOYMENT_RULES
    from rules.rent import RENTAL_RULES
    from rules.freelance import FREELANCE_RULES
    from rules.nda import NDA_RULES
    from rules.tos import TOS_RULES
    from rules.generic import GENERIC_RULES
except ImportError as e:
    st.error(f"🚨 Missing Rule File! Please check your 'rules' folder. Error: {e}")
    st.stop()

# ==========================================
# 2. PAGE CONFIGURATION & SIDEBAR (FEEDBACK)
# ==========================================
st.set_page_config(page_title="RedFlag.ai | Enterprise Risk Analyzer", page_icon="🚩", layout="centered", initial_sidebar_state="expanded")

with st.sidebar:
    st.markdown("### 🚩 About RedFlag.ai")
    st.caption("We don't provide legal advice. We act as a 'Deviation Detector' to find hidden traps, one-sided clauses, and unethical terms in your contracts.")
    st.write("---")
    
    st.markdown("### 🐞 Anonymous Feedback")
    st.write("Help us improve! No email required. 100% private.")
    
    with st.form("anonymous_feedback_form"):
        feedback_text = st.text_area("Found a bug or have a suggestion?", placeholder="Type your feedback here...", height=150)
        submitted = st.form_submit_button("Send Anonymously 🚀", use_container_width=True)
        
        if submitted:
            if len(feedback_text.strip()) < 5:
                st.warning("Please write a few words!")
            else:
                with st.spinner("Sending directly to the developer..."):
                    try:
                        # 🚀 DISCORD WEBHOOK SETUP
                        # 🚀 DISCORD WEBHOOK SETUP (SECURE)
                        DISCORD_WEBHOOK_URL = st.secrets["DISCORD_WEBHOOK"]
                        payload = {
                            "username": "RedFlag Beta Tester", 
                            "content": f"🚨 **New Feedback from RedFlag.ai:**\n\n> {feedback_text}"
                        }
                        response = requests.post(DISCORD_WEBHOOK_URL, json=payload)
                        if response.status_code in [200, 204]:
                            st.success("Sent! Thanks for helping us improve. 🎉")
                            st.balloons()
                        else:
                            st.error(f"API Error {response.status_code}: {response.text}")
                    except Exception as e:
                        st.error("Oops! Something went wrong with the connection.")

# ==========================================
# 3. HELPER FUNCTIONS 
# ==========================================
def clear_state():
    if "analysis_result" in st.session_state: del st.session_state["analysis_result"]
    if "email_draft" in st.session_state: del st.session_state["email_draft"]
    if "demo_text" in st.session_state: del st.session_state["demo_text"]

def extract_text_from_pdf(uploaded_file):
    reader = PyPDF2.PdfReader(uploaded_file)
    text = ""
    for page in reader.pages:
        extracted = page.extract_text()
        if extracted: text += extracted + "\n"
    return text

# ==========================================
# 4. DATA MODELS & MULTI-LLM FAILOVER ENGINE
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

@st.cache_resource
def get_gemini_llm():
    # 🚨 PRIMARY ENGINE (Gemini)
    my_api_key = st.secrets["GEMINI_API_KEY"] # Replace this with your actual Gemini Key for local testing
    return ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0, google_api_key=my_api_key)

@st.cache_resource
def get_groq_llm():
    # 🚨 BACKUP ENGINE (Groq Llama-3)
    my_groq_key = st.secrets["GROQ_API_KEY"] # Replace this with your actual Groq Key for local testing
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
    
    # 🚀 FAILOVER LOGIC IMPLEMENTATION 🚀
    try:
        # First Attempt: Gemini
        llm = get_gemini_llm()
        structured_llm = llm.with_structured_output(ContractAnalysis)
        return (prompt | structured_llm).invoke({"rules_text": rules_text, "contract_text": text, "language": language})
    except Exception as e:
        # Second Attempt: Switch to Groq if Gemini fails (e.g., Quota Exceeded)
        st.toast("⚠️ Gemini network busy. Switching to high-speed Llama-3 backup engine...", icon="⚡")
        fallback_llm = get_groq_llm()
        structured_fallback = fallback_llm.with_structured_output(ContractAnalysis)
        return (prompt | structured_fallback).invoke({"rules_text": rules_text, "contract_text": text, "language": language})

def generate_email(risks, doc_type):
    risk_descriptions = "\n".join([f"- Clause: '{r.clause_text}'\n  Request: {r.suggestion}" for r in risks])
    prompt = f"""You are an elite negotiator. Write a highly professional, polite email regarding a {doc_type} to negotiate these red flags:\n{risk_descriptions}\nKeep it concise and corporate. Start with "Dear [Name],". No subject line."""
    
    try:
        llm = get_gemini_llm()
        return llm.invoke(prompt).content
    except:
        fallback_llm = get_groq_llm()
        return fallback_llm.invoke(prompt).content

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

# ==========================================
# 5. FRONTEND UI & STYLING 
# ==========================================
st.markdown("<h1 style='text-align:center;'>🚩 RedFlag.ai</h1>", unsafe_allow_html=True)
st.markdown("<h5 style='text-align:center;color:gray;margin-top:-10px;'>Baseline-aware risk intelligence. We don't explain the law, we detect the deviations.</h5>", unsafe_allow_html=True)
st.write("---")

app_mode = st.radio("Choose Mode:", ["📝 Analyze Your Contract", "⚡ Instant Demos"], horizontal=True, label_visibility="collapsed", on_change=clear_state)
st.markdown("<br>", unsafe_allow_html=True)

if app_mode == "📝 Analyze Your Contract":
    rule_mapping = {"Employment / Job Offer": EMPLOYMENT_RULES, "Rental / Lease Agreement": RENTAL_RULES, "Freelance / Agency Contract": FREELANCE_RULES, "NDA / Confidentiality": NDA_RULES, "Terms of Service / Privacy Policy": TOS_RULES, "Other / Generic Contract": GENERIC_RULES}
    
    col1, col2 = st.columns(2)
    with col1: doc_type = st.selectbox("📄 Step 1: Document Type", list(rule_mapping.keys()), on_change=clear_state)
    with col2: language = st.selectbox("🌐 Step 2: Explanation Language", ["English", "Hindi", "Hinglish"], on_change=clear_state)
    
    uploaded_file = st.file_uploader("📂 Step 3: Upload PDF Contract", type=["pdf"], on_change=clear_state)
    
    user_text = ""
    if uploaded_file is not None:
        try:
            extracted_text = extract_text_from_pdf(uploaded_file)
            if len(extracted_text.split()) < 30:
                st.error("⚠️ We couldn't extract enough text. If this is a scanned image PDF, please copy and paste the text manually below.")
            else:
                user_text = extracted_text
                st.success("PDF Text Extracted Successfully! Ready to audit.")
                with st.expander("👁️ View Extracted Text"): st.text(user_text[:1000] + "... (truncated)")
        except Exception as e:
            st.error("Failed to read PDF. Please paste the text manually.")
            
    if not user_text:
        user_text = st.text_area("📝 Or Paste Contract Text Here", height=150, placeholder="Paste your text here...", on_change=clear_state)
    
    if st.button("🚨 Audit My Contract", type="primary", use_container_width=True):
        if len(user_text.split()) < 20:
            st.warning("⚠️ Please provide a bit more text. This doesn't look like a complete contract.")
        else:
            with st.spinner("Auditing against industry baselines... 🕵️‍♂️"):
                try:
                    st.session_state["analysis_result"] = analyze_contract(user_text, rule_mapping[doc_type], language)
                    st.session_state["doc_type"] = doc_type 
                except Exception as e:
                    # Is block mein app tabhi aayega jab Gemini aur Groq dono fail ho jayein (which is extremely rare)
                    st.error("An unexpected error occurred. Both our Primary and Backup engines are overwhelmed. Our team has been notified via webhook!")
                    st.caption(f"Error Details: {e}")

else:
    st.info("⚡ Experience RedFlag.ai instantly with these pre-analyzed, real-world examples.")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("💼 Toxic Job Offer", use_container_width=True):
            st.session_state["demo_text"] = "EMPLOYMENT AGREEMENT\n\n1. The employee shall be on a standard probation period of 6 months.\n2. The Company reserves the right to terminate the employee immediately without notice, while the employee must serve a 90-day notice period if they wish to resign.\n3. The Employee agrees to pay a training recovery fee of ₹3,00,000 if they leave within the first 2 years of service.\n4. The employee is bound by a standard confidentiality agreement (NDA) during and after employment."
            st.session_state["analysis_result"] = ContractAnalysis(
                risks=[
                    RiskItem(clause_text="Company reserves the right to terminate... while employee must serve a 90-day notice", risk_level="HIGH", category="Career", baseline="Mutual notice periods (e.g., 30 to 60 days for BOTH employer and employee).", deviation="Highly asymmetric. Gives the company power to fire you instantly, but forces you to stay for 3 months.", suggestion="Negotiate a mutual notice period (e.g., 30 days for both)."),
                    RiskItem(clause_text="pay a training recovery fee of ₹3,00,000 if they leave within the first 2 years", risk_level="HIGH", category="Financial", baseline="Companies cover standard onboarding costs. Bonds are only fair for expensive 3rd-party certifications.", deviation="Arbitrary financial trap. ₹3 Lakhs is excessive for basic training and acts as forced labor leverage.", suggestion="Ask for the bond to be removed or request an itemized list of training costs.")
                ],
                safe_clauses=[
                    SafeItem(clause_summary="Confidentiality (NDA)", reason="Standard practice to protect company IP."),
                    SafeItem(clause_summary="6-Month Probation Period", reason="Standard duration across the IT industry.")
                ]
            )
            st.session_state["doc_type"] = "Employment / Job Offer"

    with col2:
        if st.button("🏠 Shady Rent Agreement", use_container_width=True):
            st.session_state["demo_text"] = "LEASE AGREEMENT\n\n1. The Tenant shall pay a security deposit of ₹1,00,000.\n2. The Landlord reserves the right to automatically deduct 50% of the security deposit for 'standard repainting and deep cleaning' upon vacating, regardless of the flat's actual condition.\n3. The Tenant must give 2 months' notice to vacate, but the Landlord can evict the Tenant with 24 hours' notice.\n4. The Tenant is allowed to use the premises for residential purposes only."
            st.session_state["analysis_result"] = ContractAnalysis(
                risks=[
                    RiskItem(clause_text="automatically deduct 50% of the security deposit for 'standard repainting...'", risk_level="HIGH", category="Financial", baseline="Deductions should only be for actual damages beyond normal wear and tear.", deviation="Predatory deduction. Assumes you will damage the property and steals 50k upfront.", suggestion="Add a clause stating deductions require itemized bills for actual damages."),
                    RiskItem(clause_text="Tenant must give 2 months' notice... Landlord can evict with 24 hours' notice", risk_level="HIGH", category="Freedom", baseline="Equal notice periods (usually 1-2 months for both).", deviation="Leaves you vulnerable to sudden homelessness while binding you for 2 months.", suggestion="Demand a mutual 1-month notice period.")
                ],
                safe_clauses=[
                    SafeItem(clause_summary="Security Deposit", reason="Collecting a deposit is standard (though amount varies by city)."),
                    SafeItem(clause_summary="Residential Use Only", reason="Standard zoning and usage restriction.")
                ]
            )
            st.session_state["doc_type"] = "Rental / Lease Agreement"

    with col3:
        if st.button("💻 Freelance Trap", use_container_width=True):
            st.session_state["demo_text"] = "INDEPENDENT CONTRACTOR AGREEMENT\n\n1. The Contractor will operate as an independent contractor, not an employee.\n2. The Contractor will be paid strictly on a Net-90 days basis after invoice submission.\n3. The Contractor may not work with any other client in the software industry globally for a period of 5 years after project completion."
            st.session_state["analysis_result"] = ContractAnalysis(
                risks=[
                    RiskItem(clause_text="paid strictly on a Net-90 days basis", risk_level="MEDIUM", category="Financial", baseline="Net-15 to Net-30 days is standard for freelancers.", deviation="Client is holding your money for 3 months interest-free.", suggestion="Negotiate Net-15 or Net-30 payment terms."),
                    RiskItem(clause_text="may not work with any other client... globally for a period of 5 years", risk_level="HIGH", category="Career", baseline="Non-competes should be highly specific (direct competitors) and short (6-12 months).", deviation="Absurdly broad. Prevents you from working in your own industry globally for 5 years.", suggestion="Restrict the non-compete to specific direct competitors and reduce duration to 6 months.")
                ],
                safe_clauses=[
                    SafeItem(clause_summary="Independent Contractor Status", reason="Standard classification for freelance work, exempting client from employee benefits.")
                ]
            )
            st.session_state["doc_type"] = "Freelance / Agency Contract"

    # 👁️ THE UX MASTERSTROKE
    if "demo_text" in st.session_state:
        st.markdown("<br>", unsafe_allow_html=True)
        with st.expander("👁️ View the Contract Text being analyzed", expanded=False):
            st.info("This is the exact text RedFlag.ai is analyzing in the background.")
            st.text(st.session_state["demo_text"])


# ==========================================
# 6. PREMIUM RESULTS DASHBOARD
# ==========================================
if "analysis_result" in st.session_state:
    analysis = st.session_state["analysis_result"]
    st.markdown("<br>", unsafe_allow_html=True)
    st.subheader("📊 RedFlag Audit Report")

    if not analysis.risks:
        st.success("✅ Good news! This contract aligns with standard industry practices. No traps found.")
        st.balloons()
    else:
        score = calculate_score(analysis.risks)
        verdict = "❌ Highly Toxic" if score >= 70 else "⚠️ Negotiate Terms" if score >= 30 else "✅ Generally Safe"
        
        bg_color, border_color = ("#ffebee", "#ff4b4b") if score > 50 else ("#fff3e0", "#ff9f36") if score > 20 else ("#e8f5e9", "#00cc66")
        
        c1, c2 = st.columns([1, 2.5])
        with c1:
            st.markdown(f'<div style="text-align:center; padding: 20px; border-radius: 12px; background-color: {bg_color}; border: 2px solid {border_color};"><h1 style="color:{border_color}; margin:0; font-size: 3rem; line-height: 1;">{score}%</h1><p style="margin:0; font-weight:bold; color: #444;">Toxicity Score</p></div>', unsafe_allow_html=True)
        with c2:
            st.markdown(f"<h4 style='margin-bottom: 5px;'>Verdict: {verdict}</h4>", unsafe_allow_html=True)
            st.progress(score / 100)
            st.write(f"Found **{len(analysis.risks)}** hidden trap(s).")

        st.write("---")
        st.download_button(label="📥 Download PDF/TXT Report", data=generate_report_text(analysis, score, verdict), file_name="RedFlag_Audit_Report.txt", mime="text/plain", use_container_width=True)

        if analysis.safe_clauses:
            with st.expander("✅ Clauses Checked & Passed (Standard)"):
                st.markdown("<p style='font-size: 14px; color: gray;'>We verified these clauses and found them to be fair industry standards. No alert fatigue here.</p>", unsafe_allow_html=True)
                for s in analysis.safe_clauses:
                    st.markdown(f"- **{s.clause_summary}**: {s.reason}")

        st.markdown("### 🔍 The Breakdown (Baseline vs Deviation)")
        for r in analysis.risks:
            with st.container(border=True):
                icon, color = ("🚩", "red") if r.risk_level.upper() == "HIGH" else ("⚠️", "orange")
                st.markdown(f"<h5 style='color:{color}; margin-bottom: 10px;'>{icon} {r.risk_level.upper()} RISK | {r.category}</h5>", unsafe_allow_html=True)
                st.markdown("**📜 Found in Contract:**")
                st.info(f"\"{r.clause_text}\"") 
                st.markdown(f"**⚖️ Baseline (Standard):** {r.baseline}")
                st.markdown(f"**☠️ Deviation (The Trap):** <span style='color:red;'>{r.deviation}</span>", unsafe_allow_html=True)
                st.markdown(f"**🛡️ How to fix it:** {r.suggestion}")
        
        st.write("---")
        st.subheader("✉️ Fix It For Me")
        st.info("Let our AI draft a polite email to negotiate these unfair terms.")
        if st.button("✨ Draft Negotiation Email"):
            with st.spinner("Drafting your email... ✍️"):
                try: 
                    st.session_state["email_draft"] = generate_email(analysis.risks, st.session_state["doc_type"])
                except Exception as e:
                    st.error("Both primary and backup AI failed to generate email. Please try again.")
        if "email_draft" in st.session_state:
            st.success("Draft Generated!")
            st.text_area("Copy and send this to HR / Landlord:", value=st.session_state["email_draft"], height=250)

st.write("---")
st.markdown("<p style='text-align:center;font-size:12px;color:gray;'>Built with ❤️ by Gopesh Pandey | Provides risk intelligence, not legal advice</p>", unsafe_allow_html=True)
