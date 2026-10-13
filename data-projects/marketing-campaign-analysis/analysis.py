from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parent
RAW_PATH = ROOT / "data" / "raw" / "bank-additional" / "bank-additional" / "bank-additional-full.csv"
PROCESSED_DIR = ROOT / "data" / "processed"
CHART_DIR = ROOT / "charts"
REPORT_DIR = ROOT / "report"
NOTEBOOK_DIR = ROOT / "notebooks"

INK = "#15191d"
ACCENT = "#7a3042"
WARM = "#e47b55"
GOLD = "#d8a34a"
CHANNEL_COST = {"cellular": 2.50, "telephone": 5.00}
CONVERSION_VALUE = 240.00


def save_figure(path: Path) -> None:
    plt.savefig(path, dpi=180, bbox_inches="tight", facecolor="white")
    plt.close()


def build_notebook() -> None:
    notebook = {
        "cells": [
            {"cell_type": "markdown", "metadata": {}, "source": ["# Marketing Campaign Performance Analysis\n", "Reproduce the campaign cleaning, funnel, channel ROI scenario, segment analysis, charts, and HTML report.\n"]},
            {"cell_type": "code", "execution_count": None, "metadata": {}, "outputs": [], "source": ["from pathlib import Path\n", "import sys\n", "project_root = Path.cwd().parent if Path.cwd().name == 'notebooks' else Path.cwd()\n", "sys.path.insert(0, str(project_root))\n", "import analysis\n", "analysis.main()\n"]},
            {"cell_type": "markdown", "metadata": {}, "source": ["## Outputs\n", "Open `../report/index.html` for the case study. Exported visuals are in `../charts/` and analysis-ready tables are in `../data/processed/`.\n"]},
        ],
        "metadata": {"kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"}, "language_info": {"name": "python", "version": "3"}},
        "nbformat": 4,
        "nbformat_minor": 5,
    }
    NOTEBOOK_DIR.mkdir(parents=True, exist_ok=True)
    (NOTEBOOK_DIR / "marketing-campaign-analysis.ipynb").write_text(json.dumps(notebook, indent=2))


def write_report(metrics: dict[str, object], channel_rows: list[dict[str, object]]) -> None:
    channel_html = "".join(
        f"<tr><td>{row['channel'].title()}</td><td>{int(row['contacts']):,}</td><td>{int(row['conversions']):,}</td><td>{row['conversion_rate']:.1%}</td><td>{row['roi']:.1f}×</td><td>{row['recommended_budget_share']:.0%}</td></tr>"
        for row in channel_rows
    )
    html = f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Marketing Campaign Performance Analysis</title>
