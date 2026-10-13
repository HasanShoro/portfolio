# Subscription Cohort Retention Analysis

A portfolio-ready product analytics case study using monthly subscription-history records to measure cohort retention, compare renewal behavior, and recommend practical lifecycle actions.

## Dataset

- **Source:** Microsoft Learn, Dynamics 365 Customer Insights subscription churn sample
- **Documentation:** https://learn.microsoft.com/en-us/dynamics365/customer-insights/data/predict-subscription-churn
- **Local raw file:** `data/raw/subscription-history.csv`
- **Downloaded:** July 21, 2026
- **Important:** Microsoft presents this as sample data for a product walkthrough. It should be treated as demonstration data, not audited company performance.

## Reproduce

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python analysis.py
```

The script creates cleaned CSV exports, a 12-month cohort table, three charts, a readable HTML report, and a lightweight Jupyter notebook.

## Analytical definitions

- A customer is retained in a month when at least one subscription transaction appears in that month.
- Cohort month is the customer's first observed transaction month.
- Month 6 retention means activity at month index 5 or later; month 12 retention means activity at month index 11 or later.
- Auto-renew and price-band findings are observational. They do not establish causality.
- Gaps may represent pauses, billing timing, or sample-data behavior rather than confirmed churn.
