# rules/generic.py

GENERIC_RULES = """
CONTRACT TYPE: Unknown, Custom, or Generic Commercial Agreement.

GLOBAL HEURISTICS (THE UNIVERSAL LAWS OF CONTRACTS):
Since the exact nature of this contract is unknown, you must apply the fundamental principles of contract fairness. 
DO NOT flag standard boilerplate clauses (e.g., standard severability, force majeure, standard notices).
FINAL SAFETY RULE:
When contract type is unknown, err on the side of NOT flagging unless the risk is clear, disproportionate, and irreversible.

ONLY FLAG CLAUSES IF THEY VIOLATE THESE UNIVERSAL PRINCIPLES:

1. MUTUALITY & ASYMMETRY (TERMINATION)
   - Standard: Both parties have reasonable rights to terminate the agreement for cause, or with reasonable notice for convenience.
   - 🚩 RED FLAG: Unilateral "Termination for Convenience" (One party can walk away anytime without penalty, but the other is locked in strictly).

2. UNCAPPED LIABILITY & INDEMNIFICATION
   - Standard: Liability is capped at the total amount paid under the contract, or a reasonable multiple.
   - 🚩 RED FLAG: "Uncapped Liability" for one party while the other party's liability is strictly limited to $0 or a negligible amount.
   - 🚩 RED FLAG: One-sided indemnification (e.g., Party A must pay for all legal costs of Party B, even if Party B made the mistake).

3. UNILATERAL MODIFICATION (THE "GOD" CLAUSE)
   - Standard: Changes to the contract require written agreement/signatures from both parties.
   - 🚩 RED FLAG: One party reserves the right to change the terms, pricing, or deliverables at any time, without the explicit consent of the other party.

4. DISPUTE RESOLUTION & JURISDICTION TRAPS
   - Standard: Disputes are settled in a mutually convenient jurisdiction or through standard arbitration.
   - 🚩 RED FLAG: Forcing the weaker party to fight legal battles in an extremely unreasonable or foreign jurisdiction (e.g., a local vendor in India being forced to arbitrate in Delaware, USA) with a total ban on class actions or appeals.

5. VAGUE PENALTIES
   - Standard: Penalties for breach are clearly defined and proportionate to the harm.
   - 🚩 RED FLAG: Vague, massive financial penalties for undefined "breaches of trust" or "inconvenience".
6. PAYMENT WITHHOLDING & UNCERTAINTY
   - Standard: Payment terms are clear, time-bound, and enforceable.
   - 🚩 RED FLAG: One party can delay, suspend, or refuse payment based on vague conditions such as "satisfaction", "internal approval", or "client payment".
7. ASSIGNMENT & TRANSFER OF OBLIGATIONS
   - Standard: Neither party can transfer the contract to a third party without consent.
   - 🚩 RED FLAG: One party can freely assign or sell the contract to any third party, while the other party is explicitly prohibited from doing so.
8. SURVIVAL OF OBLIGATIONS
   - Standard: Only essential clauses (payment, confidentiality, dispute resolution) survive termination.
   - 🚩 RED FLAG: Broad language stating that "all obligations" survive termination, effectively extending penalties indefinitely.
"""