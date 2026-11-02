# Technical setup and reproducibility

This page is for technical reviewers who want to reproduce the analysis. For the business story, findings and charts, start with the [project overview](../README.md).

## Data availability

The public release includes **verified Olist seller-state and city summaries**. The original Olist transaction CSVs are **not included**, and customer-order/delivery KPIs have not yet been computed in the published Excel workbook.

Source: [Olist Brazilian E-Commerce Public Dataset on Kaggle](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce). The historical source covers Brazil in 2016-2018. Transaction values are in BRL. Check the publisher's CC BY-NC-SA 4.0 conditions before redistributing source data or derived material.

## Requirements

- Python 3.10+.
- The ETL script uses the Python standard library only.
- The Excel workbook builder uses `artifact_tool`, which must be installed in the runtime where the workbook is rebuilt.
- The optional downloader is network-dependent.

## Obtain the eight source CSVs

Download the original Olist dataset from Kaggle, or optionally try:

```bash
python scripts/download_olist.py
```

Place these eight original files in `data/raw/`:

```text
olist_orders_dataset.csv
olist_order_items_dataset.csv
olist_order_payments_dataset.csv
olist_order_reviews_dataset.csv
olist_products_dataset.csv
olist_sellers_dataset.csv
olist_customers_dataset.csv
product_category_name_translation.csv
```

The geolocation CSV is optional and is not required for the pipeline.

## Run the analysis

```bash
python scripts/process_olist.py --raw data/raw --output data/processed
python scripts/build_workbook.py --processed data/processed --output workbook/Olist_Order_Fulfilment_Intelligence.xlsx
python -m unittest discover -s tests -v
```

On Mac/Linux, `sh scripts/run_pipeline.sh` executes the steps in sequence.

The processing script produces:

- `data/processed/kpi_summary.json`
- `data/processed/orders_enriched.csv`
- `data/processed/monthly_metrics.csv`
- `data/processed/seller_summary.csv`
- `data/processed/category_summary.csv`
- `data/processed/seller_state_counts.csv`

The Excel workbook is generated from the computed files, not a manually populated customer-delivery dashboard. **Do not publish delivery metrics until the transaction data have been processed and reconciled.**

## Reconciliation and measurement boundaries

- Keep one row per order in the order-level reporting view.
- Aggregate payment and order-item values separately by `order_id` before joining to avoid duplicate financial totals.
- Measure customer on-time delivery only for delivered orders with both actual and estimated delivery dates.
- Do not claim upstream supplier OTIF, overdue purchase orders, stockouts or actual purchasing spend from this dataset.
- Review [KPI definitions](03_kpi_dictionary.md), [data-quality controls](04_data_quality.md) and [source provenance](../data/reference/PROVENANCE.md).

The current public workbook intentionally shows **Not loaded** in customer-order and delivery fields. This is a data-availability disclosure, not a zero result.
