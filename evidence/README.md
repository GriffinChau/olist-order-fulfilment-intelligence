# Olist Visual Evidence

The main portfolio README displays **one consolidated dashboard**:

**[View the executive summary](executive_summary.svg)**

Additional chart files are kept here as optional drill-down evidence. They are not repeated inline in the README or Management Brief.

| Optional chart | Question answered |
|---|---|
| [Monthly delivery](customer_delivery_performance.svg) | Which purchase months experienced more delivery exceptions? |
| [Delivery by destination state](customer_delivery_by_region.svg) | How do on-time rates vary between destination states? |
| [Customer reviews](delivery_and_reviews.svg) | What review differences are associated with delivery timing? |
| [Category freight](freight_category_analysis.svg) | How do item values and listed freight compare by product category? |
| [Seller geography](seller_state_concentration.svg) | Where are marketplace sellers located? |

**Underlying source-derived evidence:** [KPI summary](../data/processed/kpi_summary.json), [monthly data](../data/processed/monthly_metrics.csv), [customer states](../data/processed/customer_region_summary.csv), [reviews](../data/processed/review_by_delivery.csv), [category values](../data/processed/category_summary.csv) and [source provenance](../data/processed/PROVENANCE.json).

Olist source data are historical Brazil records for 2016-2018. The delivery KPI compares the customer's actual date with the estimated date. Listed freight is not independently audited carrier cost. Review-score differences do not prove causation.
