# Business requirements traceability

| ID | Business need | Acceptance test | Evidence | Status |
|---|---|---|---|---|
| BR-01 | Customer fulfilment timeliness | Delivered orders with both dates only; correct on-time denominator | [Order KPI summary](../evidence/order_delivery_kpis.json), [monthly delivery](../evidence/monthly_delivery_summary.csv) | Source aggregates verified |
| BR-02 | Explain commercial mix | Item price and freight reconcile across seller/category | [Category and freight evidence](../evidence/commercial_kpis.json) | Source aggregates verified |
| BR-03 | Avoid double counting | Many items + many payments remain one correctly valued order | Unit tests | Test passed |
| BR-04 | Profile marketplace footprint | Seller state totals = 3,095; SP = 1,849 | Verified real reference, workbook preview | Verified |
| BR-05 | Explain KPI boundaries | No invented supplier OTIF, upstream purchasing spend or stockouts | README, KPI dictionary | Documented |
| BR-06 | Reproducibility | Source attribution, executable scripts, and QA output | README, [source summary](../evidence/), [aggregate tests](../tests/test_published_evidence.py) | Aggregates validated; GitHub workbook binary replacement pending |

This is a portfolio requirements map, not a requirements baseline approved by Olist or a live employer.
