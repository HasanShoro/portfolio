from __future__ import annotations

import html
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.ticker import FuncFormatter


ROOT = Path(__file__).resolve().parent
RAW_FILE = ROOT / "data" / "raw" / "Online Retail.xlsx"
PROCESSED_DIR = ROOT / "data" / "processed"
CHART_DIR = ROOT / "charts"
REPORT_DIR = ROOT / "report"

INK = "#15191d"
MUTED = "#6b747b"
ACID = "#7a3042"
ORANGE = "#e47b55"
GRID = "#dfe3e5"


def money(value: float) -> str:
    return f"£{value:,.0f}"


def compact_money(value: float, _position: int) -> str:
    if abs(value) >= 1_000_000:
        return f"£{value / 1_000_000:.1f}M"
    if abs(value) >= 1_000:
        return f"£{value / 1_000:.0f}K"
    return f"£{value:.0f}"


def chart_style() -> None:
    plt.rcParams.update(
        {
            "font.family": "sans-serif",
            "font.size": 11,
            "axes.titlesize": 17,
            "axes.titleweight": "bold",
            "axes.labelcolor": MUTED,
            "axes.edgecolor": GRID,
            "axes.facecolor": "white",
            "figure.facecolor": "white",
            "xtick.color": MUTED,
            "ytick.color": MUTED,
        }
    )


def save_chart(fig: plt.Figure, filename: str) -> None:
    fig.tight_layout()
    fig.savefig(CHART_DIR / filename, dpi=180, bbox_inches="tight", facecolor="white")
    plt.close(fig)


def load_and_clean() -> tuple[pd.DataFrame, dict[str, float | int | str]]:
    raw = pd.read_excel(RAW_FILE, engine="openpyxl")
    raw.columns = [column.strip() for column in raw.columns]
    raw["InvoiceDate"] = pd.to_datetime(raw["InvoiceDate"], errors="coerce")
    raw["Description"] = raw["Description"].fillna("Unknown product").astype(str).str.strip()
    raw["Country"] = raw["Country"].fillna("Unknown").astype(str).str.strip()
    raw["InvoiceNo"] = raw["InvoiceNo"].astype(str).str.strip()
    raw["StockCode"] = raw["StockCode"].astype(str).str.strip()

    cancelled = raw["InvoiceNo"].str.upper().str.startswith("C", na=False)
    valid_dates = raw["InvoiceDate"].notna()
    completed = raw.loc[
        (~cancelled) & valid_dates & (raw["Quantity"] > 0) & (raw["UnitPrice"] > 0)
    ].copy()
    completed["Revenue"] = completed["Quantity"] * completed["UnitPrice"]
    completed["OrderMonth"] = completed["InvoiceDate"].dt.to_period("M").astype(str)
    completed["CustomerID"] = completed["CustomerID"].astype("Int64")

    quality = {
        "raw_rows": len(raw),
        "clean_rows": len(completed),
        "cancelled_rows": int(cancelled.sum()),
        "invalid_sales_rows": int((~cancelled & ((raw["Quantity"] <= 0) | (raw["UnitPrice"] <= 0))).sum()),
        "missing_customer_rows": int(completed["CustomerID"].isna().sum()),
        "start_date": completed["InvoiceDate"].min().strftime("%B %d, %Y"),
        "end_date": completed["InvoiceDate"].max().strftime("%B %d, %Y"),
    }
    return completed, quality


def build_customer_segments(data: pd.DataFrame) -> pd.DataFrame:
    customer_data = data.dropna(subset=["CustomerID"]).copy()
    snapshot_date = customer_data["InvoiceDate"].max() + pd.Timedelta(days=1)
    rfm = customer_data.groupby("CustomerID").agg(
        last_purchase=("InvoiceDate", "max"),
        orders=("InvoiceNo", "nunique"),
        revenue=("Revenue", "sum"),
    )
    rfm["recency_days"] = (snapshot_date - rfm["last_purchase"]).dt.days

    recency_rank = rfm["recency_days"].rank(method="first", ascending=True, pct=True)
    frequency_rank = rfm["orders"].rank(method="first", ascending=False, pct=True)
    revenue_rank = rfm["revenue"].rank(method="first", ascending=False, pct=True)
    rfm["value_score"] = (
        0.35 * recency_rank + 0.25 * frequency_rank + 0.40 * revenue_rank
    )
    rfm["segment"] = pd.qcut(
        rfm["value_score"],
        q=[0, 0.10, 0.35, 0.70, 1.0],
        labels=["Champions", "Loyal", "Promising", "At risk / low value"],
        duplicates="drop",
    )
    return rfm.reset_index()


