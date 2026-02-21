# rules/nda.py

NDA_RULES = """
CONTRACT TYPE: Non-Disclosure Agreement (NDA) or Confidentiality Agreement.

GLOBAL HEURISTICS (FLAG THESE IMMEDIATELY):
1. INFINITE TIME: NDA lasting forever for standard business information.
2. OVERREACH:  🚩 RED FLAG: Defining publicly available, independently developed, or previously known information as confidential.

INTERPRETATION RULE:
A clause should be flagged only if it restricts reasonable professional activity or creates disproportionate legal risk beyond standard confidentiality protection.
BASELINE VS. RED FLAGS (DETECT DEVIATIONS):

1. DURATION OF CONFIDENTIALITY
   - Standard: Confidentiality lasts for a reasonable, defined period (commonly 1 to 3 years) after the agreement ends. Trade secrets may be protected longer.
   - 🚩 RED FLAG: Perpetual (lifetime) confidentiality for general, non-trade-secret business information.

2. PENALTIES & DAMAGES
   - Standard: The breaching party is liable for actual, provable damages.
   - 🚩 RED FLAG: Excessive "Liquidated Damages" (e.g., "Any breach will result in an immediate penalty of $500,000" regardless of actual harm).

3. EXCLUSIONS (WHAT IS NOT CONFIDENTIAL)
   - Standard: Information already known to the receiver, public knowledge, or independently developed is excluded.
   - 🚩 RED FLAG: Missing the standard exclusions, meaning you could be sued for sharing something that is already on Google.
4. ONE-WAY (UNILATERAL) NDA
   - Standard: NDA obligations are mutual when both parties share confidential information.
   - 🚩 RED FLAG: NDA imposes confidentiality obligations only on one party, even though both parties exchange sensitive information.
5. USE OF GENERAL SKILLS & EXPERIENCE
   - Standard: NDA cannot restrict the use of general professional skills, experience, or know-how gained during engagement.
   - 🚩 RED FLAG: NDA language that prevents the individual from using general knowledge or experience in future work.
6. INJUNCTIVE RELIEF & IMMEDIATE ACTION
   - Standard: Injunctive relief is limited to actual, provable risk of irreparable harm.
   - 🚩 RED FLAG: Automatic or unconditional right to injunction without requiring proof of actual harm.
"""