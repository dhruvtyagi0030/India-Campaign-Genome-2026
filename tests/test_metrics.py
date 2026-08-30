import pandas as pd

from src.metrics import rate_by_group, channel_hhi, creative_diversity


def sample_df():
    return pd.DataFrame({
        "sector_group": ["A", "A", "A", "B", "B"],
        "talent_used": [1, 0, 1, 0, 0],
        "primary_channel": ["Digital", "Digital", "TV", "OOH", "OOH"],
        "creative_strategy": ["X", "Y", "Z", "Q", "Q"],
    })


def test_rate_by_group():
    out = rate_by_group(sample_df(), "sector_group", "talent_used", min_n=1).set_index("sector_group")
    assert out.loc["A", "records"] == 3
    assert abs(out.loc["A", "rate"] - (2/3)) < 1e-9
    assert out.loc["B", "rate"] == 0


def test_channel_hhi_is_bounded():
    out = channel_hhi(sample_df())
    assert out["channel_hhi"].between(0, 1).all()


def test_creative_diversity_is_bounded():
    out = creative_diversity(sample_df())
    assert out["creative_diversity_normalized"].between(0, 1).all()
