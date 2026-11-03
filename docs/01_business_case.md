# Business case - Order Fulfilment & Delivery Performance

## Business problem
A marketplace operations team needs to monitor customer order fulfilment, delivery delays, freight exposure and customer reviews. Orders, items, payments and reviews are separate event grains, so direct many-to-many joins can inflate revenue and distort service KPIs.

## Stakeholders and decisions
| Stakeholder | Business question | Decision |
|---|---|---|
| Operations Manager | Do delivered orders reach customers by the estimated date? | Prioritise investigation of delayed purchase-month cohorts |
| Customer Experience Analyst | Are late orders associated with lower reviews? | Investigate service issues; do not assert causation |
| Category Manager | Which product groups generate item value and freight? | Analyse product and delivery mix |
| Seller Operations | How are marketplace sellers geographically distributed? | Examine logistics coverage by location |
| Business / Data Analyst | Do source keys, metrics and joins reconcile? | Validate reports and data quality |

## Scope
In scope: Olist customer orders, delivery dates, order items, seller geography, reviews, freight, source provenance, data QA and reproducible processing.

Out of scope: inbound supplier OTIF, purchase order backlog, actual upstream purchasing spend, inventory stockouts, carrier invoices, guaranteed savings and real-time operations.

## Acceptance criteria
- AC-01: One row per order in processed order-level results.
- AC-02: Only delivered orders with both actual and estimated customer-delivery dates enter the on-time denominator.
- AC-03: Item and payment values are independently aggregated to order grain before joining.
- AC-04: Unmatched source keys are quantified.
- AC-05: Historic Brazil / BRL source, licence and limitations are disclosed.
- AC-06: Unsupported supplier and inventory KPIs remain unavailable.

**Current status:** The historical Olist source has now been analysed across customer orders, products, seller locations, reviews and payment records. The published aggregate evidence establishes 99,441 orders and 93.23% on-time customer delivery among 96,470 eligible delivered orders. The [16-sheet full-data Excel workbook](../workbook/Olist_Order_Fulfilment_Intelligence_Real_Data.xlsx), source-derived results and a [single executive dashboard](../README.md) are now published. This remains a portfolio case study, not an operational deployment.
