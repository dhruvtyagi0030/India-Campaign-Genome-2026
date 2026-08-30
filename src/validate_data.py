from pathlib import Path
import sys
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "raw" / "india_campaign_genome_90d.csv"

REQUIRED_COLUMNS = {
    "record_id", "reported_date", "brand", "sector", "action_type",
    "campaign_or_action", "primary_objective", "occasion_context",
    "geography_focus", "celebrity_or_creator", "talent_used",
    "primary_channel", "creative_strategy", "ai_data_angle",
    "funnel_stage", "source_publication", "source_url",
    "coding_confidence", "occasion_flag", "regional_localization"
}


def main() -> int:
    df = pd.read_csv(DATA)
    problems = []

    missing = sorted(REQUIRED_COLUMNS - set(df.columns))
    if missing:
        problems.append(f"Missing required columns: {missing}")

    if df.empty:
        problems.append("Dataset is empty")

    if df["record_id"].duplicated().any():
        dupes = df.loc[df["record_id"].duplicated(), "record_id"].tolist()
        problems.append(f"Duplicate record_id values: {dupes}")

    dates = pd.to_datetime(df["reported_date"], errors="coerce")
    if dates.isna().any():
        problems.append(f"Invalid dates: {int(dates.isna().sum())}")

    for col in ["talent_used", "ai_data_angle", "occasion_flag", "regional_localization"]:
        invalid = sorted(set(df[col].dropna().unique()) - {0, 1})
        if invalid:
            problems.append(f"{col} contains non-binary values: {invalid}")

    if not df["source_url"].astype(str).str.startswith(("http://", "https://")).all():
        problems.append("At least one source_url is not an HTTP(S) URL")

    if problems:
        print("DATA VALIDATION FAILED")
        for p in problems:
            print(f"- {p}")
        return 1

    print("DATA VALIDATION PASSED")
    print(f"Rows: {len(df)}")
    print(f"Unique brands: {df['brand'].nunique()}")
    print(f"Date range: {dates.min().date()} to {dates.max().date()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
