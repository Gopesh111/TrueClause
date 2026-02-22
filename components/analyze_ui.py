import streamlit as st
from core.backend import analyze_contract, extract_text_from_pdf

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
except ImportError:
    st.warning("⚠️ Our knowledge base is currently updating. Some features might be temporarily unavailable.")
    st.stop()

# ==========================================
# 2. HELPER TO CLEAR STATE
# ==========================================
def clear_state():
    if "analysis_result" in st.session_state: del st.session_state["analysis_result"]
    if "email_draft" in st.session_state: del st.session_state["email_draft"]
    if "demo_text" in st.session_state: del st.session_state["demo_text"]

# ==========================================
# 3. THE ANALYZE TAB UI
# ==========================================
def render_analyze_tab():
    rule_mapping = {
        "Employment / Job Offer": EMPLOYMENT_RULES, 
        "Rental / Lease Agreement": RENTAL_RULES, 
        "Freelance / Agency Contract": FREELANCE_RULES, 
        "NDA / Confidentiality": NDA_RULES, 
        "Terms of Service / Privacy Policy": TOS_RULES, 
        "Other / Generic Contract": GENERIC_RULES
    }
    
    col1, col2 = st.columns(2)
    with col1: 
        doc_type = st.selectbox("📄 Step 1: Document Type", list(rule_mapping.keys()), on_change=clear_state)
    with col2: 
        language = st.selectbox("🌐 Step 2: Explanation Language", ["English", "Hindi", "Hinglish"], on_change=clear_state)
    
    uploaded_file = st.file_uploader("📂 Step 3: Upload PDF Contract", type=["pdf"], on_change=clear_state)
    
    user_text = ""
    if uploaded_file is not None:
        try:
            extracted_text = extract_text_from_pdf(uploaded_file)
            if len(extracted_text.split()) < 30:
                st.warning("⚠️ We couldn't extract enough text from this PDF. It might be a scanned image. Please copy and paste the text manually below.")
            else:
                user_text = extracted_text
                st.success("PDF Text Extracted Successfully! Ready to audit.")
                with st.expander("👁️ View Extracted Text"): 
                    st.text(user_text[:1000] + "... (truncated)")
        except Exception:
            # GRACEFUL HANDLING: No technical error shown
            st.warning("⚠️ We couldn't read this specific PDF format. Could you please copy and paste the text manually below?")
            
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
                except Exception:
                    # GRACEFUL HANDLING: No raw errors, just a polite message
                    st.warning("⚠️ Our AI engines are experiencing unusually high traffic right now. Please try clicking 'Audit' again in a few seconds!")