# Management Brief - Olist Customer Fulfilment & Delivery

**Business question:** Are customer orders arriving when expected, where are service issues most visible, and what should the operations team investigate?

![Executive overview of customer delivery performance](../evidence/customer_delivery_trend.svg)

## The results

| Evidence from real Olist records | Result |
|---|---:|
| Customer orders | **99,441** |
| Eligible delivered orders | **96,470** |
| Delivered by estimated date | **93.23%** |
| Late delivered orders | **6,534** |
| Average purchase-to-delivery time | **12.56 days** |

## Three decision-relevant findings

### 1. Periods with more late deliveries

March 2018 had **1,328 late deliveries** and an **81.04% on-time rate**. February 2018 (**85.87%**) and November 2017 (**87.60%**) also warrant closer review. Combined, these three cohorts account for **48.3% of late orders**.

**Recommended review:** Compare order demand, seasonal effects, geography and shipping patterns. This analysis does not establish the cause.

### 2. Regional differences

![Customer delivery performance by state](../evidence/delivery_by_customer_state.svg)

In the large customer-state groups shown, delivery performance varies. For example, **Rio de Janeiro: 87.89% on time across 12,350 eligible orders**, compared with **São Paulo: 95.51% across 40,494 eligible orders**.

**Recommended review:** Examine customer distance and fulfilment characteristics before assessing policy options.

### 3. Customer experience is related to delivery timing

![Customer reviews and on-time versus late deliveries](../evidence/delivery_and_customer_reviews.svg)

Reviewed orders delivered on time averaged **4.29 / 5** versus **2.27 / 5** for reviewed late orders. The figures are associated, not evidence of causality.

**Recommended review:** Prioritise late-order case studies and review whether communications and delay recovery could be improved.

## Freight and category context

![Product value and freight by category](../evidence/product_category_and_freight.svg)

**BRL 13.59 million** of listed item value and **BRL 2.25 million** of quoted freight value appear in the original item records. Freight equals **16.57%** of the item value total. The published value is not a verified operational freight cost or supplier purchasing expense.

## What happened during the analysis?

![From source data to business decision](../evidence/analysis_to_action.svg)

The analysis identified the business questions, validated record counts and joins, measured delivery outcomes, compared groups and documented the operational decisions that the evidence could support.

## Important limitations

Data are real, historical, anonymised Olist transactions from **Brazil, 2016-2018**, reported in BRL. On-time delivery means actual customer receipt on or before the estimated calendar date, not upstream supplier OTIF. Raw CSV records are not republished in this GitHub repository. No claims about proven root causes, actual cost savings or results for a New Zealand business are made.

**Review links:** [Project overview](../README.md) | [KPI dictionary](03_kpi_dictionary.md) | [Data-quality notes](04_data_quality.md) | [Source-derived evidence](../evidence/).
