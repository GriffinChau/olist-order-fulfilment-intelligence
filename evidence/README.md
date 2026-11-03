# Olist Business Analysis - Visual Evidence

**Actual historical Olist records | Brazil, 2016-2018 | Source-derived aggregated results**

The charts answer the main management questions without requiring a reviewer to read the underlying CSVs.

## Delivery and customer experience

| Visual | Key question |
|---|---|
| ![Monthly delivery performance](customer_delivery_trend.svg) | When did customer orders arrive later than estimated? |
| ![Regional delivery reliability](delivery_by_customer_state.svg) | Which customer states had lower on-time delivery rates? |
| ![Customer reviews by delivery timing](delivery_and_customer_reviews.svg) | How did customer ratings differ between on-time and late orders? |
| ![Item categories and freight](product_category_and_freight.svg) | Which product groups have high recorded item value and freight exposure? |

## Seller geography (context)

[Seller state concentration](seller_state_concentration.svg) | [Top seller cities](top_seller_cities.svg) | [Analysis to decision process](analysis_to_action.svg).

Seller population is not a measure of sales, order volume or delivery quality.

## Evidence files and source scope

| File | What is verified |
|---|---|
| [Order KPI summary](order_delivery_kpis.json) | 99,441 orders; 96,470 eligible delivered; 93.23% on time; 6,534 late |
| [Monthly delivery CSV](monthly_delivery_summary.csv) | One row per purchase-month cohort; order and delivery reconciliation |
| [Customer state and reviews](delivery_by_state_and_reviews.json) | State-level eligible orders, late counts and descriptive order-level review scores |
| [Commercial categories](commercial_kpis.json) | 112,650 item lines, category item prices and listed freight, plus reconciliation checks |
| [Customer payments](customer_payment_kpis.json) | 103,886 customer payment events, separate from procurement spend |

**Source:** [Olist Brazilian E-Commerce Public Dataset](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce), accessed through a [public source CSV mirror](https://github.com/anggid/Brazilian-E-Commerce-Public-Dataset-by-Olist). The original source records are not redistributed in this repository. Source licence: **CC BY-NC-SA 4.0**.

**Measurement boundaries:** On-time compares customer actual vs estimated delivery calendar date, not supplier OTIF. Listed freight is not an audited carrier cost. Differences in customer review scores describe association, not causality.

The GitHub-hosted [Excel workbook](../workbook/Olist_Order_Fulfilment_Intelligence.xlsx) is still the earlier seller preview until its binary is replaced with the updated workbook. The validated delivery results are published in the evidence above.
