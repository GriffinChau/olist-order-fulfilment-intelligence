# Business Findings - Seller Geography

**Verified source:** Public Olist seller records from Brazil (2016-2018), not synthetic observations.

## Finding 1. Seller locations are highly concentrated

![Verified seller-state concentration](../evidence/seller_state_concentration.svg)

**1,849 out of 3,095 seller IDs (59.7%)** are in São Paulo state. The top five states account for **2,803 (90.6%)**.

**Management question:** Does customer demand follow the same geographic pattern? Seller counts alone cannot establish a logistics bottleneck.

## Finding 2. The largest raw city location is São Paulo

![Top ten seller city/state strings](../evidence/top_seller_cities.svg)

The raw city/state string `sao paulo, SP` accounts for **694 seller IDs (22.4%)**. The top ten strings represent **1,254 seller IDs (40.5%)**.

**Management question:** Are seller and customer locations balanced? This would require original customer order records, not only the seller master.

## Finding 3. Delivery reporting needs transaction-level evidence

Customer on-time delivery, late orders, freight ratios and review patterns are **not yet measured in the published workbook**. The original Olist order, item and review files must be loaded and reconciled first.

**Management question:** Once that data is ready, which months, states and categories show service issues that merit investigation?

See the [one-page management brief](09_management_brief.md) for a decision-oriented summary and the [data-quality note](04_data_quality.md) for source limitations.

**Interpretation boundary:** Seller location is not proof of revenue concentration, late shipments, warehouse capacity, supplier OTIF or operational savings.
