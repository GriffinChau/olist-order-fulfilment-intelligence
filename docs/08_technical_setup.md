# Technical Reproducibility

Business reviewers can start at the [project overview and single executive dashboard](../README.md) or [the 16-sheet full-data Excel workbook](../workbook/Olist_Order_Fulfilment_Intelligence_Real_Data.xlsx). Technical details are kept here to avoid cluttering the portfolio page.

## Source and verified results

The project processed eight original Olist public CSVs and published reconciled aggregate results: **99,441 orders**, **96,470 eligible delivered orders**, **93.23% on-time**, category commercial values, destination-state delivery and review comparisons. The original row-level records are not redistributed.

[Olist source repository](https://github.com/olist/work-at-olist-data) | [Original Kaggle listing](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce) | [Source commit](../data/processed/PROVENANCE.json)

## Reproducing the analysis

With Python 3.10+, obtain the original Olist files (`olist_orders_dataset.csv`, `olist_order_items_dataset.csv`, `olist_order_payments_dataset.csv`, `olist_order_reviews_dataset.csv`, `olist_products_dataset.csv`, `olist_sellers_dataset.csv`, `olist_customers_dataset.csv`, `product_category_name_translation.csv`) and put them in `data/raw/`.

```bash
python scripts/process_olist.py --raw data/raw --output data/processed
python scripts/summarise_delivery_experience.py --orders data/processed/orders_enriched.csv --output data/processed
python -m unittest discover -s tests -v
```

The processing pipeline uses the Python standard library. The optional [workbook builder](../scripts/build_workbook.py) uses `artifact_tool` and builds a simpler Excel reporting edition; the currently published **16-worksheet portfolio workbook** is [here](../workbook/Olist_Order_Fulfilment_Intelligence_Real_Data.xlsx).

## Measures and limitations

- One order ID is counted once; items, payments and reviews are aggregated separately before joining.
- On-time delivery compares actual and estimated **customer** delivery dates. Eight delivered records missing actual dates are excluded.
- The source's `canceled` status corresponds to 625 canceled orders.
- Category totals, monthly counts, review coverage and customer-region totals are checked against source-derived aggregates.
- Currency is BRL, historical Brazil 2016-2018. Customer-side item and freight values are not supplier spend or audited transport invoices.

See [data quality](04_data_quality.md) and [KPI dictionary](03_kpi_dictionary.md).
