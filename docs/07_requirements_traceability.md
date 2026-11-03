# Business Requirements and Evidence

| Requirement | What was delivered | Source evidence |
|---|---|---|
| BR-01: Measure customer on-time delivery | **93.23%** among 96,470 eligible orders | [KPIs](../data/processed/kpi_summary.json), [monthly chart](../evidence/customer_delivery_performance.svg) |
| BR-02: Investigate service exceptions | March 2018 and other weaker delivery periods identified | [Monthly evidence](../data/processed/monthly_metrics.csv) |
| BR-03: Understand customer regions | State-level on-time outcomes and denominators | [Region chart](../evidence/customer_delivery_by_region.svg) |
| BR-04: Connect delivery timing and reviews | Score association reported without causal claims | [Review chart](../evidence/delivery_and_reviews.svg) |
| BR-05: Analyse commercial exposure | Item prices and listed freight by category | [Freight chart](../evidence/freight_category_analysis.svg) |
| BR-06: Avoid misleading reporting | Unique order keys, separate aggregation and source reconciliation | [QA evidence](04_data_quality.md), [unit tests](../tests/test_pipeline.py) |

**Data status:** Source-derived aggregate reporting and business visualisations are complete. The GitHub Excel binary is still the initial seller-only edition and requires a separate refresh.

The case study has not been approved by a real Olist stakeholder and does not claim measured operational improvements.
