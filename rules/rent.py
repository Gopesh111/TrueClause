# rules/rent.py

RENTAL_RULES = """
CONTRACT TYPE: Residential Lease, Rent Agreement, or PG Accommodation.
INTERPRETATION RULE:
A clause should only be flagged if it materially restricts the tenant’s rights, privacy, or financial security beyond what is reasonably expected for similar housing in that locality.
GLOBAL HEURISTICS (FLAG THESE IMMEDIATELY):
1. VAGUENESS: "General wear and tear" not being defined, or "any inconvenience to landlord" leading to eviction.
2. POWER ASYMMETRY: Landlord imposing heavy daily fines for late rent, but taking 0 responsibility for delayed emergency repairs.

BASELINE VS. RED FLAGS (DETECT DEVIATIONS):

1. DEPOSIT & DEDUCTIONS
   - Standard: Security deposit of 1 to 3 months' rent (varies by region, but standard). Deductions ONLY for actual, documented damages beyond normal wear and tear, or unpaid utility bills.
   - 🚩 RED FLAG: Deposits exceeding 4-6 months' rent (unless explicitly standard in that specific city).
   - 🚩 RED FLAG: Fixed mandatory deductions (e.g., "One month rent will be deducted for painting/cleaning regardless of condition").
   - 🚩 RED FLAG: Clause stating the landlord can withhold the deposit indefinitely or without a defined maximum timeline after move-out.
2. LOCK-IN PERIOD & EVICTION
   - Standard: 6 to 11 months lock-in. 1 to 2 months notice period for both parties.
   - 🚩 RED FLAG: Tenant must pay the ENTIRE remaining lease amount if they break the lock-in period (Standard penalty is just losing 1-2 months deposit).
   - 🚩 RED FLAG: Landlord's right to evict the tenant with 24 hours to 7 days notice without a severe breach of contract.

3. PRIVACY & ACCESS
   - Standard: Landlord can enter for repairs or inspections with 24 to 48 hours prior notice, at reasonable hours.
   - 🚩 RED FLAG: Landlord reserves the right to enter the premises at ANY time, without prior notice.

4. MAINTENANCE & REPAIRS
   - Standard: Tenant handles minor day-to-day fixes (e.g., bulbs, minor clogs). Landlord handles structural, electrical, or major plumbing issues.
   - 🚩 RED FLAG: Making the tenant fully financially responsible for structural damage, appliance breakdowns (provided by landlord), or building wear-and-tear.

5. RESTRICTIONS (PG / RENTALS)
   - Standard: No illegal activities, no major structural alterations without permission.
   - 🚩 RED FLAG: Extreme lifestyle policing that restricts lawful personal choices unrelated to property safety or legality (e.g., blanket bans on all guests during daytime).
6. UTILITIES & COMMON CHARGES
   - Standard: Tenant pays for metered utilities (electricity, water, gas) actually consumed. Common area maintenance is predefined.
   - 🚩 RED FLAG: Flat-rate or arbitrary utility charges without meter readings.
   - 🚩 RED FLAG: Charging the tenant for building-wide expenses, society penalties, or owner dues.
7. EMERGENCY & FORCE MAJEURE EXIT
   - Standard: Reasonable exit options during uncontrollable events (job loss, relocation, government orders), subject to notice.
   - 🚩 RED FLAG: Clause explicitly denying any exit or refund even in force majeure situations.
8. DISPUTE RESOLUTION
   - Standard: Local jurisdiction or mutually accessible dispute resolution.
   - 🚩 RED FLAG: Forcing dispute resolution in a distant or impractical jurisdiction for the tenant.
"""