def build_charts(data: pd.DataFrame, customers: pd.DataFrame) -> dict[str, pd.DataFrame]:
    chart_style()

    monthly = data.groupby("OrderMonth", as_index=False)["Revenue"].sum()
    fig, axis = plt.subplots(figsize=(11, 5.4))
    axis.plot(monthly["OrderMonth"], monthly["Revenue"], color=INK, linewidth=2.8, marker="o", markersize=5)
    peak_index = monthly["Revenue"].idxmax()
    axis.scatter(monthly.loc[peak_index, "OrderMonth"], monthly.loc[peak_index, "Revenue"], color=ORANGE, s=90, zorder=3)
    axis.set_title("Revenue accelerates sharply in the holiday period", loc="left", pad=16)
    axis.set_ylabel("Completed sales revenue")
    axis.yaxis.set_major_formatter(FuncFormatter(compact_money))
    axis.grid(axis="y", color=GRID, alpha=0.65)
    axis.spines[["top", "right"]].set_visible(False)
    axis.tick_params(axis="x", rotation=45)
    save_chart(fig, "monthly-revenue.png")

    products = (
        data.loc[~data["StockCode"].isin(["POST", "DOT", "M", "BANK CHARGES"])]
        .groupby("Description", as_index=False)["Revenue"]
        .sum()
        .nlargest(10, "Revenue")
        .sort_values("Revenue")
    )
    fig, axis = plt.subplots(figsize=(10, 6.3))
    colors = [INK] * len(products)
    colors[-1] = ACID
    axis.barh(products["Description"].str.title(), products["Revenue"], color=colors)
    axis.set_title("A small group of gift products leads revenue", loc="left", pad=16)
    axis.set_xlabel("Completed sales revenue")
    axis.xaxis.set_major_formatter(FuncFormatter(compact_money))
    axis.grid(axis="x", color=GRID, alpha=0.6)
    axis.spines[["top", "right", "left"]].set_visible(False)
    save_chart(fig, "top-products.png")

    countries = (
        data.loc[data["Country"] != "United Kingdom"]
        .groupby("Country", as_index=False)["Revenue"]
        .sum()
        .nlargest(10, "Revenue")
        .sort_values("Revenue")
    )
    fig, axis = plt.subplots(figsize=(9.5, 6))
    colors = [INK] * len(countries)
    colors[-1] = ORANGE
    axis.barh(countries["Country"], countries["Revenue"], color=colors)
    axis.set_title("The Netherlands is the strongest market beyond the UK", loc="left", pad=16)
    axis.set_xlabel("Completed sales revenue")
    axis.xaxis.set_major_formatter(FuncFormatter(compact_money))
    axis.grid(axis="x", color=GRID, alpha=0.6)
    axis.spines[["top", "right", "left"]].set_visible(False)
    save_chart(fig, "international-markets.png")

    segment_summary = (
        customers.groupby("segment", observed=False)
        .agg(customers=("CustomerID", "count"), revenue=("revenue", "sum"))
        .reset_index()
    )
    segment_summary["revenue_share"] = segment_summary["revenue"] / segment_summary["revenue"].sum()
    fig, axis = plt.subplots(figsize=(9.5, 5.8))
    colors = [ACID, INK, "#7b8176", ORANGE]
    axis.bar(segment_summary["segment"].astype(str), segment_summary["revenue_share"] * 100, color=colors)
    axis.set_title("Customer value is concentrated in top segments", loc="left", pad=16)
    axis.set_ylabel("Share of identified-customer revenue")
    axis.set_ylim(0, max(segment_summary["revenue_share"] * 100) * 1.22)
    axis.grid(axis="y", color=GRID, alpha=0.6)
    axis.spines[["top", "right"]].set_visible(False)
    for index, value in enumerate(segment_summary["revenue_share"] * 100):
        axis.text(index, value + 1, f"{value:.1f}%", ha="center", fontweight="bold", color=INK)
    save_chart(fig, "customer-segments.png")

    return {"monthly": monthly, "products": products, "countries": countries, "segments": segment_summary}


