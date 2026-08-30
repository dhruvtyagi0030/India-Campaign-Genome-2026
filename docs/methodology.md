# Methodology

## Research objective

The project asks how observable brand marketing actions in India are structured across **objectives, channels, celebrity/creator use, occasion marketing, regional localization, funnel stages, and AI/data-led execution**.

## Unit of analysis

One row represents one publicly reported marketing action, such as a campaign launch, ambassador partnership, branded-content activation, product/offer campaign, media mandate, experiential activation, or material marketing-strategy shift.

## Coverage

- **Reported-date window:** 1 June 2026 to 29 August 2026
- **Geographic focus:** India and India-relevant marketing activity
- **Current release:** 91 coded observations

## Reconstruction method

The dataset is a **retrospective public-source reconstruction**. Records were identified from marketing-industry archives and official brand/platform sources, then normalized into a common schema.

`reported_date` is the date on which the action was reported by the cited source. It should not automatically be interpreted as the exact campaign launch date.

## Analyst-coded fields

The following fields require judgement and therefore should not be treated as objective ground truth:

- `sector`
- `primary_objective`
- `primary_channel`
- `creative_strategy`
- `funnel_stage`
- `regional_localization`
- broad `sector_group` in the processed dataset

The raw source-oriented fields remain unchanged; derived features are generated reproducibly by code in `src/features.py`.

## Original analytical metrics

### Celebrity Dependency Rate

For a group `g`:

`named-talent actions in g / all observed actions in g`

### Occasion Marketing Rate

`occasion-linked actions / all observed actions`

### AI/Data Activation Rate

`actions where AI or data materially enters the activation / all observed actions`

### Channel Concentration HHI

For channel shares `s_i` inside a group:

`HHI = sum(s_i^2)`

Higher values mean the observed channel mix is more concentrated.

### Creative Diversity

Shannon entropy is calculated over the coded creative-strategy distribution. A normalized entropy score is also provided from 0 to 1.

## Reproducibility

Run:

```bash
python src/validate_data.py
python src/run_analysis.py
pytest -q
```

The scripts rebuild the processed dataset, summary tables, and repository figures from the raw CSV.
