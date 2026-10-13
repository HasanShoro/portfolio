# Hasan Mustafa Shoro — Data & Business Analyst

Source for my portfolio site plus three end-to-end data analytics case studies. Operations Coordinator & Dispatcher at Mosaic Supply Chain, moving into data and business analysis.

- Résumé: [resume/Hasan-Shoro-Resume.pdf](resume/Hasan-Shoro-Resume.pdf)
- LinkedIn: [linkedin.com/in/hasan-mustafa-shoro](https://www.linkedin.com/in/hasan-mustafa-shoro/)

| Project | Focus | Tools | Headline result |
|---|---|---|---|
| [Online Retail Performance](data-projects/online-retail-analysis/) | Revenue drivers, seasonality, RFM customer segments | Python, pandas, Matplotlib | £10.7M revenue across 19,960 orders analyzed |
| [Subscription Cohort Retention](data-projects/cohort-retention-analysis/) | Cohort retention, renewal behavior | Python, pandas, Matplotlib | 62.4% six-month / 49.2% twelve-month retention |
| [Marketing Campaign ROI](data-projects/marketing-campaign-analysis/) | Funnel, channel economics, segments | Python, pandas, Matplotlib | 41,188 contacts, 11.3% conversion |

Each project folder has its own README, a reproducible `analysis.py`, charts, and an HTML report in `report/`.

## Run a project

```bash
cd data-projects/<project>
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python analysis.py
```

`online-retail-analysis/data/processed/clean_online_retail.csv` (54 MB) is not committed; `analysis.py` regenerates it from the raw workbook.

## Contact

- Email: hmshoro@gmail.com
- LinkedIn: https://www.linkedin.com/in/hasan-mustafa-shoro/
