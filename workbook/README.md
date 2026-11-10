# Excel Dashboard

This project includes a **[16-sheet Excel dashboard](Olist_Order_Fulfilment_Intelligence_Real_Data.xlsx)** built using real Olist e-commerce data from Brazil (2016–2018).

Python is used to clean, transform and validate the eight original datasets. Excel presents the results through KPIs, delivery trends, regional performance, customer reviews and freight analysis.

The data processing pipeline can be rerun using the original CSV files. The published 16-sheet dashboard is a separately curated portfolio deliverable; **the Python script does not recreate its exact layout**. See the [technical setup](../docs/08_technical_setup.md) for instructions.

**Key results:** 99,441 orders analysed; 96,470 eligible deliveries; 89,936 delivered on time (**93.23%**) and 6,534 delivered late.

*Scope:* On-time delivery is measured against the estimated customer delivery date, not supplier inbound OTIF. Freight is the listed dataset value, not verified carrier expense.
