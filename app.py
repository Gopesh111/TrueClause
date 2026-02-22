import streamlit as st

# ==========================================
# 1. IMPORTING OUR CUSTOM UI COMPONENTS
# ==========================================
from components.sidebar import render_sidebar
from components.analyze_ui import render_analyze_tab
from components.demo_ui import render_demo_tab
from components.dashboard_ui import render_dashboard

# ==========================================
# 2. PAGE CONFIGURATION
# ==========================================
st.set_page_config(
    page_title="RedFlag.ai | Enterprise Risk Analyzer", 
    page_icon="🚩", 
    layout="centered", 
    initial_sidebar_state="expanded"
)

# ==========================================
# 3. RENDER SIDEBAR
# ==========================================
render_sidebar()

# ==========================================
# 4. MAIN HEADER
# ==========================================
st.markdown("<h1 style='text-align:center;'>🚩 RedFlag.ai</h1>", unsafe_allow_html=True)
st.markdown("<h5 style='text-align:center;color:gray;margin-top:-10px;margin-bottom:20px;'>Baseline-aware risk intelligence. We don't explain the law, we detect the deviations.</h5>", unsafe_allow_html=True)

# ==========================================
# 5. CLEAR STATE FUNCTION
# ==========================================
def clear_state():
    for key in ["analysis_result", "email_draft", "demo_text", "doc_type"]:
        if key in st.session_state: 
            del st.session_state[key]

# ==========================================
# 6. APP NAVIGATION (RADIO BUTTONS)
# ==========================================

app_mode = st.radio(
    "Choose Mode:", 
    ["📝 Analyze Your Contract", "⚡ Instant Demos"], 
    horizontal=True, 
    label_visibility="collapsed", 
    on_change=clear_state
)

st.markdown("<br>", unsafe_allow_html=True)

if app_mode == "📝 Analyze Your Contract":
    render_analyze_tab()
else:
    render_demo_tab()

# ==========================================
# 7. RESULTS DASHBOARD
# ==========================================
render_dashboard()

# ==========================================
# 8. FOOTER
# ==========================================
st.write("---")
st.markdown("<p style='text-align:center;font-size:12px;color:gray;'>Built with ❤️ by Gopesh Pandey | Provides risk intelligence, not legal advice</p>", unsafe_allow_html=True)
