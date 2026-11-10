# Technical reproducibility

This repository makes the **analysis and reconciled reporting data reproducible**. The public, curated **16-sheet Excel portfolio workbook is a separate, reviewed presentation artifact**; the Python workbook builder creates a simpler reporting edition, **not a pixel-identical or sheet-identical reproduction**. This distinction is intentional and should not be hidden from reviewers.

## Original data and dependencies

Use **Python 3.10+** and the eight original Olist CSV files from the [publisher repository](https://github.com/olist/work-at-olist-data) or [Kaggle listing](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce):

`olist_orders_dataset.csv`, `olist_order_items_dataset.csv`, `olist_order_payments_dataset.csv`, `olist_order_reviews_dataset.csv`, `olist_products_dataset.csv`, `olist_sellers_dataset.csv`, `olist_customers_dataset.csv`, and `product_category_name_translation.csv`.

Put the original files in `data/raw/`. The data-processing, reconciliation and unit-test scripts use only the Python standard library. **Only the optional workbook builder requires `artifact_tool`**. The original transaction-level CSVs are not redistributed in GitHub. The source commit and provenance of the published aggregates are recorded in [PROVENANCE.json](../data/processed/PROVENANCE.json).

## Rebuild and verify

From the repository root:

```bash
# Rebuild every source-derived aggregate, without the optional Excel dependency
BUILD_WORKBOOK=0 sh scripts/run_pipeline.sh

# With artifact_tool available, also produce a separately named reporting workbook
sh scripts/run_pipeline.sh
```

The shell workflow runs the following in order:

1. `scripts/process_olist.py`: join records at **order grain**, aggregate item/payment/review events separately, compute source KPIs and monthly/category/seller data.
2. `scripts/summarise_delivery_experience.py`: create the customer-state and review-by-delivery output files from the **freshly rebuilt** `orders_enriched.csv`.
3. `scripts/check_processed_outputs.py`: independently reconcile fresh monthly, category, customer-state and review aggregates with `kpi_summary.json`.
4. `python -m unittest discover -s tests -v` and `scripts/verify_bundle.py`: run regression tests and validate the separately published portfolio bundle.
5. Optional `scripts/build_workbook.py`: write `workbook/Olist_Order_Fulfilment_Intelligence_Rebuilt.xlsx` (simpler reporting edition, not the 16-sheet curated publication).

For the processing and QA steps alone, no workbook library is necessary. Set `RAW_DIR`, `PROCESSED_DIR`, `PYTHON`, or `WORKBOOK_OUTPUT` to override the defaults. Tests of **published** outputs still read the tracked `data/processed/` files; the new explicit reconciliation step checks the **freshly rebuilt** output directory.

## Canonical published workbook versus reproducible outputs

- **Published portfolio:** [Olist_Order_Fulfilment_Intelligence_Real_Data.xlsx](../workbook/Olist_Order_Fulfilment_Intelligence_Real_Data.xlsx) (16 curated worksheets; available immediately for reviewers).
- **Rebuildable deliverables:** `kpi_summary.json`, `monthly_metrics.csv`, `customer_region_summary.csv`, `review_by_delivery.csv`, `category_summary.csv`, and the separately named script-generated workbook.
- **Remaining limitation:** there is no code that recreates all 16 curated worksheets and their exact formatting. Do not present the builder as doing so. Automating that presentation layer would be a separate enhancement.

## Business definitions and boundaries

On-time delivery compares **actual vs estimated customer-delivery calendar dates** among delivered orders where both exist. Eight delivered orders lacking an actual date are omitted from this denominator. All values are historical Brazil 2016-2018, in **BRL**. Listed item and freight values are not audited carrier costs, purchasing spend or realised savings. See the [KPI dictionary](03_kpi_dictionary.md), [data quality checks](04_data_quality.md), and [management findings](10_delivery_performance_findings.md).
