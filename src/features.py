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


def enrich(df: pd.DataFrame) -> pd.DataFrame:
    """Add reproducible, explicitly derived analytical features."""
    out = df.copy()
    out["reported_date"] = pd.to_datetime(out["reported_date"], errors="coerce")
    out["sector_group"] = out["sector"].map(sector_group)
    out["reported_month"] = out["reported_date"].dt.to_period("M").astype(str)
    out["lower_funnel_flag"] = out["funnel_stage"].isin(
        ["Acquisition", "Conversion", "Performance", "Retention"]
    ).astype(int)
    out["talent_label"] = out["talent_used"].map({1: "Named talent used", 0: "No named talent stated"})
    out["occasion_label"] = out["occasion_flag"].map({1: "Occasion-linked", 0: "Not occasion-linked"})
    return out
