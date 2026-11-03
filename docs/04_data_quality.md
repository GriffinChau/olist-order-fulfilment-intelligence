# Data Quality and Acceptance Evidence

## Source coverage verified

| Source record type | Source rows verified | Reporting use |
|---|---:|---|
| Orders | **99,441** | Delivery timing, purchase-month cohorts and cancellation status |
| Delivered orders | **96,478** | Customer delivery status |
| Eligible delivered orders | **96,470** | On-time customer delivery; 8 missing actual delivery dates excluded |
| Order items | **112,650** | Item price and freight value |
| Customer payments | **103,886** | Customer-side payment amount, not supplier spend |
| Review events | **99,224** | Review scores grouped within order |
| Seller master | **3,095** | Marketplace seller geography |
| Products | **32,951** | Product category and item classification |

## Reconciliation rules

- **Delivery:** 89,936 on time + 6,534 late = **96,470 eligible delivered orders**.
- **Monthly:** Sum of all purchase-month order counts = **99,441**.
- **Geography:** Sum of all eligible orders across customer states = **96,470**.
- **Commercial:** Category-level item values sum to **BRL 13,591,643.70** and quoted freight values sum to **BRL 2,251,909.54**.
- **Payments:** Customer payment events sum to **BRL 16,008,872.12** and must not be joined directly to item lines before summing.
- **Reviews:** Where more than one review occurs for an order, first compute the **per-order mean review**, then compare reviewed order groups.

These source-derived aggregate files are published in [evidence](../evidence/). The Python checks in [test_published_evidence.py](../tests/test_published_evidence.py) independently verify internal aggregate consistency. The existing synthetic test fixtures test code behaviour, not real-world delivery performance.

## Exceptions and limitations

- 8 delivered orders do not have an actual customer delivery timestamp; they are excluded from the eligible on-time denominator.
- 1,603 order-item lines were linked to products with missing or blank category descriptions in the source analysis; keep them in the overall item-value total.
- A passing aggregate check does not establish independent financial audit accuracy, perfect postal addresses or cause of delivery delays.
- Supplier inbound OTIF, overdue upstream purchase orders and inventory stockouts are not available in this public dataset.
- Original raw Olist CSVs are not redistributed. Source is historical Brazil 2016-2018, currency BRL.

## Business acceptance

| Requirement | Evidence |
|---|---|
| BR-01 Delivery on-time KPI | [Source-derived order KPI summary](../evidence/order_delivery_kpis.json) |
| BR-02 Freight and category values | [Commercial evidence](../evidence/commercial_kpis.json) |
| BR-03 Avoid doubled values | Order-level grouping methodology, QA and synthetic join unit test |
| BR-04 Seller geography | [Verified seller counts](../data/reference/olist_seller_state_profile.csv) |
| BR-05 Transparent reporting scope | [KPI Dictionary](03_kpi_dictionary.md) and [source limitations](../README.md) |
| BR-06 Reproducibility | Original publisher, public mirror, processing code and aggregate tests |

**Reporting release caveat:** The GitHub-hosted Excel binary is an earlier seller-only version pending replacement. Data-derived dashboard images and aggregate metrics in the repository are current.
