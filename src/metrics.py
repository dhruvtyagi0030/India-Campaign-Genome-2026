from __future__ import annotations

import math
import pandas as pd


def rate_by_group(df: pd.DataFrame, group: str, flag: str, min_n: int = 2) -> pd.DataFrame:
    """Return group-level count, positive count and rate for a binary flag."""
    result = (
        df.groupby(group, dropna=False)[flag]
          .agg(records="count", positives="sum", rate="mean")
          .reset_index()
    )
    return result[result["records"] >= min_n].sort_values(["rate", "records"], ascending=[False, False])


def channel_hhi(df: pd.DataFrame, group: str = "sector_group") -> pd.DataFrame:
    """Herfindahl-Hirschman Index of channel concentration for each group.

    HHI ranges from 0 to 1 in this implementation. Larger values indicate a
    more concentrated channel mix. Small group sizes should be interpreted cautiously.
    """
    rows = []
    for name, g in df.groupby(group):
        shares = g["primary_channel"].value_counts(normalize=True)
        rows.append({
            group: name,
            "records": len(g),
            "unique_channels": g["primary_channel"].nunique(),
            "channel_hhi": float((shares ** 2).sum()),
        })
    return pd.DataFrame(rows).sort_values(["channel_hhi", "records"], ascending=[False, False])


def creative_diversity(df: pd.DataFrame, group: str = "sector_group") -> pd.DataFrame:
    """Shannon entropy of the coded creative-strategy mix by group."""
    rows = []
    for name, g in df.groupby(group):
        shares = g["creative_strategy"].value_counts(normalize=True)
        entropy = -sum(float(p) * math.log(float(p), 2) for p in shares if p > 0)
        max_entropy = math.log(len(shares), 2) if len(shares) > 1 else 0.0
        normalized = entropy / max_entropy if max_entropy else 0.0
        rows.append({
            group: name,
            "records": len(g),
            "unique_strategies": g["creative_strategy"].nunique(),
            "creative_entropy_bits": entropy,
            "creative_diversity_normalized": normalized,
        })
    return pd.DataFrame(rows).sort_values(["creative_diversity_normalized", "records"], ascending=[False, False])
