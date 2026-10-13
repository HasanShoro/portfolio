# Online Retail Performance Analysis

A portfolio-ready business analysis of transaction data from a UK-based online retailer. The project asks:

> Which products, markets, customer groups, and seasonal patterns drive revenue, and where should the business focus next?

## Local dataset files

The complete public dataset is stored locally in `data/raw/`:

- `Online Retail.xlsx` — original workbook from UCI (541,909 transaction rows)
- `online-retail.zip` — original downloaded archive
- `data/processed/clean_online_retail.csv` — reusable cleaned transaction-level export created by the analysis
- `data/processed/customer_segments.csv` — customer-level RFM segmentation export

The Python analysis reads the local Excel workbook. It does not depend on a remote data URL at runtime.

## Source and license

- **Dataset:** Online Retail
- **Publisher:** UCI Machine Learning Repository
- **Dataset page:** https://archive.ics.uci.edu/dataset/352/online-retail
- **Permanent identifier:** https://doi.org/10.24432/C5BW33
- **License:** Creative Commons Attribution 4.0 International (CC BY 4.0)
- **Downloaded:** July 21, 2026
- **Attribution:** Chen, D. (2015). Online Retail [Dataset]. UCI Machine Learning Repository. https://doi.org/10.24432/C5BW33

CC BY 4.0 permits sharing and adaptation, including portfolio and educational use, provided appropriate credit is given and changes are indicated. License details: https://creativecommons.org/licenses/by/4.0/

## Reproduce the analysis

From this folder:

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python analysis.py
```

The script cleans the data, exports analysis-ready CSV files, creates four chart images, and writes `report/index.html`.

## Cleaning assumptions

- Revenue is calculated as `Quantity × UnitPrice` because product cost is not included; the project does not claim profit analysis.
- Cancelled invoice numbers, non-positive quantities, and non-positive unit prices are excluded from completed-sales analysis.
- Rows without `CustomerID` remain in transaction and product analysis but are excluded from customer segmentation.
- Product descriptions are standardized for grouping; exact stock codes remain unchanged.
- Customer value groups use an interpretable RFM-style method based on recency, order frequency, and revenue.

## Portfolio framing

Suggested role wording: **Business / Data Analyst — independent portfolio project**. Replace this later if the work becomes part of a class, internship, or team project.
