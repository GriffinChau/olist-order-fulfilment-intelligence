# Olist Excel dashboard — published versus generated

The **[curated 16-sheet full-data Excel portfolio workbook](Olist_Order_Fulfilment_Intelligence_Real_Data.xlsx)** is the canonical presentation delivered in this repository. It contains verified Olist Brazil (2016-2018) reporting, using BRL. The [one-image executive summary](../README.md) is a quicker starting point for business reviewers.

## Reproducibility

The **source-derived metrics** and supporting aggregates can be recreated from the eight original Olist CSVs, with integrity checks; see [technical reproducibility](../docs/08_technical_setup.md).

```bash
# Rebuild source-derived tables and validate them without the optional workbook library
BUILD_WORKBOOK=0 sh scripts/run_pipeline.sh

# Also generate a simpler spreadsheet, with artifact_tool installed
sh scripts/run_pipeline.sh
```

The generated workbook is named `Olist_Order_Fulfilment_Intelligence_Rebuilt.xlsx` to prevent confusing it with the curated publication. The Python builder **does not currently recreate the canonical 16-sheet workbook or its exact visuals**. The curated file is checked as an Excel ZIP package by the repository tests, but this is not a claim that it is automatically regenerated.

**Verified source highlights:** 99,441 historical customer orders; 96,470 eligible delivered orders; 89,936 on time (93.23%); 6,534 late. Customer delivery against the estimated date is **not** supplier inbound OTIF. Listed freight is not an independently verified carrier invoice.
