# Visual evidence

This folder presents verified findings from real Olist marketplace seller records. The charts are based on the source summaries in [data/reference](../data/reference/PROVENANCE.md).

| Visual | What it shows |
|---|---|
| [Executive dashboard](dashboard_overview.svg) | Confirmed seller counts and current data availability |
| [State concentration](seller_state_concentration.svg) | Top five states, all remaining states and seller counts |
| [Top seller cities](top_seller_cities.svg) | Ten most frequent raw city/state seller locations |
| [Analysis to action](analysis_to_action.svg) | How the business question leads to analysis and next decisions |

## Key numbers

- **3,095** distinct Olist seller IDs across **23** Brazilian state codes.
- São Paulo state accounts for **1,849 (59.7%)**.
- Top five states together account for **2,803 (90.6%)**.
- Top ten city/state strings together account for **1,254 (40.5%)**.
- Raw `sao paulo, SP` accounts for **694 (22.4%)**.

These are seller population statistics, not order, turnover, delivery or warehouse metrics.

The original [Olist Excel workbook](../workbook/Olist_Order_Fulfilment_Intelligence.xlsx) is also available; its transactional customer delivery results remain **Not loaded** pending the original order files.

**Source:** [Olist Brazilian E-Commerce Public Dataset](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce), with the seller records via the [public CSV mirror](https://raw.githubusercontent.com/spdrio/Brazilian-E-Commerce-Public-Dataset-by-Olist/master/files/olist_sellers_dataset.csv). Source data are historical Brazil records from 2016-2018.
