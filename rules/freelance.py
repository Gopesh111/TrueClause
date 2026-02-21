# rules/freelance.py

FREELANCE_RULES = """
CONTRACT TYPE: Freelance, Independent Contractor, Agency, or Vendor Agreement.
INTERPRETATION RULE:
A clause should be flagged only if it shifts unreasonable business risk to the freelancer compared to standard independent contractor practices.

GLOBAL HEURISTICS (FLAG THESE IMMEDIATELY):
1. VAGUENESS: "Unlimited revisions", "satisfactory quality" (without objective metrics).
2. POWER ASYMMETRY: Client takes full ownership of the work immediately, but payment is delayed by 90+ days or contingent on their own clients paying them ("pay-when-paid" clauses).

BASELINE VS. RED FLAGS (DETECT DEVIATIONS):

1. INTELLECTUAL PROPERTY (IP) TRANSFER
   - Standard: IP rights transfer to the client ONLY upon full and final payment.
   - 🚩 RED FLAG: Clause stating the client owns the IP upon creation, even if the freelancer hasn't been paid yet.
   - 🚩 RED FLAG: Banning the freelancer from showcasing the work in a private portfolio, unless the engagement is explicitly defined as ghostwriting or white-label work with appropriate compensation.
2. PAYMENT TERMS
   - Standard: Net-15 to Net-30 days. Late payment incurs a standard interest fee (e.g., 1.5% per month).
   - 🚩 RED FLAG: Net-90 or Net-120 payment terms (making the freelancer act like a free bank for the client).
   - 🚩 RED FLAG: "Pay-when-paid" clauses (you only get paid if the client's customer pays them).

3. NON-COMPETE FOR FREELANCERS
   - Standard: Cannot steal the client's direct customers.
   - 🚩 RED FLAG: Broad Non-Compete clauses restricting freelancers from working with competitors beyond protecting the client’s direct customers or confidential information. 
4. SCOPE CREEP & UNPAID WORK
   - Standard: Clear project scope with defined deliverables. Additional work requires written approval and revised payment.
   - 🚩 RED FLAG: Clauses allowing the client to request additional features, revisions, or support beyond the original scope without extra compensation.
   - 🚩 RED FLAG: "Unlimited revisions" without a cap or definition of what counts as a revision.
5. TERMINATION & PARTIAL PAYMENT
   - Standard: If the contract is terminated early, the freelancer is paid for all work completed up to the termination date.
   - 🚩 RED FLAG: Client can terminate the contract at any time without paying for completed or in-progress work.
6. LIABILITY & INDEMNITY
   - Standard: Freelancer is responsible only for their own intentional misconduct or gross negligence.
   - 🚩 RED FLAG: Freelancer must indemnify the client for all losses, lawsuits, or third-party claims, even those unrelated to the freelancer’s work.
"""