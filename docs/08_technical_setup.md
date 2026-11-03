# Reproducibility for Technical Reviewers

For the business narrative and visual results, start with the [project overview](../README.md).

## Verified analysis is already complete

The Olist source-based report covers **99,441 orders**, **96,470 delivery-eligible orders**, **93.23% on-time customer deliveries**, category value, customer region and review outcomes. The [source manifest](../data/processed/PROVENANCE.json) records the original Olist repository commit used.

The original row-level files are deliberately **not republished**. Source-verified aggregates are provided in [data/processed](../data/processed/kpi_summary.json).

## Rebuild the results

- Source CSVs: [Olist's original public GitHub repository](https://github.com/olist/work-at-olist-data/tree/master/datasets) or [Olist on Kaggle](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce).
- Required tables: `olist_orders_dataset.csv`, `olist_order_items_dataset.csv`, `olist_order_payments_dataset.csv`, `olist_order_reviews_dataset.csv`, `olist_products_dataset.csv`, `olist_sellers_dataset.csv`, `olist_customers_dataset.csv`, `product_category_name_translation.csv`.
- Optional: geolocation CSV is not used in this analysis.

With Python 3.10+ and the eight files in `data/raw/`, run:

```bash
python scripts/process_olist.py --raw data/raw --output data/processed
python scripts/summarise_delivery_experience.py --orders data/processed/orders_enriched.csv --output data/processed
python -m unittest discover -s tests -v
```

The pipeline itself uses the Python standard library. The optional Excel builder `scripts/build_workbook.py` uses `artifact_tool`, which requires a compatible runtime; the GitHub-hosted workbook is still the earlier seller edition.

## Key checks and boundaries

- Unique order IDs are retained, and item/payment/review rows are independently aggregated before joining.
- The on-time cohort contains only delivered orders with actual and estimated customer dates.
- Eight delivered records lack actual dates, so they are excluded from the eligible denominator.
- The source status `canceled` is included in cancellation rate.
- QA verifies monthly counts, customer destinations and category merchandise/freight totals.
- Monetary values are customer-side BRL, not upstream supplier spending or carrier invoices.
- Supplier inbound OTIF, overdue upstream POs and inventory stockouts cannot be established from these source tables.

The public [source-derived KPI file](../data/processed/kpi_summary.json), [KPI definitions](03_kpi_dictionary.md) and [data quality results](04_data_quality.md) provide more detail.
