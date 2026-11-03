# Project Publication and Reproducibility

**Public portfolio status:** Original Olist customer transactions have been processed and the verified results have been published as aggregate data and business-facing charts.

## For a business reviewer

Start at [README](README.md) or the [Management Brief](docs/09_management_brief.md). Those pages explain the problem, findings and practical business implications visually.

## For a technical reviewer

The [source provenance](data/processed/PROVENANCE.json) identifies the original Olist repository and commit. The project processed eight transactional CSVs using the provided Python scripts. Raw order or customer rows are **not** committed to the portfolio.

The [verified metrics](data/processed/kpi_summary.json), [monthly outcomes](data/processed/monthly_metrics.csv), [regional outcomes](data/processed/customer_region_summary.csv), [review comparison](data/processed/review_by_delivery.csv) and [category values](data/processed/category_summary.csv) are available for reconciliation.

[GitHub Actions pipeline](.github/workflows/load_real_olist_data.yml) fetches Olist's own public CSVs and verifies source aggregate consistency. [CI unit and aggregate tests](.github/workflows/validate.yml) run against published code/data.

The [Excel workbook](workbook/Olist_Order_Fulfilment_Intelligence.xlsx) currently remains the earlier seller-geography edition on GitHub. Its binary has not yet been refreshed; use the published source-based visual report for the complete transaction findings.

Original data: Olist Brazil 2016-2018. Source licence terms must be respected. Figures are not a live commercial implementation, supplier inbound OTIF, warehouse stockouts or verified purchasing spend.
