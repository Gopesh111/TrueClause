import streamlit as st
from core.backend import send_feedback

# ==========================================
# 6. THE SIDEBAR UI (ABOUT & FEEDBACK)
# ==========================================
def render_sidebar():
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
                            # Calling the backend function
                            response = send_feedback(feedback_text)
                            if response.status_code in [200, 204]:
                                st.success("Sent! Thanks for helping us improve. 🎉")
                                st.balloons()
                        except Exception as e:
                            # GRACEFUL HANDLING: Catching webhook errors politely
                            st.error("Oops! Something went wrong with the connection. Please try again later.")