# rules/tos.py

TOS_RULES = """
CONTRACT TYPE: Terms of Service (ToS), Privacy Policy, or Software License.

GLOBAL HEURISTICS (FLAG THESE IMMEDIATELY):
1. POWER ASYMMETRY: Company can change the rules at any time without notifying the user, but holds the user strictly accountable.
2. LOSS OF RIGHTS: Forced arbitration without a reasonable opt-out mechanism or meaningful alternative dispute resolution.
INTERPRETATION RULE:
A clause should be flagged only if it significantly reduces user rights, control, or remedies beyond what a reasonable user would expect when using similar digital services.
BASELINE VS. RED FLAGS (DETECT DEVIATIONS):

1. DATA PRIVACY & SHARING
   - Standard: Data is used to provide the service and shared with essential infrastructure partners (e.g., AWS, payment gateways).
   - 🚩 RED FLAG: Explicit right to SELL personal data or user content to third-party data brokers or marketing agencies.
   - 🚩 RED FLAG: Claiming copyright or ownership over user-generated content beyond a limited license necessary to operate the service.

2. MODIFICATION OF TERMS
   - Standard: Company will notify users via email or prominent notice 30 days before major terms change.
   - 🚩 RED FLAG: "We reserve the right to change these terms at any time without notice. Continued use constitutes acceptance."

3. DISPUTE RESOLUTION
   - Standard: Disputes handled in a neutral jurisdiction or via mutual arbitration.
   - 🚩 RED FLAG: Forced binding arbitration in a highly inconvenient jurisdiction (e.g., forcing an Indian user to fight a case in a specific US state) with a blanket ban on class-action lawsuits.
4. ACCOUNT TERMINATION & SERVICE ACCESS
   - Standard: Company may suspend or terminate accounts for clear policy violations, with notice and appeal where feasible.
   - 🚩 RED FLAG: Company can permanently suspend or delete user accounts, content, or paid access at its sole discretion, without notice, explanation, or appeal.
5. BILLING, AUTO-RENEWAL & REFUNDS
   - Standard: Clear disclosure of pricing, renewal frequency, and cancellation method.
   - 🚩 RED FLAG: Auto-renewal without clear prior notice or requiring unreasonable steps to cancel.
   - 🚩 RED FLAG: Blanket "no refunds under any circumstances" clauses for paid subscriptions.
6. LIMITATION OF LIABILITY
   - Standard: Company limits liability to a reasonable extent.
   - 🚩 RED FLAG: Company disclaims all liability, even for data loss, security breaches, or financial harm caused by its own negligence.
"""