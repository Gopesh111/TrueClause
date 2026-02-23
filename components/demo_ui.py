import streamlit as st
from core.backend import ContractAnalysis, RiskItem, SafeItem

# ==========================================
# 5. THE DEMO TAB UI
# ==========================================
def render_demo_tab():
    st.info("⚡ Experience TrueClause instantly with these pre-analyzed, real-world examples.")
    
    # 🔄 THE TOGGLE LOGIC HELPER
    def toggle_demo_state(selected_doc_type, text_content, analysis_obj):
        # Agar same button wapas click hua hai, toh close kar do (clear state)
        if st.session_state.get("doc_type") == selected_doc_type:
            for key in ["demo_text", "analysis_result", "doc_type", "email_draft"]:
                st.session_state.pop(key, None)
        # Warna naya demo open kar do (set state)
        else:
            st.session_state["demo_text"] = text_content
            st.session_state["analysis_result"] = analysis_obj
            st.session_state["doc_type"] = selected_doc_type

    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("💼 Restrictive Job Offer", use_container_width=True):
            analysis = ContractAnalysis(
                risks=[
                    RiskItem(clause_text="Company reserves the right to terminate... while employee must serve a 90-day notice", risk_level="HIGH", category="Career", baseline="Mutual notice periods (e.g., 30 to 60 days for BOTH employer and employee).", deviation="Highly asymmetric. Gives the company power to fire you instantly, but forces you to stay for 3 months.", suggestion="Negotiate a mutual notice period (e.g., 30 days for both)."),
                    RiskItem(clause_text="pay a training recovery fee of ₹3,00,000 if they leave within the first 2 years", risk_level="HIGH", category="Financial", baseline="Companies cover standard onboarding costs. Bonds are only fair for expensive 3rd-party certifications.", deviation="Arbitrary financial trap. ₹3 Lakhs is excessive for basic training and acts as forced labor leverage.", suggestion="Ask for the bond to be removed or request an itemized list of training costs.")
                ],
                safe_clauses=[
                    SafeItem(clause_summary="Confidentiality (NDA)", reason="Standard practice to protect company IP."),
                    SafeItem(clause_summary="6-Month Probation Period", reason="Standard duration across the IT industry.")
                ]
            )
            text = "EMPLOYMENT AGREEMENT\n\n1. The employee shall be on a standard probation period of 6 months.\n2. The Company reserves the right to terminate the employee immediately without notice, while the employee must serve a 90-day notice period if they wish to resign.\n3. The Employee agrees to pay a training recovery fee of ₹3,00,000 if they leave within the first 2 years of service.\n4. The employee is bound by a standard confidentiality agreement (NDA) during and after employment."
            toggle_demo_state("Employment / Job Offer", text, analysis)

    with col2:
        if st.button("🏠 Unfair Lease Agreement", use_container_width=True):
            analysis = ContractAnalysis(
                risks=[
                    RiskItem(clause_text="automatically deduct 50% of the security deposit for 'standard repainting...'", risk_level="HIGH", category="Financial", baseline="Deductions should only be for actual damages beyond normal wear and tear.", deviation="Predatory deduction. Assumes you will damage the property and steals 50k upfront.", suggestion="Add a clause stating deductions require itemized bills for actual damages."),
                    RiskItem(clause_text="Tenant must give 2 months' notice... Landlord can evict with 24 hours' notice", risk_level="HIGH", category="Freedom", baseline="Equal notice periods (usually 1-2 months for both).", deviation="Leaves you vulnerable to sudden homelessness while binding you for 2 months.", suggestion="Demand a mutual 1-month notice period.")
                ],
                safe_clauses=[
                    SafeItem(clause_summary="Security Deposit", reason="Collecting a deposit is standard (though amount varies by city)."),
                    SafeItem(clause_summary="Residential Use Only", reason="Standard zoning and usage restriction.")
                ]
            )
            text = "LEASE AGREEMENT\n\n1. The Tenant shall pay a security deposit of ₹1,00,000.\n2. The Landlord reserves the right to automatically deduct 50% of the security deposit for 'standard repainting and deep cleaning' upon vacating, regardless of the flat's actual condition.\n3. The Tenant must give 2 months' notice to vacate, but the Landlord can evict the Tenant with 24 hours' notice.\n4. The Tenant is allowed to use the premises for residential purposes only."
            toggle_demo_state("Rental / Lease Agreement", text, analysis)

    with col3:
        if st.button("💻 Freelance Contract", use_container_width=True):
            analysis = ContractAnalysis(
                risks=[
                    RiskItem(clause_text="paid strictly on a Net-90 days basis", risk_level="MEDIUM", category="Financial", baseline="Net-15 to Net-30 days is standard for freelancers.", deviation="Client is holding your money for 3 months interest-free.", suggestion="Negotiate Net-15 or Net-30 payment terms."),
                    RiskItem(clause_text="may not work with any other client... globally for a period of 5 years", risk_level="HIGH", category="Career", baseline="Non-competes should be highly specific (direct competitors) and short (6-12 months).", deviation="Absurdly broad. Prevents you from working in your own industry globally for 5 years.", suggestion="Restrict the non-compete to specific direct competitors and reduce duration to 6 months.")
                ],
                safe_clauses=[
                    SafeItem(clause_summary="Independent Contractor Status", reason="Standard classification for freelance work, exempting client from employee benefits.")
                ]
            )
            text = "INDEPENDENT CONTRACTOR AGREEMENT\n\n1. The Contractor will operate as an independent contractor, not an employee.\n2. The Contractor will be paid strictly on a Net-90 days basis after invoice submission.\n3. The Contractor may not work with any other client in the software industry globally for a period of 5 years after project completion."
            toggle_demo_state("Freelance / Agency Contract", text, analysis)

    # 👁️ THE UX MASTERSTROKE
    if "demo_text" in st.session_state:
        st.markdown("<br>", unsafe_allow_html=True)
        with st.expander("👁️ View the Contract Text being analyzed", expanded=False):
            st.info("This is the exact text TrueClause is analyzing in the background.")
            st.text(st.session_state["demo_text"])
