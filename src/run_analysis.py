from pathlib import Path
import sys
import pandas as pd
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.features import enrich
from src.metrics import rate_by_group, channel_hhi, creative_diversity

RAW = ROOT / "data" / "raw" / "india_campaign_genome_90d.csv"
PROCESSED = ROOT / "data" / "processed" / "campaign_genome_enriched.csv"
TABLES = ROOT / "outputs" / "tables"
FIGURES = ROOT / "outputs" / "figures"

TABLES.mkdir(parents=True, exist_ok=True)
FIGURES.mkdir(parents=True, exist_ok=True)


def save_bar(series: pd.Series, title: str, xlabel: str, filename: str, horizontal: bool = True):
    plt.figure(figsize=(10, 6))
    if horizontal:
        series.sort_values().plot(kind="barh")
        plt.xlabel(xlabel)
        plt.ylabel("")
    else:
        series.plot(kind="bar")
        plt.ylabel(xlabel)
        plt.xlabel("")
        plt.xticks(rotation=35, ha="right")
    plt.title(title)
    plt.tight_layout()
    plt.savefig(FIGURES / filename, dpi=180, bbox_inches="tight")
    plt.close()


def main():
    df = pd.read_csv(RAW)
    df = enrich(df)
    df.to_csv(PROCESSED, index=False)

    role_distribution = (
    df["marketing_role"]
    .value_counts()
    .rename_axis("marketing_role")
    .reset_index(name="records")
)

role_distribution.to_csv(
    TABLES / "marketing_role_distribution.csv",
    index=False
)

    talent = rate_by_group(df, "sector_group", "talent_used", min_n=3)
    talent.to_csv(TABLES / "celebrity_dependency_by_sector_group.csv", index=False)

    occasion = rate_by_group(df, "sector_group", "occasion_flag", min_n=3)
    occasion.to_csv(TABLES / "occasion_marketing_by_sector_group.csv", index=False)

    ai_data = rate_by_group(df, "sector_group", "ai_data_angle", min_n=3)
    ai_data.to_csv(TABLES / "ai_data_activation_by_sector_group.csv", index=False)

    hhi = channel_hhi(df)
    hhi.to_csv(TABLES / "channel_concentration_hhi.csv", index=False)

    diversity = creative_diversity(df)
    diversity.to_csv(TABLES / "creative_diversity.csv", index=False)

        save_bar(
    df["marketing_role"].value_counts(),
    "Observed Marketing Actions by Standardized Marketing Role",
    "Number of coded actions",
    "marketing_role_distribution.png",
)

    talent_series = talent.set_index("sector_group")["rate"].head(10)
    save_bar(
        talent_series,
        "Named-Talent Dependency by Broad Sector Group",
        "Share of observed actions using named talent",
        "celebrity_dependency.png",
    )

    month_occ = df.groupby("reported_month")["occasion_flag"].mean()
    save_bar(
        month_occ,
        "Occasion-Linked Share by Reported Month",
        "Share of observed actions",
        "occasion_share_by_month.png",
        horizontal=False,
    )

    ai_counts = (
        df[df["ai_data_angle"] == 1]["sector_group"]
        .value_counts()
        .head(10)
    )
    save_bar(
        ai_counts,
        "AI/Data-Led Marketing Actions by Broad Sector Group",
        "Number of coded actions",
        "ai_data_actions.png",
    )

    print("Analysis complete.")
    print(f"Processed dataset: {PROCESSED.relative_to(ROOT)}")
    print(f"Tables: {TABLES.relative_to(ROOT)}")
    print(f"Figures: {FIGURES.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
