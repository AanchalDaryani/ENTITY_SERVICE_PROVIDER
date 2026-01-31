
---

## Data Quality Rules Implemented

### Rule 1 — Missing Mandatory Providers
Each entity is expected to have an Auditor, Custodian, and Administrator.

**Finding:**  
~27% of entities were missing at least one mandatory provider type, indicating
data completeness or onboarding issues.

---

### Rule 2 — Multiple Active Providers
Entities should not have more than one active provider of the same type at a given time.

**Finding:**  
~2% of entities had multiple active providers, representing a governance risk.

---

### Rule 3 — Overlapping Relationship Periods
Historical provider relationship periods should not overlap.

**Finding:**  
~2.5% of entities showed overlapping periods, indicating audit trail inconsistencies.

---

## Summary of Findings

| Data Quality Rule | Affected Entities | Impact |
|------------------|------------------|--------|
| Missing Providers | ~272 | 27.2% |
| Multiple Active Providers | 19 | 1.9% |
| Overlapping Periods | 25 | 2.5% |

---

## Key Insights
- Most data quality issues relate to **completeness**, not governance
- Governance and audit issues occur less frequently but carry higher risk
- Upstream data generation and process design strongly affect downstream data quality

---

## Remediation Strategy
- Enforce mandatory provider assignment during entity onboarding
- Prevent multiple active providers via temporal validation
- Validate date ranges to avoid historical overlaps
- Periodically audit provider relationship data

---

## Why This Project
This project was designed to move beyond generic data analysis and focus on how analysts
work with relational data, data quality rules, and governance checks in real-world systems.

It reflects realistic challenges faced in analytics, compliance, and data engineering roles.
