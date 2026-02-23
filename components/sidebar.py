import streamlit as st
from core.backend import send_feedback

# ==========================================
# 6. THE SIDEBAR UI (ABOUT & FEEDBACK)
# ==========================================
def render_sidebar():
    with st.sidebar:
        st.markdown("### 🛡️ About TrueClause")
        st.caption("We provide baseline-aware contract intelligence, not legal advice. TrueClause helps you identify deviations from industry standards and asymmetric terms in your agreements.")
        st.write("---")
        
        st.markdown("### 💡 Anonymous Feedback")
        st.write("Help us improve the engine. No email required. 100% private.")
        
        with st.form("anonymous_feedback_form"):
            feedback_text = st.text_area("Found a bug or have a suggestion?", placeholder="Type your feedback here...", height=150)
            submitted = st.form_submit_button("Send Feedback 📤", use_container_width=True)
            
            if submitted:
                if len(feedback_text.strip()) < 5:
                    st.warning("Please provide a few more details so we can understand your feedback.")
                else:
                    with st.spinner("Securely routing your feedback... ⚙️"):
                        try:
                            # Calling the backend function
                            response = send_feedback(feedback_text)
                            if response.status_code in [200, 204]:
                                st.success("Feedback received! Thanks for helping us improve TrueClause.")
                        except Exception as e:
                            # Asli error screen par print karwao
                            st.error(f"System Error: {str(e)}")
                            # st.error("We couldn't connect to our servers right now. Please try again later.")
