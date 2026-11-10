# Power BI implementation notes

This folder documents **how the four-page Olist Delivery Intelligence report was modelled and assembled in Power BI**, based on the local PDF-style PBIP project. It is public technical evidence for the portfolio; **the editable PBIX/PBIP is intentionally kept off GitHub**.

The local project uses **Power Query (M), nine semantic-model tables, four relationships, 56 DAX measures and four report pages**. The source data is a historical Olist Brazil (2016–2018) snapshot, with amounts in BRL.

## Where to look

| File | What it documents |
|---|---|
| [Semantic model and Power Query](semantic_model.md) | Data origins, table grain, offline Import logic, dimension creation, relationship direction and modelling limits |
| [DAX measures](measures.dax) | **All 56 measure definitions** as transcribed from the local TMDL, including KPI displays, top-eight selection and conditional-color measures |
| [KPI dictionary](kpi_dictionary.md) | Definitions, numerators/denominators, expected values and QA checkpoints |
| [Four report pages](report_pages.md) | Exact Power BI visual types, measure bindings, positions, design and narrative for all four pages |
| [Page manifest](page_manifest.json) | Machine-readable page order, visual IDs/fields and 1600×900 coordinates |
| [Relationships](relationships.tmdl) | Four TMDL relationships from the local project |
| [Theme](theme.json) | The report's exported Power BI theme color/font settings |

The [model diagram](../powerbi_reporting_model.svg) illustrates the four fact–dimension branches. The [four-page PDF](../../reports/Olist_Delivery_Intelligence_Report.pdf) is the **visual reference**. It is not claimed to be a verified export from the local PBIP.

## Build flow

`8 original Olist CSVs → Python ETL + QA → published CSV/JSON aggregates → Power Query Import → 9-table semantic model → 56 DAX measures → 4 Power BI report pages`

The PDF-style Power BI project uses the published **aggregate snapshot** embedded into its local Power Query partitions. It does not contain all raw order-level rows, and cannot genuinely cross-filter category, region, month and reviews together.

**Report implementation:** Four 1600×900 pages. Each uses a static design template for the green sidebar, card frames and explanatory copy, with **four live Power BI KPI visuals and two native charts layered over it**. The page design follows the supplied reference PDF.

**Validation status:** The previously supplied offline project was reported to load in Power BI Desktop. The exact PDF-style layout was generated and checked structurally, but it still needs page-by-page visual confirmation in Power BI Desktop. These notes document the implementation; they do not pretend a screenshot or PDF was exported from the final local project.

## Portfolio-safe wording

> Built a Power BI reporting prototype with Power Query, a nine-table aggregate semantic model and DAX measures for delivery, regional, review and freight performance. Documented four report pages and reconciled the headline KPIs against published Olist aggregates.

Once the PDF-style report has been refreshed and visually validated in Desktop, the user can accurately describe it as a **Power BI dashboard/report**. The PBIX can remain private, while DAX, model documentation and screenshots of the *actual Desktop report* can be shared here later.
