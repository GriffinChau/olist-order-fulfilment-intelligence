# Power BI | Olist Customer Delivery Intelligence

**Purpose:** Convert the verified historical Olist analysis into an interactive, business-friendly report for Operations and Supply Chain managers.

**Status:** Power BI-ready datasets and calculation definitions have been prepared. **No report has yet been published to a Power BI workspace**, because publishing requires an authorised Microsoft Power BI connection.

## Suggested report layout

| Page | What the viewer sees | Intended question |
|---|---|---|
| **1. Executive Overview** | KPI cards: 99,441 orders, 93.23% on-time, 6,534 late, 12.56-day historical average lead time; monthly trend | How reliable is customer delivery? |
| **2. Delivery Exceptions** | On-time and late counts by purchase month, with March 2018 highlighted | Which periods merit investigation? |
| **3. Customer Regions** | On-time rates and eligible-order volumes by customer destination state | Where does service performance differ? |
| **4. Customer Experience** | Review scores and low-rating shares for on-time vs late deliveries | What association exists between delays and reviews? |
| **5. Product & Freight** | Category item value, listed freight and freight/item ratio | Which categories merit further cost investigation? |

**Visual style:** Navy headings, teal for key results, amber for delivery exceptions, short annotations, no repeated screenshots or text-heavy introductions.

## Public Power BI-ready datasets

These files contain **aggregated real Olist results**, not simulated orders.

| Import as | Source in this repository | Data grain |
|---|---|---|
| `KPIs` | [kpi_overview.csv](kpi_overview.csv) | One row, entire historical period |
| `Monthly` | [monthly_metrics.csv](../data/processed/monthly_metrics.csv) | One row per purchase month |
| `Regions` | [customer_region_summary.csv](../data/processed/customer_region_summary.csv) | One row per customer destination state |
| `Reviews` | [review_by_delivery.csv](../data/processed/review_by_delivery.csv) | One row per delivery outcome |
| `Categories` | [category_summary.csv](../data/processed/category_summary.csv) | One row per product category |

**Calculations:** [Power BI DAX measures](measures.dax). These include correctly weighted on-time rates and freight-to-item ratios.

## How the Power BI report should behave

- Use monthly measures to show the overall trend and to filter monthly charts.
- Use the customer-state table for regional comparisons; filter out very small cohorts or always display the denominator.
- Display review scores for each delivery-outcome group, not a sum of averages.
- Display the freight ratio using aggregated item and freight totals, not the average of individual category percentages.
- **Do not cross-filter independent aggregated tables as though they share transaction-level relationships.** A month selection cannot correctly recalculate region or review results without more detailed transaction-level data.
- Keep the historical `Avg Lead Days` measure clearly labelled as an overall-period statistic rather than a per-month metric.

## How to open in Power BI

After connecting and authorising Power BI, import these five CSVs from their raw GitHub links or download the files from this repository. Assign the table names above, set numeric types and apply the measures from [measures.dax](measures.dax). For `Monthly[month]`, sort ascending as text in `YYYY-MM` format. The complete project source is [Olist's official public data](https://github.com/olist/work-at-olist-data).

If a fully cross-filterable report by both month **and** customer destination is required, the original order-level Olist data must be loaded in Power BI, with a checked one-to-many data model. The public CSVs above are intentionally aggregates.

## Data integrity

The prepared inputs are derived from **99,441 actual Olist orders**, of which **96,470** delivered orders have both actual and estimated delivery dates. **89,936** of those met the estimated date, giving **93.23% on-time delivery**. Source [KPI checks](../data/processed/kpi_summary.json), [QA notes](../docs/04_data_quality.md) and [provenance](../data/processed/PROVENANCE.json) are public.

Historical Brazil data (2016-2018), BRL. The report measures **customer delivery against estimated dates**, not inbound supplier OTIF, purchasing spend or audited carrier expense. Observed review differences are not proof of causality.
