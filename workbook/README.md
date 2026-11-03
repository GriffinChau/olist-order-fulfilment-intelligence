# Olist Excel Dashboard - Full Real-Data Edition

**[Open the current Excel dashboard (16 worksheets)](Olist_Order_Fulfilment_Intelligence_Real_Data.xlsx)**

This is the **full real-data edition**, covering the original Olist customer-order analysis, delivery performance, region and category comparisons, seller information and business reporting. The workbook is saved in this repository and is separate from the lightweight public-data pipeline scripts.

For the simplest overview, start with the [one-image executive dashboard](../README.md) rather than browsing every worksheet.

**Verified source highlights:** 99,441 customer orders, 96,470 delivery-eligible orders, 93.23% on time, 6,534 late deliveries. Source evidence and quality controls are published in [data/processed](../data/processed/kpi_summary.json).

**Scope:** Historical Olist Brazil data (2016-2018), BRL. The on-time metric measures customer delivery against the estimated date, not upstream supplier OTIF. Listed freight is not a carrier invoice.

The optional [Python Excel builder](../scripts/build_workbook.py) is a simpler reproducible reporting implementation; it should not be confused with the formatting and layout of this 16-worksheet portfolio file.
