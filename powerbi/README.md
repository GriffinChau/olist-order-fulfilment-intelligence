# Power BI - Interactive Olist Delivery Intelligence

The Olist portfolio now includes **source-verified conformed fact tables** specifically prepared for an interactive Power BI Desktop model. The separate Power BI Project deliverable uses a native 1920 x 1080 layout, not screenshot-based KPI backgrounds.

## Real star-schema inputs

| Fact table | Grain | Verified source |
|---|---|---|
| **FactOrders** | Purchase month x customer state x delivery outcome | [Source-based order aggregates](../data/processed/pbi_fact_orders.csv) |
| **FactItems** | Purchase month x customer state x product category | [Source-based item aggregates](../data/processed/pbi_fact_items.csv) |

The Power BI model defines four dimensions: **DimMonth**, **DimState**, **DimDelivery**, **DimCategory**. There are **six active one-to-many relationships**. Month and State are conformed dimensions that can filter both fact tables. Delivery outcome filters only FactOrders; Category filters only FactItems. This is a fact constellation that preserves genuine reporting grain, not a fabricated transaction-level join.

All 99,441 source orders, 96,470 eligible deliveries, 6,534 late deliveries, 112,650 order-item lines and BRL item/freight totals have been reconciled in [source-derived QA tests](../tests/test_pbi_star_facts.py).

## Native Power BI report design

Five 16:9 pages:
1. Executive Overview - dynamically calculated KPIs and monthly/experience charts.
2. Delivery Exceptions - monthly service trend and late-order counts.
3. Customer Regions - delivery reliability and exceptions by destination state.
4. Customer Experience - reviews associated with on-time and late deliveries.
5. Product and Freight - real item value and freight ratios by category.

Cards are **live DAX measures**, not an image of a card. The Power BI report can be filtered using month, destination state, delivery outcome and product category slicers. A customer-state or month selection can affect metrics on both fact tables through relationships. All calculations preserve the original historical Olist source.

**External data dependency:** the new Power BI Project reads the two aggregated fact tables and the category dimension from public CSV links hosted on this repository with Power Query Web.Contents. Power BI Desktop may ask to set credentials to **Anonymous** and to refresh the model on first open. The PBIP project ZIP is a separate deliverable and is not currently checked into this GitHub repository.

## Source boundaries

[Original Olist publisher](https://github.com/olist/work-at-olist-data) | [Source provenance](../data/processed/PROVENANCE.json) | [Data checks](../docs/04_data_quality.md).

Data are historical Brazil 2016-2018, with BRL values. The on-time measure is based on customer delivery against the estimated date; it is **not supplier inbound OTIF**. Listed freight is not an audited carrier invoice. Review-score differences are associations rather than proof of causation.
