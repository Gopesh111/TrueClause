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
    st.subheader("📊 RedFlag Audit Report")

    # Agar koi risk nahi mila
    if not analysis.risks:
        st.success("✅ Good news! This contract aligns with standard industry practices. No traps found.")
        st.balloons()
        return

    # Score aur Verdict calculate karna
    score = calculate_score(analysis.risks)
    verdict = "❌ Highly Toxic" if score >= 70 else "⚠️ Negotiate Terms" if score >= 30 else "✅ Generally Safe"
    
    # UI Colors based on score
    bg_color, border_color = ("#ffebee", "#ff4b4b") if score > 50 else ("#fff3e0", "#ff9f36") if score > 20 else ("#e8f5e9", "#00cc66")
    
    c1, c2 = st.columns([1, 2.5])
    with c1: 
        st.markdown(f'<div style="text-align:center; padding: 20px; border-radius: 12px; background-color: {bg_color}; border: 2px solid {border_color};"><h1 style="color:{border_color}; margin:0; font-size: 3rem; line-height: 1;">{score}%</h1><p style="margin:0; font-weight:bold; color: #444;">Toxicity Score</p></div>', unsafe_allow_html=True)
    with c2:
        st.markdown(f"<h4 style='margin-bottom: 5px;'>Verdict: {verdict}</h4>", unsafe_allow_html=True)
        st.progress(score / 100)
        st.write(f"Found **{len(analysis.risks)}** hidden trap(s).")

    st.write("---")
    
    # Download Button
    st.download_button(
        label="📥 Download PDF/TXT Report", 
        data=generate_report_text(analysis, score, verdict), 
        file_name="RedFlag_Audit_Report.txt", 
        mime="text/plain", 
        use_container_width=True
    )

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
                st.warning(f"⚠️ {str(e)} Please try drafting again in a few moments.")
                
    if "email_draft" in st.session_state:
        st.success("Draft Generated!")
        st.text_area("Copy and send this to HR / Landlord:", value=st.session_state["email_draft"], height=250)