def write_report(
    data: pd.DataFrame,
    customers: pd.DataFrame,
    quality: dict[str, float | int | str],
    summaries: dict[str, pd.DataFrame],
) -> None:
    total_revenue = data["Revenue"].sum()
    orders = data["InvoiceNo"].nunique()
    customers_count = data["CustomerID"].nunique()
    average_order = total_revenue / orders
    uk_share = data.loc[data["Country"] == "United Kingdom", "Revenue"].sum() / total_revenue
    peak_month_row = summaries["monthly"].loc[summaries["monthly"]["Revenue"].idxmax()]
    top_product = summaries["products"].iloc[-1]
    top_market = summaries["countries"].iloc[-1]
    champion_row = summaries["segments"].loc[summaries["segments"]["segment"].astype(str) == "Champions"].iloc[0]

    metrics = [
        ("Completed revenue", money(total_revenue)),
        ("Completed orders", f"{orders:,}"),
        ("Identified customers", f"{customers_count:,}"),
        ("Average order value", money(average_order)),
    ]
    metric_cards = "".join(
        f'<div class="metric"><span>{html.escape(label)}</span><strong>{html.escape(value)}</strong></div>'
        for label, value in metrics
    )

    report = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="Business analysis of the UCI Online Retail dataset by Hasan.">
  <title>Online Retail Performance Analysis — Hasan</title>
  <style>
    :root {{ --ink:#15191d; --muted:#6b747b; --paper:#f7f8f6; --acid:#f1dde2; --orange:#a8432a; --line:#dfe3e5; }}
    * {{ box-sizing:border-box; }}
    body {{ margin:0; color:var(--ink); background:var(--paper); font-family:Inter,ui-sans-serif,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif; line-height:1.65; }}
    a {{ color:inherit; text-decoration-thickness:1px; text-underline-offset:4px; }}
    .wrap {{ width:min(calc(100% - 40px),1080px); margin:auto; }}
    header {{ padding:80px 0 64px; background:linear-gradient(rgba(17,19,16,.035) 1px,transparent 1px),linear-gradient(90deg,rgba(17,19,16,.035) 1px,transparent 1px),white; background-size:48px 48px; border-bottom:1px solid var(--line); }}
    .tag {{ display:inline-block; margin-bottom:26px; padding:7px 12px; background:var(--acid); border-radius:99px; font-size:.75rem; font-weight:850; letter-spacing:.08em; text-transform:uppercase; }}
    h1 {{ max-width:900px; margin:0 0 24px; font-size:clamp(3rem,8vw,7rem); line-height:.9; letter-spacing:-.065em; }}
    .lede {{ max-width:760px; margin:0; color:var(--muted); font-size:clamp(1.05rem,2vw,1.35rem); }}
    .metrics {{ display:grid; grid-template-columns:repeat(4,1fr); gap:12px; margin-top:-30px; position:relative; }}
    .metric {{ padding:24px; background:white; border:1px solid var(--line); border-radius:18px; box-shadow:0 18px 50px rgba(17,19,16,.08); }}
    .metric span {{ display:block; color:var(--muted); font-size:.75rem; font-weight:800; letter-spacing:.05em; text-transform:uppercase; }}
    .metric strong {{ display:block; margin-top:8px; font-size:clamp(1.4rem,3vw,2rem); letter-spacing:-.04em; }}
    section {{ padding:72px 0; border-bottom:1px solid var(--line); }}
    .kicker {{ color:var(--orange); font-size:.78rem; font-weight:850; letter-spacing:.12em; text-transform:uppercase; }}
    h2 {{ max-width:820px; margin:8px 0 22px; font-size:clamp(2rem,4.8vw,4rem); line-height:1; letter-spacing:-.05em; }}
    h3 {{ margin:0 0 8px; font-size:1.35rem; }}
    p {{ max-width:800px; color:var(--muted); }}
    .finding-grid {{ display:grid; grid-template-columns:repeat(2,1fr); gap:18px; margin-top:34px; }}
    .finding {{ padding:25px; background:white; border:1px solid var(--line); border-radius:18px; }}
    .finding b {{ color:var(--ink); }}
    figure {{ margin:38px 0 0; padding:18px; background:white; border:1px solid var(--line); border-radius:22px; }}
    figure img {{ width:100%; display:block; border-radius:10px; }}
    figcaption {{ padding:10px 8px 0; color:var(--muted); font-size:.88rem; }}
    .recommendations {{ display:grid; grid-template-columns:repeat(3,1fr); gap:16px; margin-top:30px; counter-reset:item; }}
    .recommendation {{ padding:26px; background:var(--ink); color:white; border-radius:20px; }}
    .recommendation::before {{ counter-increment:item; content:"0" counter(item); display:block; margin-bottom:30px; color:var(--acid); font-weight:850; }}
    .recommendation p {{ color:#cdd1c8; }}
    .method {{ display:grid; grid-template-columns:.8fr 1.2fr; gap:50px; }}
    ul {{ padding-left:20px; color:var(--muted); }}
    .source-box {{ padding:26px; background:white; border-left:5px solid var(--orange); }}
    footer {{ padding:36px 0 55px; color:var(--muted); }}
    @media (max-width:760px) {{ .metrics,.finding-grid,.recommendations,.method {{ grid-template-columns:1fr; }} .metrics {{ margin-top:20px; }} header {{ padding:60px 0 45px; }} section {{ padding:54px 0; }} }}
  </style>
</head>
<body><nav style="max-width:1120px;margin:0 auto;padding:16px 24px;font:600 14px/1.4 Inter,-apple-system,sans-serif"><a href="../../../index.html#work" style="color:inherit;text-decoration:none">← Back to portfolio</a></nav>
  <header><div class="wrap"><span class="tag">Business + Data Analysis</span><h1>What drives online retail revenue?</h1><p class="lede">An independent analysis of 541,909 transaction records to identify revenue patterns, valuable customers, product leaders, and international growth opportunities.</p></div></header>
  <main>
    <div class="wrap metrics">{metric_cards}</div>
    <section><div class="wrap"><div class="kicker">01 · Business question</div><h2>Where should this retailer focus to grow efficiently?</h2><p>The analysis evaluates completed sales from {quality['start_date']} through {quality['end_date']}. Because the dataset contains selling prices but no product costs, the financial measure is revenue—not profit.</p><div class="finding-grid">
      <article class="finding"><h3>Seasonality</h3><p><b>{peak_month_row['OrderMonth']}</b> was the strongest month at <b>{money(peak_month_row['Revenue'])}</b>, highlighting the importance of holiday inventory and campaign readiness.</p></article>
      <article class="finding"><h3>Market concentration</h3><p>The UK generated <b>{uk_share:.1%}</b> of completed-sales revenue. Outside the home market, <b>{html.escape(str(top_market['Country']))}</b> led with <b>{money(top_market['Revenue'])}</b>.</p></article>
      <article class="finding"><h3>Product leadership</h3><p><b>{html.escape(str(top_product['Description']).title())}</b> was the highest-revenue merchandise item at <b>{money(top_product['Revenue'])}</b>.</p></article>
      <article class="finding"><h3>Customer concentration</h3><p>The top <b>{int(champion_row['customers']):,} customers</b> in the Champions segment produced <b>{champion_row['revenue_share']:.1%}</b> of identified-customer revenue.</p></article>
    </div></div></section>
    <section><div class="wrap"><div class="kicker">02 · Revenue pattern</div><h2>Demand peaks late in the year.</h2><p>Monthly revenue rises into autumn and reaches its high point in November 2011. Operations and marketing should prepare for the surge before Q4 begins.</p><figure><img src="../charts/monthly-revenue.png" alt="Line chart of monthly revenue"><figcaption>Completed sales only; cancellations and non-positive transaction values are excluded.</figcaption></figure></div></section>
    <section><div class="wrap"><div class="kicker">03 · Product mix</div><h2>Giftable products anchor the catalog.</h2><p>The leading products suggest a strong decorative-gift and homeware use case. High-revenue items deserve reliable stock coverage, but product concentration should be monitored.</p><figure><img src="../charts/top-products.png" alt="Horizontal bar chart of top products by revenue"><figcaption>Administrative stock codes such as postage and bank charges are omitted from the merchandise ranking.</figcaption></figure></div></section>
    <section><div class="wrap"><div class="kicker">04 · International growth</div><h2>Several European markets show traction.</h2><p>The UK dominates the business, while the Netherlands, Ireland, Germany, France, and Australia provide a practical shortlist for targeted international testing.</p><figure><img src="../charts/international-markets.png" alt="Horizontal bar chart of international markets by revenue"><figcaption>Top non-UK countries ranked by completed-sales revenue.</figcaption></figure></div></section>
    <section><div class="wrap"><div class="kicker">05 · Customer value</div><h2>Retention should be selective, not generic.</h2><p>An RFM-style segmentation ranks customers using recency, number of orders, and revenue. The result separates high-value Champions from promising and lower-value groups.</p><figure><img src="../charts/customer-segments.png" alt="Bar chart showing revenue share by customer segment"><figcaption>Customers without an identifier are excluded from segmentation but retained in transaction analysis.</figcaption></figure></div></section>
    <section><div class="wrap"><div class="kicker">06 · Recommendations</div><h2>Three actions connect the analysis to the business.</h2><div class="recommendations">
      <article class="recommendation"><h3>Plan Q4 earlier</h3><p>Set inventory, campaign, and fulfillment plans by late summer for the products that lead holiday revenue.</p></article>
      <article class="recommendation"><h3>Protect Champions</h3><p>Use early access, replenishment reminders, and personalized offers for the highest-value customer segment.</p></article>
      <article class="recommendation"><h3>Test focused expansion</h3><p>Run small localized campaigns in the strongest non-UK markets before investing in broad expansion.</p></article>
    </div></div></section>
    <section><div class="wrap method"><div><div class="kicker">07 · Method</div><h2>Clean, local, reproducible.</h2></div><div><ul>
      <li>Loaded {quality['raw_rows']:,} rows from the locally saved UCI workbook.</li>
      <li>Retained {quality['clean_rows']:,} completed positive-value sales rows.</li>
      <li>Removed {quality['cancelled_rows']:,} cancellation rows and {quality['invalid_sales_rows']:,} other non-positive sales rows.</li>
      <li>Kept {quality['missing_customer_rows']:,} valid sales rows without CustomerID for product and market analysis.</li>
      <li>Calculated revenue as Quantity × UnitPrice and exported cleaned CSV files.</li>
    </ul><div class="source-box"><b>Source and reuse</b><p>UCI Machine Learning Repository, Online Retail, DOI 10.24432/C5BW33. Licensed under CC BY 4.0. The original workbook, cleaned CSV, Python analysis, and charts are saved with this project.</p><a href="../README.md">Read the project notes and provenance</a></div></div></div></section>
  </main>
  <footer><div class="wrap">Independent portfolio project by Hasan · Business / Data Analyst</div></footer>
</body>
</html>"""
    (REPORT_DIR / "index.html").write_text(report, encoding="utf-8")


def main() -> None:
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    CHART_DIR.mkdir(parents=True, exist_ok=True)
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    data, quality = load_and_clean()
    customers = build_customer_segments(data)
    data.to_csv(PROCESSED_DIR / "clean_online_retail.csv", index=False)
    customers.to_csv(PROCESSED_DIR / "customer_segments.csv", index=False)
    summaries = build_charts(data, customers)
    write_report(data, customers, quality, summaries)
    print(f"Rows analyzed: {len(data):,}")
    print(f"Completed revenue: {money(data['Revenue'].sum())}")
    print(f"Report: {REPORT_DIR / 'index.html'}")


if __name__ == "__main__":
    main()
