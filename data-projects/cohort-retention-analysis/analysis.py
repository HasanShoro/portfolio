from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parent
RAW_PATH = ROOT / "data" / "raw" / "subscription-history.csv"
PROCESSED_DIR = ROOT / "data" / "processed"
CHART_DIR = ROOT / "charts"
REPORT_DIR = ROOT / "report"
NOTEBOOK_DIR = ROOT / "notebooks"

INK = "#15191d"
MUTED = "#6b747b"
ACCENT = "#7a3042"
WARM = "#e47b55"
PALE = "#f5ebe7"


def month_difference(later: pd.Series, earlier: pd.Series) -> pd.Series:
    return (later.dt.year - earlier.dt.year) * 12 + later.dt.month - earlier.dt.month


def save_figure(path: Path) -> None:
    plt.savefig(path, dpi=180, bbox_inches="tight", facecolor="white")
    plt.close()


def build_notebook() -> None:
    notebook = {
        "cells": [
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "# Subscription Cohort Retention Analysis\n",
                    "This notebook reproduces the cleaned exports, cohort tables, charts, and HTML case study from the local Microsoft sample dataset.\n",
                ],
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "from pathlib import Path\n",
                    "import sys\n",
                    "project_root = Path.cwd().parent if Path.cwd().name == 'notebooks' else Path.cwd()\n",
                    "sys.path.insert(0, str(project_root))\n",
                    "import analysis\n",
                    "analysis.main()\n",
                ],
            },
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "## Outputs\n",
                    "Open `../report/index.html` for the narrative case study and `../charts/` for exported visuals. Analysis-ready CSV files are in `../data/processed/`.\n",
                ],
            },
        ],
        "metadata": {
            "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
            "language_info": {"name": "python", "version": "3"},
        },
        "nbformat": 4,
        "nbformat_minor": 5,
    }
    NOTEBOOK_DIR.mkdir(parents=True, exist_ok=True)
    (NOTEBOOK_DIR / "cohort-retention-analysis.ipynb").write_text(json.dumps(notebook, indent=2))


def write_report(metrics: dict[str, object], driver_rows: list[dict[str, object]]) -> None:
    driver_html = "".join(
        f"<tr><td>{row['segment']}</td><td>{int(row['customers']):,}</td><td>{row['retention_6m']:.1%}</td><td>{row['retention_12m']:.1%}</td></tr>"
        for row in driver_rows
    )
    html = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Subscription Cohort Retention Analysis</title>
