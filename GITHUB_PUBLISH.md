# Publication and Data Reproducibility

This repository contains a **verified historical Olist Business Analysis portfolio**. To review without technical detail, read the [single visual overview](README.md).

**Published deliverables:**
- [Full real-data Excel workbook, 16 worksheets](workbook/Olist_Order_Fulfilment_Intelligence_Real_Data.xlsx).
- [Management findings](docs/10_delivery_performance_findings.md) and [management brief](docs/09_management_brief.md).
- [Source-derived KPI and monthly evidence](data/processed/kpi_summary.json).
- [Data quality and tests](docs/04_data_quality.md).

Source data were obtained from [Olist's original public dataset repository](https://github.com/olist/work-at-olist-data), with the exact source commit documented in [provenance](data/processed/PROVENANCE.json). Individual customer/order records are not redistributed.

GitHub Actions verifies the processing logic and aggregate reconciliations. The [technical setup guide](docs/08_technical_setup.md) describes how to reproduce the calculations. The optional workbook-generation script is a **simpler Excel edition**, not a pixel-identical recreation of the published 16-sheet portfolio workbook.

Data describe Brazil 2016-2018 and transactions in BRL. The project does not claim supplier inbound OTIF, inventory stockouts, upstream purchasing spend, live deployment or proven savings.
