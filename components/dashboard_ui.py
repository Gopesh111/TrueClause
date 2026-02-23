import streamlit as st
from core.backend import calculate_score, generate_report_text, generate_email

# ==========================================
# 4. THE RESULTS DASHBOARD UI
# ==========================================
def render_dashboard():
    # Agar abhi tak koi analysis nahi hua hai, toh dashboard mat dikhao
    if "analysis_result" not in st.session_state: 
        return
    
    analysis = st.session_state["analysis_result"]
    st.markdown("<br>", unsafe_allow_html=True)
    st.subheader("🛡️ TrueClause Intelligence Report")

    # Agar koi risk nahi mila
    if not analysis.risks:
        st.success("✅ Good news! This contract aligns with standard industry practices. No significant deviations found.")
        st.balloons()
        return

    # Score aur Verdict calculate karna
    score = calculate_score(analysis.risks)
    verdict = "⚠️ High Risk Exposure" if score >= 70 else "⚖️ Review & Negotiate" if score >= 30 else "✅ Standard Terms"
    
    # Premium B2B SaaS Colors (Tailwind inspired soft backgrounds with crisp borders)
    if score >= 70:
        bg_color, border_color = "#FEF2F2", "#DC2626" # Soft Red
    elif score >= 30:
        bg_color, border_color = "#FFFBEB", "#D97706" # Soft Amber
    else:
        bg_color, border_color = "#F0FDF4", "#16A34A" # Soft Green
    
    c1, c2 = st.columns([1, 2.5])
    with c1: 
        st.markdown(f'<div style="text-align:center; padding: 20px; border-radius: 12px; background-color: {bg_color}; border: 1px solid {border_color}; box-shadow: 0 4px 6px rgba(0,0,0,0.05);"><h1 style="color:{border_color}; margin:0; font-size: 3rem; line-height: 1;">{score}%</h1><p style="margin:0; font-weight:600; color: #475569; font-size:14px; margin-top:5px;">Risk Exposure</p></div>', unsafe_allow_html=True)
    with c2:
        st.markdown(f"<h4 style='margin-bottom: 5px; color: #1E293B;'>Verdict: {verdict}</h4>", unsafe_allow_html=True)
        st.progress(score / 100)
        st.write(f"Found **{len(analysis.risks)}** clause deviation(s).")

    st.write("---")
    
    # Download Button
    st.download_button(
        label="📥 Download TrueClause Report", 
        data=generate_report_text(analysis, score, verdict), 
        file_name="TrueClause_Audit_Report.txt", 
        mime="text/plain", 
        use_container_width=True
    )

    if analysis.safe_clauses:
        with st.expander("✅ Clauses Checked & Passed (Industry Standard)"):
            st.markdown("<p style='font-size: 14px; color: #64748B;'>We verified these clauses against market baselines. No alert fatigue here.</p>", unsafe_allow_html=True)
            for s in analysis.safe_clauses:
                st.markdown(f"- **{s.clause_summary}**: {s.reason}")

    st.markdown("<h3 style='color: #1E3A8A; margin-top: 20px;'>🔍 The Breakdown (Baseline vs Deviation)</h3>", unsafe_allow_html=True)
    for r in analysis.risks:
        with st.container(border=True):
            icon, color = ("🚨", "#DC2626") if r.risk_level.upper() == "HIGH" else ("⚠️", "#D97706")
            st.markdown(f"<h5 style='color:{color}; margin-bottom: 10px;'>{icon} {r.risk_level.upper()} RISK | {r.category}</h5>", unsafe_allow_html=True)
            st.markdown("**📜 Found in Contract:**")
            st.info(f"\"{r.clause_text}\"") 
            st.markdown(f"**⚖️ Baseline (Standard):** {r.baseline}")
            st.markdown(f"**⚠️ Deviation Found:** <span style='color:{color}; font-weight:500;'>{r.deviation}</span>", unsafe_allow_html=True)
            st.markdown(f"**🛡️ Recommended Fix:** {r.suggestion}")
            
    st.write("---")
    
    st.subheader("✉️ Negotiation Assistant")
    st.info("Let our agentic workflow draft a polite, corporate-ready email to negotiate these flagged terms.")
    if st.button("✨ Draft Negotiation Email"):
        with st.spinner("Drafting your email... ✍️"):
            try: 
                st.session_state["email_draft"] = generate_email(analysis.risks, st.session_state["doc_type"])
            except Exception as e:
                st.warning(f"⚠️ {str(e)} Please try drafting again in a few moments.")
                
    if "email_draft" in st.session_state:
        st.success("Draft Generated!")
        st.text_area("Review, copy, and send:", value=st.session_state["email_draft"], height=250)