<style>
:root{{--ink:#15191d;--muted:#6b747b;--paper:#f7f8f6;--surface:#fff;--accent:#7a3042;--warm:#e47b55;--line:#dfe3e5;}}
*{{box-sizing:border-box}} body{{margin:0;color:var(--ink);background:var(--paper);font-family:Inter,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;line-height:1.65}} .wrap{{width:min(1120px,calc(100% - 40px));margin:auto}}
header{{padding:90px 0 70px;background:linear-gradient(135deg,#2a1c2d,#6f2d3d 55%,#e47b55);color:white}} .tag{{font-size:.75rem;font-weight:800;letter-spacing:.13em;text-transform:uppercase}} h1{{max-width:900px;margin:18px 0;font-size:clamp(3rem,7vw,6rem);line-height:.95;letter-spacing:-.065em}} .lede{{max-width:760px;color:rgba(255,255,255,.78);font-size:1.15rem}}
section{{padding:74px 0;border-bottom:1px solid var(--line)}} h2{{font-size:clamp(2rem,4vw,3.6rem);line-height:1;letter-spacing:-.05em}} h3{{margin-bottom:8px}} .metrics{{display:grid;grid-template-columns:repeat(4,1fr);gap:14px;margin-top:-38px}} .metric{{padding:25px;border:1px solid var(--line);border-radius:20px;background:white;box-shadow:0 18px 55px rgba(20,23,25,.08)}} .metric strong{{display:block;font-size:2rem;letter-spacing:-.05em}} .metric span,.muted{{color:var(--muted)}}
.grid{{display:grid;grid-template-columns:repeat(2,1fr);gap:24px}} .card{{padding:28px;border:1px solid var(--line);border-radius:22px;background:white}} img{{width:100%;border:1px solid var(--line);border-radius:22px;background:white}} table{{width:100%;border-collapse:collapse;background:white}} th,td{{padding:14px;border-bottom:1px solid var(--line);text-align:left}} th{{font-size:.72rem;letter-spacing:.1em;text-transform:uppercase;color:var(--accent)}} .recommendations{{display:grid;grid-template-columns:repeat(3,1fr);gap:18px}} .rec{{padding:26px;border-radius:20px;background:#15191d;color:white}} .rec p{{color:#cbd0d3}} .source{{padding:24px;border-left:5px solid var(--warm);background:white}} a{{color:var(--accent)}} footer{{padding:38px 0 55px;color:var(--muted)}}
@media(max-width:760px){{.metrics,.grid,.recommendations{{grid-template-columns:1fr}}.metrics{{margin-top:20px}}header{{padding:64px 0 50px}}section{{padding:54px 0}}}}
.grid>img{{grid-column:1/-1}}</style></head><body><nav style="max-width:1120px;margin:0 auto;padding:16px 24px;font:600 14px/1.4 Inter,-apple-system,sans-serif"><a href="../../../index.html#work" style="color:inherit;text-decoration:none">← Back to portfolio</a></nav>
<header><div class="wrap"><span class="tag">Product Analytics · Cohort Retention</span><h1>When do subscribers stay — or disappear?</h1><p class="lede">A cohort analysis of {metrics['transactions']:,} subscription transactions, tracking repeat activity over twelve months and identifying practical retention levers.</p></div></header>
<main><section><div class="wrap"><div class="metrics"><div class="metric"><strong>{metrics['customers']:,}</strong><span>Subscribers</span></div><div class="metric"><strong>{metrics['retention_6m']:.1%}</strong><span>Month 6 retention</span></div><div class="metric"><strong>{metrics['retention_12m']:.1%}</strong><span>Month 12 retention</span></div><div class="metric"><strong>{metrics['auto_renew_lift']:+.1f} pts</strong><span>Auto-renew lift at 6M</span></div></div></div></section>
<section><div class="wrap grid"><div><p class="tag muted">Business question</p><h2>Where does retention weaken?</h2><p>Subscription growth is only durable when customers continue paying after acquisition. This project measures monthly repeat activity, compares acquisition cohorts, and tests whether auto-renew and starting price relate to longer customer lifetimes.</p></div><div class="card"><h3>Approach</h3><ul><li>Standardized transaction and subscription dates.</li><li>Collapsed duplicate activity to one customer-month record.</li><li>Assigned each customer to their first active month.</li><li>Calculated month-index retention for the first 12 months.</li><li>Compared retention by initial auto-renew status and price band.</li></ul></div></div></section>
<section><div class="wrap"><p class="tag muted">Retention curve</p><h2>The steepest loss happens early.</h2><img src="../charts/retention-curve.png" alt="Twelve month subscriber retention curve by auto-renew status"></div></section>
<section><div class="wrap"><p class="tag muted">Cohort view</p><h2>Newer cohorts repeat the same early drop.</h2><img src="../charts/cohort-heatmap.png" alt="Cohort retention heatmap"></div></section>
<section><div class="wrap grid"><div><p class="tag muted">Key findings</p><h2>Retention is an onboarding problem first.</h2><div class="card"><h3>Auto-renew is the clearest lever</h3><p>Customers starting on auto-renew show a {metrics['auto_renew_lift']:.1f}-point advantage at month 6. This is an association, not proof of causation, but it is large enough to prioritize in experiments.</p></div><div class="card"><h3>Value compounds with longevity</h3><p>The median retained subscriber contributes {metrics['retained_value_ratio']:.1f}× the observed revenue of a subscriber who leaves before month 6.</p></div></div><img src="../charts/retention-drivers.png" alt="Six and twelve month retention by customer segment"></div></section>
<section><div class="wrap"><p class="tag muted">Segment table</p><h2>Retention drivers at a glance.</h2><table><thead><tr><th>Segment</th><th>Customers</th><th>6M retention</th><th>12M retention</th></tr></thead><tbody>{driver_html}</tbody></table></div></section>
<section><div class="wrap"><p class="tag muted">Recommendations</p><h2>Turn retention insight into product action.</h2><div class="recommendations"><div class="rec"><h3>01 · Improve first 90 days</h3><p>Trigger onboarding nudges, setup checklists, and success milestones before the early retention curve flattens.</p></div><div class="rec"><h3>02 · Test auto-renew prompts</h3><p>Offer a transparent auto-renew default or incentive, then measure incremental retention with a randomized test.</p></div><div class="rec"><h3>03 · Watch cohorts monthly</h3><p>Make the heatmap a recurring operating metric and annotate product, pricing, and lifecycle-message changes.</p></div></div></div></section>
<section><div class="wrap"><div class="source"><h3>Dataset and limitations</h3><p>Source: Microsoft Learn customer analytics sample data, downloaded July 21, 2026. The file is a demonstration dataset rather than audited production records. Monthly activity is treated as retention; gaps can represent pauses, delayed billing, or data-generation behavior. Auto-renew findings are observational and should be validated experimentally.</p><p><a href="https://learn.microsoft.com/en-us/dynamics365/customer-insights/data/predict-subscription-churn">Microsoft Learn source documentation</a></p></div></div></section></main>
<footer><div class="wrap">Independent portfolio project · Python · pandas · Matplotlib</div></footer></body></html>"""
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    (REPORT_DIR / "index.html").write_text(html)


def main() -> None:
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    CHART_DIR.mkdir(parents=True, exist_ok=True)
    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    raw = pd.read_csv(RAW_PATH)
    date_format = "%m/%d/%Y %I:%M:%S %p"
    for column in ["SubscriptionStartDate", "SubscriptionEndDate", "TransactionDate"]:
        raw[column] = pd.to_datetime(raw[column], format=date_format, errors="coerce")
    raw["SubscriptionAmount"] = pd.to_numeric(raw["SubscriptionAmount"], errors="coerce")
    raw["is_auto_renew"] = raw["is_auto_renew"].astype(str).str.lower().eq("true")
    raw = raw.dropna(subset=["CustomerID", "TransactionDate", "SubscriptionAmount"]).copy()
    raw = raw[raw["SubscriptionAmount"] >= 0].copy()
    raw["activity_month"] = raw["TransactionDate"].dt.to_period("M").dt.to_timestamp()
    raw.to_csv(PROCESSED_DIR / "clean_subscription_history.csv", index=False)

    monthly = (
        raw.sort_values("TransactionDate")
        .groupby(["CustomerID", "activity_month"], as_index=False)
        .agg(
            monthly_revenue=("SubscriptionAmount", "sum"),
            auto_renew=("is_auto_renew", "max"),
            subscription_id=("SubscriptionID", "first"),
        )
    )
    first_month = monthly.groupby("CustomerID")["activity_month"].transform("min")
    monthly["cohort_month"] = first_month
    monthly["month_index"] = month_difference(monthly["activity_month"], monthly["cohort_month"]).astype(int)
    monthly.to_csv(PROCESSED_DIR / "customer_month_activity.csv", index=False)

    cohort_sizes = monthly[monthly["month_index"] == 0].groupby("cohort_month")["CustomerID"].nunique()
    cohort_counts = monthly[monthly["month_index"].between(0, 12)].pivot_table(
        index="cohort_month", columns="month_index", values="CustomerID", aggfunc="nunique"
    )
    retention = cohort_counts.div(cohort_sizes, axis=0).reindex(columns=range(13))
    retention.index = retention.index.strftime("%b %Y")
    retention.to_csv(PROCESSED_DIR / "cohort_retention.csv")

    customer_first = monthly.sort_values("activity_month").groupby("CustomerID").first()
    customer_summary = monthly.groupby("CustomerID").agg(
        first_month=("activity_month", "min"),
        last_month=("activity_month", "max"),
        active_months=("activity_month", "nunique"),
        observed_revenue=("monthly_revenue", "sum"),
        max_month_index=("month_index", "max"),
    )
    customer_summary["initial_auto_renew"] = customer_first["auto_renew"]
    customer_summary["initial_amount"] = customer_first["monthly_revenue"]
    customer_summary["retained_6m"] = customer_summary["max_month_index"] >= 5
    customer_summary["retained_12m"] = customer_summary["max_month_index"] >= 11
    customer_summary["price_band"] = pd.qcut(
        customer_summary["initial_amount"].rank(method="first"), 4, labels=["Entry", "Lower-mid", "Upper-mid", "Premium"]
    )
    customer_summary.to_csv(PROCESSED_DIR / "customer_retention_summary.csv")

    overall_curve = monthly[monthly["month_index"].between(0, 12)].groupby("month_index")["CustomerID"].nunique()
    overall_curve = overall_curve / monthly[monthly["month_index"] == 0]["CustomerID"].nunique()
    curve_rows = []
    for auto_renew, customer_ids in customer_summary.groupby("initial_auto_renew").groups.items():
        subset = monthly[monthly["CustomerID"].isin(customer_ids) & monthly["month_index"].between(0, 12)]
        denominator = len(customer_ids)
        curve = subset.groupby("month_index")["CustomerID"].nunique().reindex(range(13), fill_value=0) / denominator
        for month_index, value in curve.items():
            curve_rows.append({"segment": "Auto-renew" if auto_renew else "Manual renewal", "month_index": month_index, "retention": value})
    curves = pd.DataFrame(curve_rows)
    curves.to_csv(PROCESSED_DIR / "retention_curves.csv", index=False)

    plt.figure(figsize=(10, 5.6))
    plt.plot(overall_curve.index, overall_curve.values, color=INK, linewidth=3, marker="o", label="All subscribers")
    for label, group in curves.groupby("segment"):
        color = ACCENT if label == "Auto-renew" else WARM
        plt.plot(group["month_index"], group["retention"], linewidth=2.5, marker="o", label=label, color=color)
    plt.title("Subscriber retention falls fastest in the first six months", loc="left", fontsize=17, fontweight="bold")
    plt.xlabel("Months since first subscription activity")
    plt.ylabel("Retained customers")
    plt.gca().yaxis.set_major_formatter(lambda value, _: f"{value:.0%}")
    plt.xticks(range(13))
    plt.ylim(0, 1.03)
    plt.grid(axis="y", alpha=.18)
    plt.legend(frameon=False)
    save_figure(CHART_DIR / "retention-curve.png")

    heatmap_data = retention.loc[cohort_sizes[cohort_sizes >= 30].index.strftime("%b %Y")].tail(14)
    fig, ax = plt.subplots(figsize=(12, 7))
    image = ax.imshow(heatmap_data.values, aspect="auto", cmap="RdPu", vmin=0, vmax=1)
    ax.set_title("Monthly retention by acquisition cohort", loc="left", fontsize=17, fontweight="bold", pad=16)
    ax.set_xlabel("Months since first activity")
    ax.set_ylabel("Acquisition cohort")
    ax.set_xticks(range(13), labels=range(13))
    ax.set_yticks(range(len(heatmap_data.index)), labels=heatmap_data.index)
    for row_index in range(heatmap_data.shape[0]):
        for column_index in range(heatmap_data.shape[1]):
            value = heatmap_data.iloc[row_index, column_index]
            if pd.notna(value):
                ax.text(column_index, row_index, f"{value:.0%}", ha="center", va="center", fontsize=8, color="white" if value > .55 else INK)
    fig.colorbar(image, ax=ax, fraction=.025, pad=.02, label="Retention")
    fig.tight_layout()
    save_figure(CHART_DIR / "cohort-heatmap.png")

    driver_frames = []
    auto_driver = customer_summary.groupby("initial_auto_renew").agg(
        customers=("active_months", "size"), retention_6m=("retained_6m", "mean"), retention_12m=("retained_12m", "mean")
    )
    for key, row in auto_driver.iterrows():
        driver_frames.append({"segment": "Auto-renew" if key else "Manual renewal", **row.to_dict()})
    price_driver = customer_summary.groupby("price_band", observed=False).agg(
        customers=("active_months", "size"), retention_6m=("retained_6m", "mean"), retention_12m=("retained_12m", "mean")
    )
    for key, row in price_driver.iterrows():
        driver_frames.append({"segment": f"{key} starting price", **row.to_dict()})
    drivers = pd.DataFrame(driver_frames)
    drivers.to_csv(PROCESSED_DIR / "retention_drivers.csv", index=False)

    plot_drivers = drivers.set_index("segment")[["retention_6m", "retention_12m"]]
    ax = plot_drivers.plot(kind="barh", figsize=(10, 6), color=[ACCENT, WARM], width=.72)
    ax.set_title("Auto-renew is the strongest observed retention signal", loc="left", fontsize=17, fontweight="bold")
    ax.set_xlabel("Retention rate")
    ax.set_ylabel("")
    ax.xaxis.set_major_formatter(lambda value, _: f"{value:.0%}")
    ax.grid(axis="x", alpha=.18)
    ax.legend(["Month 6", "Month 12"], frameon=False)
    plt.tight_layout()
    save_figure(CHART_DIR / "retention-drivers.png")

    retention_6m = float(customer_summary["retained_6m"].mean())
    retention_12m = float(customer_summary["retained_12m"].mean())
    auto_rates = customer_summary.groupby("initial_auto_renew")["retained_6m"].mean()
    auto_lift = float((auto_rates.get(True, np.nan) - auto_rates.get(False, np.nan)) * 100)
    retained_revenue = customer_summary.loc[customer_summary["retained_6m"] & (customer_summary["observed_revenue"] > 0), "observed_revenue"]
    early_revenue = customer_summary.loc[~customer_summary["retained_6m"] & (customer_summary["observed_revenue"] > 0), "observed_revenue"]
    retained_median = retained_revenue.median()
    early_median = early_revenue.median()
    retained_value_ratio = float(retained_median / early_median) if early_median else 0
    metrics = {
        "transactions": len(raw),
        "customers": customer_summary.shape[0],
        "retention_6m": retention_6m,
        "retention_12m": retention_12m,
        "auto_renew_lift": auto_lift,
        "retained_value_ratio": retained_value_ratio,
    }
    (PROCESSED_DIR / "summary_metrics.json").write_text(json.dumps(metrics, indent=2))
    write_report(metrics, drivers.to_dict("records"))
    build_notebook()
    print(json.dumps(metrics, indent=2))


if __name__ == "__main__":
    main()
