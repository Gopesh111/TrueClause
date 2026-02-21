# rules/employment.py

EMPLOYMENT_RULES = """
NOTE:
For Independent Contractors, apply these rules conservatively. Independent contractors typically accept higher risk, but power asymmetry, vague penalties, and unpaid ownership transfers are still red flags.
CONTRACT TYPE: Employment, Job Offer, or Independent Contractor Agreement.
INTERPRETATION RULE:
A clause should only be flagged if it materially increases risk beyond what a reasonable professional would expect for this role and seniority level.
GLOBAL HEURISTICS (FLAG THESE IMMEDIATELY):
1. VAGUENESS: Words like "at company's sole discretion", "as deemed fit", "without prior notice" when tied to penalties, salary deductions, or termination.
2. INFINITE TIME: "Perpetual", "lifetime", or "indefinite" restrictions applied to non-competes or to confidentiality covering general skills, knowledge, or publicly known information.
3. POWER ASYMMETRY: Rights given exclusively to the employer without matching obligations, or penalties for the employee without an appeal/warning process.

BASELINE VS. RED FLAGS (DETECT DEVIATIONS):

1. NOTICE PERIOD & TERMINATION
   - Standard: Mutual notice period of 15 to 90 days. Employer can terminate immediately ONLY for severe cause (fraud, crime, severe misconduct).
   - 🚩 RED FLAG: Unilateral termination (Employer gives 0 days, Employee must give 30+ days).
   - 🚩 RED FLAG: Notice periods exceeding 90 days.
   - 🚩 RED FLAG: Company reserving the right to withhold full final settlement if notice period is not served, without offering a buyout option.

2. FINANCIAL PENALTIES & BONDS
   - Standard: Clawback of joining bonus/relocation allowance if employee leaves within 1 year.
   - 🚩 RED FLAG: "Training Bonds" or penalties (e.g., Fixed amount like ₹3,00,000) without explicit proof of actual, out-of-pocket training costs.
   - 🚩 RED FLAG: Salary withholding or deductions for "poor performance" or "damages" without a legal/objective audit.

3. INTELLECTUAL PROPERTY (IP) & MOONLIGHTING
   - Standard: Company owns IP created during working hours, using company equipment, or directly related to the company's current business.
   - 🚩 RED FLAG: Company claiming ownership of ALL IP created by the employee, including weekend side-projects built on personal devices (Pre-invention assignment overreach).
   - 🚩 RED FLAG: Total ban on all outside activities/hobbies even if they are non-commercial and don't conflict with the company.

4. NON-COMPETE & NON-SOLICITATION
   - Standard: Cannot join a direct, named competitor or poach current clients/employees for 6 to 12 months after leaving.
   - 🚩 RED FLAG: Blanket bans on working in the entire industry (e.g., "Cannot work in IT or Software").
   - 🚩 RED FLAG: Non-compete periods lasting longer than 12 months.

5. RELOCATION & ROLE CHANGES
   - Standard: Employee works at the designated location and role.
   - 🚩 RED FLAG: Clause stating the company can transfer the employee to any global/national location, or change their role entirely, without the employee's consent or compensation adjustment.
      - 🚩 RED FLAG: Clause allowing assignment of additional responsibilities that are substantially unrelated to the original role, without compensation review.

6. FINAL SETTLEMENT & EXIT BLOCKING
   - Standard: Employer releases full and final settlement within a reasonable time after exit, subject to clear dues.
   - 🚩 RED FLAG: Company reserves the right to delay or withhold final settlement, experience letter, or relieving letter indefinitely.
   - 🚩 RED FLAG: Linking final settlement to vague conditions like "management approval" or "successful knowledge transfer".
"""