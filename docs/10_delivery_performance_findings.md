# Customer Delivery Performance - Evidence-Based Findings

**Read the [one-page visual summary](../README.md) first.** This document provides the underlying interpretation, data denominators and practical follow-up questions without repeating the charts.

## 1. Customer delivery performance

The original Olist source contains **99,441 customer orders** and **96,478** orders marked delivered. Of the delivered population, **96,470** contain both an actual customer-delivery date and an estimated date; eight were excluded from the on-time denominator because the actual date was missing.

Of the eligible orders, **89,936 (93.23%)** were on or before the estimated calendar date and **6,534** arrived later. Mean time from purchase to delivery was **12.56 days** in the eligible group.

## 2. Periods warranting review

March 2018 had **1,328 late orders** among **7,003** eligible orders, giving **81.04%** on-time performance. February 2018 had **926 late (85.87% on time)** and November 2017 **904 late (87.60% on time)**. These are differences by *purchase-month cohort*, not independently verified carrier failure.

## 3. Destination differences

**SP:** 40,494 eligible deliveries, **95.51%** on time. **RJ:** 12,350 eligible deliveries, **87.89%** on time. **CE:** 1,279 eligible deliveries, **86.24%** on time. Comparisons must keep their denominators and account for order mix. The locations describe customer destinations rather than warehouse or dispatch origin.

## 4. Reviews and delivery timing

Reviewed on-time/early orders had a mean valid review score of **4.29/5** across **89,443 reviewed orders**. Reviewed late orders had an average of **2.27/5** across **6,381** reviewed orders. Low review scores (1-2/5) made up **9.23%** and **62.36%** respectively.

This is an observed association. The public records do not establish that timing alone caused lower ratings.

## 5. Merchandise and freight exposure

Across the original order-item rows, the sum of listed item prices was **BRL 13,591,643.70** and listed freight **BRL 2,256,599.44**, a freight-to-item ratio of **16.60%**. Category comparisons can identify areas for investigation. Listed freight is not independently verified carrier expense or a measure of profit.

## Management follow-up

| Priority | Question to investigate | Evidence still needed |
|---|---|---|
| 1 | Why did March 2018 have more late deliveries? | Carrier milestones, dispatch processes, order mix and demand peaks |
| 2 | Why do destination-state outcomes differ? | Routes, dispatch origins, distance and carrier allocation |
| 3 | How might late-delivery experience be improved? | Customer support histories and interventions |
| 4 | Which categories have higher underlying logistics costs? | Carrier invoices and contribution margin, not just listed freight |

## Evidence and boundaries

[Overall KPIs](../data/processed/kpi_summary.json) | [Monthly data](../data/processed/monthly_metrics.csv) | [Destination data](../data/processed/customer_region_summary.csv) | [Reviews](../data/processed/review_by_delivery.csv) | [Categories](../data/processed/category_summary.csv) | [Source provenance](../data/processed/PROVENANCE.json).

The source uses `canceled` for canceled orders, and **625 orders (0.63%)** have that status. Source-key, monthly, item and category checks passed. This is a **customer-delivery** study, not a calculation of supplier inbound OTIF, warehouse inventory or purchasing costs. Results reflect historical Brazilian records (2016-2018) rather than a live deployment.
