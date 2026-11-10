# Olist customer delivery — management brief

## Executive decision

**Recommendation:** prioritise a diagnostic review of the **March 2018 purchase cohort** and lower-performing destination states, then examine whether the observed delays align with specific fulfilment events, carrier patterns or order characteristics. The available Olist records identify **where to investigate**, not a proven operational root cause or a realised saving.

Among **96,470 eligible deliveries**, **89,936 arrived on time (93.23%)** and **6,534 were late**. For orders purchased in **March 2018**, only **81.04%** were on time: **1,328 late out of 7,003 eligible**. This is a **12.19 percentage-point descriptive gap** compared with the entire eligible population; it is not an estimate of preventable delays or a causal effect.

## Evidence → business implication → proposed action

| Evidence observed | Business implication (hypothesis, not proven impact) | Decision / next investigation | Additional evidence required |
|---|---|---|---|
| March 2018 purchase cohort: **81.04%** on time, **1,328** late | An unusually large exception cohort deserves attention | Compare process milestones and service promises with other months | Dispatch timestamps, carrier scans, peak demand and route mix |
| **SP: 95.51%** on time among 40,494 eligible vs **RJ: 87.89%** among 12,350 | Different customer destinations experienced different service levels | Segment RJ and SP by category, seller origin, distance and promise window | Carrier allocation, dispatch origins and comparable order segments |
| Valid reviewed orders: on-time/early **4.29/5**, late **2.27/5** | Delays may signal an elevated customer-experience risk | Review negative feedback on late deliveries and evaluate service-recovery options | Complaint/contact histories and controlled follow-up outcomes |
| Listed freight **BRL 2.26M** vs item value **BRL 13.59M** (**16.60%**) | Freight exposure deserves further segmentation | Review categories with higher freight-to-item ratios | Actual carrier invoices, fulfilment costs and contribution margins |

## Suggested decision sequence

1. **Operations diagnostic:** identify whether March 2018 exceptions cluster in specific routes, dispatch origins, delivery promises or order types. Define comparable cohorts before suggesting a cause.
2. **Customer experience review:** connect late-delivery groups to complaints and support interactions where additional records are available; assess possible interventions.
3. **Cost validation:** compare listed freight charges with actual carrier invoices and margins before recommending any financial optimisation.
4. **Pilot only after validation:** if a suspected driver is confirmed and an intervention is feasible, specify an owner, baseline on-time rate, target metric, comparison population and decision date. No pilot or savings are claimed here.

## How confident are we?

The repository publishes source provenance, one-order-per-order processing logic and reconciled monthly, regional, category and review aggregates. Those checks support **internal consistency**, not external financial assurance or causal inference.

**Interpretation boundaries:** reporting groups orders by **purchase month**, not actual delivery month; regions are **customer destinations**, not warehouse locations. On-time measures **actual versus estimated customer delivery**, not supplier inbound OTIF. The records are historical Brazil 2016–2018, in **BRL**. Listed freight is not independently audited carrier expense. This is an **independent portfolio case study**, not an implemented Olist decision.

**Evidence:** [Detailed findings](10_delivery_performance_findings.md) · [Quality and reconciliation](04_data_quality.md) · [Source-derived KPI summary](../data/processed/kpi_summary.json) · [Monthly data](../data/processed/monthly_metrics.csv) · [Data pipeline](08_technical_setup.md).
