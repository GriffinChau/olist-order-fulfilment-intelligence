# Project roadmap

## Completed - Seller geography

Verified 3,095 unique marketplace sellers across 23 Brazilian states. Published seller-state and city graphics.

## Completed - Full customer-order analysis

Processed eight real Olist transactional CSVs from the publisher's public repository. Verified 99,441 orders, 96,470 delivered orders eligible for on-time calculation, 6,534 late orders and 93.23% on-time customer delivery. Produced category and customer-region aggregates and review comparisons.

## Completed - Business-facing visual reporting

Published monthly delivery, destination state, review comparisons and item/freight visualisations, including a [management findings report](10_delivery_performance_findings.md). The original row-level transaction records are not redistributed.

## Remaining - Excel workbook refresh

The GitHub Excel file remains the initial seller-geography edition. Rebuild the Excel file from the verified published aggregates with the same visual business interpretation and check that it matches the latest source-validated numbers. Do not call the original workbook the full-data report until updated.

## Future optional improvements

Explore carrier and origin/destination patterns if suitable data exist, and test whether delivery feedback associations hold when considering order value, category and customer region. Never infer supplier PO, inbound OTIF, inventory stockouts or actual purchasing spend from customer-side Olist orders.

**Release principle:** every portfolio metric must have an identifiable source, correct denominator and clear business meaning.
