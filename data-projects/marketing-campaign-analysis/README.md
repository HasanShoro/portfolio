# Marketing Campaign Performance Analysis

A portfolio-ready marketing analytics project using the UCI Bank Marketing dataset to evaluate the conversion funnel, channel performance, audience segments, campaign fatigue, and a transparent ROI allocation scenario.

## Dataset

- **Dataset:** Bank Marketing
- **Publisher:** UCI Machine Learning Repository
- **Dataset page:** https://archive.ics.uci.edu/dataset/222/bank+marketing
- **DOI:** https://doi.org/10.24432/C5K306
- **License:** Creative Commons Attribution 4.0 International (CC BY 4.0)
- **Local archive:** `data/raw/bank-marketing.zip`
- **Analysis file:** `data/raw/bank-additional/bank-additional/bank-additional-full.csv`
- **Downloaded:** July 21, 2026

## Reproduce

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python analysis.py
```

## ROI scenario assumptions

The dataset does not contain media spend or customer lifetime value, so the project models—not reports—ROI:

- Cellular contact cost: `$2.50`
- Telephone contact cost: `$5.00`
- Contribution value per conversion: `$240`
- ROI: `(modeled value - modeled spend) / modeled spend`

These assumptions are isolated in `analysis.py` so a reviewer can test alternative scenarios.

## Limitations

- Call duration is only known after contact. It describes engagement stages but must not be used as a pre-contact targeting feature.
- Channel recommendations reflect modeled unit economics and observed conversion, not a randomized experiment.
- The campaign occurred from May 2008 to November 2010, so response patterns may not transfer directly to modern digital campaigns.
