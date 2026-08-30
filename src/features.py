from __future__ import annotations

import pandas as pd


def sector_group(sector: str) -> str:
    """Map granular source-coded sectors into broad portfolio-analysis groups.

    This is an analyst-derived convenience feature. The original `sector` field
    is preserved in the raw dataset and should remain the source of truth.
    """
    s = str(sector).lower()

    if any(k in s for k in ["fmcg", "food", "beverage", "qsr", "dairy", "snacks", "confectionery"]):
        return "FMCG / Food & Beverage"
    if any(k in s for k in ["beauty", "personal care", "skincare", "grooming"]):
        return "Beauty & Personal Care"
    if any(k in s for k in ["bank", "fintech", "insurance", "financial", "mutual fund", "venture capital"]):
        return "Financial Services"
    if any(k in s for k in ["quick commerce", "e-commerce", "retail", "commerce"]):
        return "Retail & Commerce"
    if any(k in s for k in ["technology", "adtech", "enterprise", "ai", "consumer electronics"]):
        return "Technology & Electronics"
    if any(k in s for k in ["automotive", "mobility", "electric mobility", "auto marketplace"]):
        return "Automotive & Mobility"
    if any(k in s for k in ["media", "streaming", "entertainment", "news"]):
        return "Media & Entertainment"
    if any(k in s for k in ["fashion", "home", "interior", "textile", "furniture", "jewellery", "stationery", "lifestyle", "building materials", "kitchenware"]):
        return "Lifestyle, Home & Fashion"
    if any(k in s for k in ["health", "pharma"]):
        return "Healthcare"
    if any(k in s for k in ["travel", "hospitality"]):
        return "Travel & Hospitality"
    if any(k in s for k in ["sport", "culture", "education"]):
        return "Sports, Culture & Education"
    if any(k in s for k in ["renewable", "energy"]):
        return "Energy & Sustainability"

    return "Other"


def standardize_marketing_role(stage: str) -> str:
    """Convert the original mixed funnel coding into comparable marketing roles.

    The raw `funnel_stage` field is preserved. This derived variable avoids
    treating strategic activities such as agency mandates as consumer funnel
    stages.
    """

    mapping = {
        "Awareness": "Awareness",
        "Consideration": "Consideration",
        "B2B Consideration": "Consideration",
        "Conversion": "Conversion / Acquisition",
        "Acquisition": "Conversion / Acquisition",
        "Engagement": "Engagement",
        "Retention": "Retention",
        "Strategy": "Strategic Enabler",
        "Performance": "Other / Review",
    }

    return mapping.get(str(stage), "Other / Review")


def enrich(df: pd.DataFrame) -> pd.DataFrame:
    """Add reproducible, explicitly derived analytical features."""

    out = df.copy()

    out["reported_date"] = pd.to_datetime(
        out["reported_date"],
        errors="coerce"
    )

    out["sector_group"] = out["sector"].map(sector_group)

    out["reported_month"] = (
        out["reported_date"]
        .dt.to_period("M")
        .astype(str)
    )

    # Preserve the original funnel_stage and create a standardized role.
    out["marketing_role"] = (
        out["funnel_stage"]
        .map(standardize_marketing_role)
    )

    # ICG-024 is a B2B demonstration campaign designed to generate advertiser
    # consideration, so it is manually standardized to Consideration.
    out.loc[
        out["record_id"].eq("ICG-024"),
        "marketing_role"
    ] = "Consideration"

    out["lower_funnel_flag"] = (
        out["marketing_role"]
        .isin(["Conversion / Acquisition", "Retention"])
        .astype(int)
    )

    out["talent_label"] = out["talent_used"].map(
        {
            1: "Named talent used",
            0: "No named talent stated"
        }
    )

    out["occasion_label"] = out["occasion_flag"].map(
        {
            1: "Occasion-linked",
            0: "Not occasion-linked"
        }
    )

    return out
