# Excel workbook

**[Download Olist_Order_Fulfilment_Intelligence.xlsx](Olist_Order_Fulfilment_Intelligence.xlsx)**

The published 12-sheet Excel workbook is a historical Olist portfolio prototype. It contains a verified 3,095-seller geographic reference, an executive summary, seller-state and city views, KPI definitions, BA requirements, source log, how-to-use instructions and data-quality controls.

**Data status:** The Olist customer order, item, payment and review CSVs are **not** bundled in this GitHub repository. Accordingly, customer delivery counts, on-time rates, lead time, seller-attributed item sales and category sales are marked **Not loaded** in the released workbook. Do not quote those as observed KPIs.

## Review

1. Open `DASHBOARD`: 3,095 unique seller IDs, 23 Brazilian state codes, 1,849 sellers in São Paulo.
2. Check `SELLER_STATES` and `SELLER_CITIES` for the grouped reference.
3. Review `KPI_DICTIONARY`, `BA_REQUIREMENTS`, `SOURCE_LOG` and `DATA_QA`.
4. For the business story and findings, read the [project overview](../README.md). Technical reviewers who want to load the full Olist order dataset can use the [separate setup guide](../docs/08_technical_setup.md).

Reporting source: [Olist Brazilian E-Commerce Public Dataset](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce). The project is not a live operational system. Currency of the original order dataset is BRL, not NZD.

The original `.xlsx` binary was committed to this repository without modifying its fonts or layout.