<style>:root{{--ink:#15191d;--muted:#6b747b;--paper:#f7f8f6;--surface:#fff;--accent:#7a3042;--warm:#e47b55;--line:#dfe3e5}}*{{box-sizing:border-box}}body{{margin:0;color:var(--ink);background:var(--paper);font-family:Inter,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;line-height:1.65}}.wrap{{width:min(1120px,calc(100% - 40px));margin:auto}}header{{padding:90px 0 70px;background:linear-gradient(135deg,#2a1c2d,#6f2d3d 55%,#e47b55);color:white}}.tag{{font-size:.75rem;font-weight:800;letter-spacing:.13em;text-transform:uppercase}}h1{{max-width:930px;margin:18px 0;font-size:clamp(3rem,7vw,6rem);line-height:.95;letter-spacing:-.065em}}.lede{{max-width:780px;color:rgba(255,255,255,.78);font-size:1.15rem}}section{{padding:74px 0;border-bottom:1px solid var(--line)}}h2{{font-size:clamp(2rem,4vw,3.6rem);line-height:1;letter-spacing:-.05em}}.metrics{{display:grid;grid-template-columns:repeat(4,1fr);gap:14px;margin-top:-38px}}.metric{{padding:25px;border:1px solid var(--line);border-radius:20px;background:white;box-shadow:0 18px 55px rgba(20,23,25,.08)}}.metric strong{{display:block;font-size:2rem;letter-spacing:-.05em}}.metric span,.muted{{color:var(--muted)}}.grid{{display:grid;grid-template-columns:repeat(2,1fr);gap:24px}}.card{{padding:28px;border:1px solid var(--line);border-radius:22px;background:white}}img{{width:100%;border:1px solid var(--line);border-radius:22px;background:white}}table{{width:100%;border-collapse:collapse;background:white}}th,td{{padding:14px;border-bottom:1px solid var(--line);text-align:left}}th{{font-size:.72rem;letter-spacing:.1em;text-transform:uppercase;color:var(--accent)}}.recommendations{{display:grid;grid-template-columns:repeat(3,1fr);gap:18px}}.rec{{padding:26px;border-radius:20px;background:#15191d;color:white}}.rec p{{color:#cbd0d3}}.source{{padding:24px;border-left:5px solid var(--warm);background:white}}a{{color:var(--accent)}}footer{{padding:38px 0 55px;color:var(--muted)}}@media(max-width:760px){{.metrics,.grid,.recommendations{{grid-template-columns:1fr}}.metrics{{margin-top:20px}}header{{padding:64px 0 50px}}section{{padding:54px 0}}}}.grid>img{{grid-column:1/-1}}</style></head><body><nav style="max-width:1120px;margin:0 auto;padding:16px 24px;font:600 14px/1.4 Inter,-apple-system,sans-serif"><a href="../../../index.html#work" style="color:inherit;text-decoration:none">← Back to portfolio</a></nav>
<header><div class="wrap"><span class="tag">Marketing Analytics · Campaign ROI</span><h1>Which audience and channel deserve the next dollar?</h1><p class="lede">An analysis of {metrics['contacts']:,} outbound campaign contacts, combining conversion, channel efficiency, segment response, and a transparent ROI scenario.</p></div></header><main>
<section><div class="wrap"><div class="metrics"><div class="metric"><strong>{metrics['contacts']:,}</strong><span>Contacts</span></div><div class="metric"><strong>{metrics['conversions']:,}</strong><span>Conversions</span></div><div class="metric"><strong>{metrics['conversion_rate']:.1%}</strong><span>Conversion rate</span></div><div class="metric"><strong>{metrics['modeled_roi']:.1f}×</strong><span>Modeled ROI</span></div></div></div></section>
<section><div class="wrap grid"><div><p class="tag muted">Business question</p><h2>How should campaign budget be reallocated?</h2><p>The goal is to separate reach from productive engagement, compare cellular and telephone contact economics, and identify segments that convert without excessive repeated touches.</p></div><div class="card"><h3>Approach</h3><ul><li>Cleaned 41,188 public campaign records.</li><li>Built a duration-based engagement funnel.</li><li>Compared conversion by contact channel, job, and age.</li><li>Modeled spend using explicit per-contact cost assumptions.</li><li>Translated profit per contact into a budget allocation scenario.</li></ul></div></div></section>
<section><div class="wrap"><p class="tag muted">Conversion funnel</p><h2>Only a small share reaches a meaningful conversation.</h2><img src="../charts/conversion-funnel.png" alt="Campaign conversion funnel"></div></section>
<section><div class="wrap grid"><div><p class="tag muted">Channel economics</p><h2>Cellular combines scale with stronger efficiency.</h2><p>The ROI model assumes ${CONVERSION_VALUE:,.0f} contribution per conversion, ${CHANNEL_COST['cellular']:.2f} per cellular contact, and ${CHANNEL_COST['telephone']:.2f} per telephone contact. These are scenario inputs because the source data does not include media cost or customer lifetime value.</p><table><thead><tr><th>Channel</th><th>Contacts</th><th>Conversions</th><th>Rate</th><th>ROI</th><th>Budget</th></tr></thead><tbody>{channel_html}</tbody></table></div><img src="../charts/channel-performance.png" alt="Channel conversion and ROI comparison"></div></section>
<section><div class="wrap"><p class="tag muted">Audience segments</p><h2>Response varies sharply by customer profile.</h2><img src="../charts/segment-conversion.png" alt="Conversion rate by job segment"></div></section>
<section><div class="wrap"><p class="tag muted">Budget allocation</p><h2>Move spend toward profitable contact efficiency.</h2><img src="../charts/roi-allocation.png" alt="Modeled channel ROI and recommended budget allocation"></div></section>
<section><div class="wrap"><p class="tag muted">Recommendations</p><h2>Spend smarter before spending more.</h2><div class="recommendations"><div class="rec"><h3>01 · Prioritize cellular</h3><p>Use cellular as the default scalable channel while preserving a smaller telephone test budget for high-value segments.</p></div><div class="rec"><h3>02 · Suppress fatigue</h3><p>Conversion falls as repeated campaign contacts accumulate. Cap attempts and shift nonresponders into a slower nurture path.</p></div><div class="rec"><h3>03 · Test high-response segments</h3><p>Build controlled audience tests around the strongest job and age groups rather than applying broad targeting rules immediately.</p></div></div></div></section>
<section><div class="wrap"><div class="source"><h3>Dataset and limitations</h3><p>Source: UCI Machine Learning Repository, Bank Marketing dataset, downloaded July 21, 2026. The campaign ran from May 2008 to November 2010. Call duration strongly predicts conversion but is only known after a call, so it is used to describe the funnel—not as a pre-contact targeting feature. ROI is a planning scenario, not reported financial performance.</p><p><a href="https://archive.ics.uci.edu/dataset/222/bank+marketing">UCI dataset page</a> · <a href="https://doi.org/10.24432/C5K306">Dataset DOI</a></p></div></div></section></main><footer><div class="wrap">Independent portfolio project · Python · pandas · Matplotlib</div></footer></body></html>"""
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    (REPORT_DIR / "index.html").write_text(html)


def main() -> None:
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    CHART_DIR.mkdir(parents=True, exist_ok=True)
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    data = pd.read_csv(RAW_PATH, sep=";")
    data["converted"] = data["y"].eq("yes")
    data["age_band"] = pd.cut(data["age"], bins=[17, 29, 39, 49, 59, 120], labels=["18–29", "30–39", "40–49", "50–59", "60+"])
    data["contact_cost"] = data["contact"].map(CHANNEL_COST)
    data["modeled_value"] = data["converted"].astype(int) * CONVERSION_VALUE
    data["modeled_profit"] = data["modeled_value"] - data["contact_cost"]
    data.to_csv(PROCESSED_DIR / "clean_campaign_contacts.csv", index=False)

    funnel = pd.DataFrame({
        "stage": ["Contacts", "60s+ conversations", "180s+ conversations", "Conversions"],
        "count": [len(data), int((data["duration"] >= 60).sum()), int((data["duration"] >= 180).sum()), int(data["converted"].sum())],
    })
    funnel["share_of_contacts"] = funnel["count"] / len(data)
    funnel.to_csv(PROCESSED_DIR / "conversion_funnel.csv", index=False)

    plt.figure(figsize=(10, 5.8))
    colors = [INK, ACCENT, WARM, GOLD]
    bars = plt.barh(funnel["stage"][::-1], funnel["count"][::-1], color=colors[::-1])
    plt.title("Campaign reach narrows quickly into qualified conversations", loc="left", fontsize=17, fontweight="bold")
    plt.xlabel("Contacts")
    plt.grid(axis="x", alpha=.18)
    for bar, count, share in zip(bars, funnel["count"][::-1], funnel["share_of_contacts"][::-1]):
        plt.text(bar.get_width() + 500, bar.get_y() + bar.get_height()/2, f"{count:,} · {share:.1%}", va="center")
    plt.xlim(0, funnel["count"].max() * 1.22)
    plt.tight_layout()
    save_figure(CHART_DIR / "conversion-funnel.png")

    channel = data.groupby("contact").agg(contacts=("converted", "size"), conversions=("converted", "sum"), spend=("contact_cost", "sum"), value=("modeled_value", "sum"), profit=("modeled_profit", "sum"))
    channel["conversion_rate"] = channel["conversions"] / channel["contacts"]
    channel["roi"] = channel["profit"] / channel["spend"]
    positive_efficiency = (channel["profit"] / channel["contacts"]).clip(lower=0)
    channel["recommended_budget_share"] = positive_efficiency / positive_efficiency.sum()
    channel.index.name = "channel"
    channel.reset_index().to_csv(PROCESSED_DIR / "channel_performance.csv", index=False)

    fig, axes = plt.subplots(1, 2, figsize=(11, 5.6))
    channel["conversion_rate"].sort_values().plot(kind="barh", ax=axes[0], color=[WARM, ACCENT])
    axes[0].set_title("Conversion rate", loc="left", fontweight="bold")
    axes[0].xaxis.set_major_formatter(lambda value, _: f"{value:.0%}")
    axes[0].set_xlabel("")
    axes[0].set_ylabel("")
    channel["roi"].sort_values().plot(kind="barh", ax=axes[1], color=[WARM, ACCENT])
    axes[1].set_title("Modeled ROI", loc="left", fontweight="bold")
    axes[1].set_xlabel("Profit / spend")
    axes[1].set_ylabel("")
    for ax in axes:
        ax.grid(axis="x", alpha=.18)
    fig.suptitle("Cellular leads on conversion and modeled efficiency", x=.06, ha="left", fontsize=17, fontweight="bold")
    fig.tight_layout()
    save_figure(CHART_DIR / "channel-performance.png")

    segment = data.groupby("job").agg(contacts=("converted", "size"), conversions=("converted", "sum"))
    segment["conversion_rate"] = segment["conversions"] / segment["contacts"]
    segment = segment[segment["contacts"] >= 500].sort_values("conversion_rate")
    segment.to_csv(PROCESSED_DIR / "job_segment_performance.csv")
    plt.figure(figsize=(10, 6.2))
    plt.barh(segment.index, segment["conversion_rate"], color=np.where(segment["conversion_rate"] >= segment["conversion_rate"].median(), ACCENT, "#d8dcde"))
    plt.title("Student and retired audiences respond above average", loc="left", fontsize=17, fontweight="bold")
    plt.xlabel("Conversion rate")
    plt.ylabel("")
    plt.gca().xaxis.set_major_formatter(lambda value, _: f"{value:.0%}")
    plt.grid(axis="x", alpha=.18)
    plt.tight_layout()
    save_figure(CHART_DIR / "segment-conversion.png")

    fig, axes = plt.subplots(1, 2, figsize=(11, 5.6))
    channel["roi"].plot(kind="bar", ax=axes[0], color=[ACCENT, WARM], rot=0)
    axes[0].set_title("Modeled ROI by channel", loc="left", fontweight="bold")
    axes[0].set_ylabel("Profit / spend")
    channel["recommended_budget_share"].plot(kind="bar", ax=axes[1], color=[ACCENT, WARM], rot=0)
    axes[1].set_title("Recommended test budget", loc="left", fontweight="bold")
    axes[1].yaxis.set_major_formatter(lambda value, _: f"{value:.0%}")
    for ax in axes:
        ax.set_xlabel("")
        ax.grid(axis="y", alpha=.18)
    fig.suptitle("A transparent scenario favors cellular investment", x=.06, ha="left", fontsize=17, fontweight="bold")
    fig.tight_layout()
    save_figure(CHART_DIR / "roi-allocation.png")

    touches = data.assign(touch_band=pd.cut(data["campaign"], [0, 1, 2, 3, 5, 100], labels=["1", "2", "3", "4–5", "6+"])).groupby("touch_band", observed=False).agg(contacts=("converted", "size"), conversion_rate=("converted", "mean"))
    touches.to_csv(PROCESSED_DIR / "campaign_fatigue.csv")

    metrics = {
        "contacts": int(len(data)),
        "conversions": int(data["converted"].sum()),
        "conversion_rate": float(data["converted"].mean()),
        "modeled_roi": float(data["modeled_profit"].sum() / data["contact_cost"].sum()),
        "cellular_budget_share": float(channel.loc["cellular", "recommended_budget_share"]),
    }
    (PROCESSED_DIR / "summary_metrics.json").write_text(json.dumps(metrics, indent=2))
    write_report(metrics, channel.reset_index().to_dict("records"))
    build_notebook()
    print(json.dumps(metrics, indent=2))


if __name__ == "__main__":
    main()
