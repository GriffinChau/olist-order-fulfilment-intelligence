# Data Quality - Verified Olist Analysis

The eight transaction CSVs are read from [Olist's original GitHub repository](https://github.com/olist/work-at-olist-data) and independently summarised. Only verified aggregates are published, not the individual order records.

| Data checked | Source count |
|---|---:|
| Customer orders | **99,441** |
| Delivered orders | **96,478** |
| Eligible for on-time KPI | **96,470** |
| Delivered on time | **89,936** |
| Delivered late | **6,534** |
| Canceled orders | **625** |
| Item lines | **112,650** |
| Customer payment events | **103,886** |
| Review events | **99,224** |
| Seller master IDs | **3,095** |

## Reconciliation

- On-time 89,936 + late 6,534 = **96,470 eligible**.
- Eight delivered orders have no actual customer-delivery date and are excluded from the on-time denominator.
- Monthly order counts sum to **99,441**; customer-state eligible counts sum to **96,470**.
- Category merchandise total: **BRL 13,591,643.70**.
- Category listed freight total: **BRL 2,256,599.44**.
- Customer payment total: **BRL 16,008,872.12**. Payment events are aggregated by order before any order-item join.
- Multiple review records on one order are averaged to one order-level score.
- A source-status spelling of `canceled` is recognised; 625 canceled orders are counted.

All source-key linkage checks and monthly/item/category reconciliations passed. This establishes internal consistency, not independent financial audit accuracy.

**Review the evidence:** [Order KPI summary](../data/processed/kpi_summary.json), [monthly metrics](../data/processed/monthly_metrics.csv), [regions](../data/processed/customer_region_summary.csv), [reviews](../data/processed/review_by_delivery.csv), [product categories](../data/processed/category_summary.csv), [source commit](../data/processed/PROVENANCE.json).

The [automated aggregate tests](../tests/test_published_evidence.py) validate these published files. Synthetic unit-test fixtures remain clearly separated from real business results.

## Scope

The figures are historical Olist Brazil, 2016-2018. The metric is **customer on-time delivery against the estimated date**, not supplier inbound OTIF. This dataset cannot validate purchasing spend, warehouse inventory, actual carrier cost or operational savings.

The [16-worksheet full-data Excel workbook](../workbook/Olist_Order_Fulfilment_Intelligence_Real_Data.xlsx) is now published, with the [single business overview](../README.md) and reconciled source-derived results.
