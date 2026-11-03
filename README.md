# Olist Order Fulfilment & Delivery Intelligence

**Business Analysis portfolio | Real public marketplace data | Brazil, 2016-2018**

**The business challenge:** Understand where marketplace sellers are concentrated and build a reliable foundation for measuring whether customers receive orders on time.

> **Current result:** Seller-network analysis is complete using real Olist records. Customer delivery analysis is the next phase because the full order files have not been processed. No delivery rates or business savings are claimed.

![Executive dashboard: verified seller counts, geographic concentration and unavailable delivery metrics](evidence/dashboard_overview.svg)

**[Excel Dashboard](workbook/Olist_Order_Fulfilment_Intelligence.xlsx) | [One-page Management Brief](docs/09_management_brief.md) | [Original Olist Data](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)**

## What I worked on

Instead of starting with a dashboard, I started with the business question: **Can an operations team see where the seller network is concentrated and identify what to investigate next?**

![Workflow from public seller data to business decisions](evidence/analysis_to_action.svg)

The work covers understanding the decision, checking real seller IDs, grouping them by location, building visual reporting and explaining the limitations of the information.

## The findings at a glance

| Verified observation | Result |
|---|---:|
| Distinct sellers | **3,095** |
| Brazilian states represented | **23** |
| Sellers in São Paulo state | **1,849 (59.7%)** |
| Sellers across the five largest states | **2,803 (90.6%)** |
| Sellers across the ten largest city/state strings | **1,254 (40.5%)** |

### Finding 1. Sellers are concentrated in a few states

![Chart: the top five Brazilian states by seller IDs and all remaining states](evidence/seller_state_concentration.svg)

**What it means:** Nearly six in ten recorded seller IDs are in São Paulo state. This is a starting point for examining geographic coverage, not proof of delivery delays or a supplier-capacity risk.

### Finding 2. São Paulo city has the largest seller count

![Chart: the ten city/state strings with the most Olist seller IDs](evidence/top_seller_cities.svg)

**What it means:** The raw `sao paulo, SP` city/state entry represents **694 sellers (22.4%)**. Geographic distribution can be compared with customer demand once actual orders and delivery addresses are available.

## What decisions could a manager make?

| Question | Practical next step |
|---|---|
| Is the seller network geographically concentrated? | Review the state and city breakdowns. |
| Does that concentration affect customers? | Compare seller locations with customer order locations and demand. |
| Are deliveries arriving when expected? | Measure performance only after validating actual and estimated delivery dates. |
| Which issues should be prioritised? | Use late-delivery trends, freight and customer reviews once transactional analysis is complete. |

**Important:** Seller counts are not sales, shipments, warehouse capacity or supplier OTIF.

## What comes next?

<details>
<summary><strong>Customer delivery, freight and customer experience</strong></summary>

The original Olist dataset also contains customer orders, items, payment records and reviews. When these files are analysed and reconciled, the project can calculate customer on-time delivery, average lead time, late orders, freight-to-item value and review patterns. **These results have not yet been published.**

The workbook intentionally shows **Not loaded** for unavailable customer-order and delivery measures rather than fictional percentages.

</details>

## Explore more

**[Management Brief](docs/09_management_brief.md)** - findings, visuals and decision questions for business readers.

**[Excel Dashboard](workbook/Olist_Order_Fulfilment_Intelligence.xlsx)** - verified seller geography and clearly identified pending delivery metrics.

**[Business Case](docs/01_business_case.md)** - the business problem and stakeholders.

**[Data Quality](docs/04_data_quality.md)** - what was checked.

**[Technical Setup](docs/08_technical_setup.md)** - source files and reproducibility instructions for technical reviewers.

**[Source Provenance](data/reference/PROVENANCE.md)** - original public seller dataset and coverage.

<sub>Source: Olist Brazilian E-Commerce Public Dataset, Brazil 2016-2018. The published charts reflect verified seller IDs only. Original data licence: CC BY-NC-SA 4.0. An independent case study; not an Olist or New Zealand production system. Monetary order data, when processed, are in BRL rather than NZD.</sub>
