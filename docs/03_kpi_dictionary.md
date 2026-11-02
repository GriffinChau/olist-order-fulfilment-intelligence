# KPI dictionary

| Metric | Formula / method | Correct denominator | Limitation |
|---|---|---|---|
| On-time customer delivery | Actual delivery calendar date <= estimated delivery date | Delivered orders with both dates | Estimate proxy, not supplier OTIF |
| Delivery delay days | Actual date - estimated date | Eligible delivered orders | Negative means early, positive means late |
| Average late days | Average of positive delay days | Late eligible delivered orders | Excludes early deliveries |
| Delivery lead time | Actual delivery timestamp - purchase timestamp | Eligible orders | Calendar duration |
| Cancellation rate | Cancelled order count / all orders | Loaded order population | Not supplier cancellation |
| Item value | Sum of order_items.price | Item lines | BRL merchandise value, not purchasing spend |
| Freight value | Sum of order_items.freight_value | Item lines | Not verified freight carrier invoice |
| Customer payment value | Sum of payment_value at order grain | Customer payment events | Not upstream AP spend |
| Seller-attributed sales | Sum item value by seller_id | Item lines | Marketplace sellers, not industrial suppliers |
| Category item value | Sum item value by translated category | Item lines | Preserve raw category if unmapped |
| Review rating | Mean valid 1-5 review scores within each order | Review events to order | Correlation is not causation |
| Seller footprint | Distinct seller IDs grouped by state | Seller master | Geography, not delivery performance |

Unavailable: supplier inbound OTIF, overdue supplier POs, actual supplier spend, inventory turnover, warehouse fill rate and stockouts. These require distinct operational records with trustworthy common keys.

**Historical data:** Brazil, 2016-2018. **Currency:** BRL, not NZD.
