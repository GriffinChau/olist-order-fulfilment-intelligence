# Implementation roadmap

## Stage 1 - Verified real-data seller footprint
Use the publicly accessible Olist sellers table, compute and reconcile real seller-state and seller-city summaries. Publish provenance and a workbook preview without invented delivery figures.

## Stage 2 - Full Olist order data
Download the eight original required CSVs from Kaggle, process them with `scripts/process_olist.py`, inspect `kpi_summary.json` and regenerate Excel using `scripts/build_workbook.py`. Resolve data gaps explicitly rather than inventing missing values.

## Stage 3 - Business Analysis validation
Inspect monthly delivery cohorts, seller/category freight trends and review associations, check denominators, confirm dashboard to source reconciliation, and document acceptance evidence. Do not claim real stakeholder sign-off.

## Stage 4 - Optional extensions
Investigate regional freight patterns, seller order concentration and an authenticated refresh process. Upstream supplier PO, inventory or actual procurement-cost reporting would require separately authorised ERP data from the *same* organisation.

**Release gate:** Do not call the project a completed full-data delivery analysis until all source CSVs have been processed and the KPI outputs spot-checked against the original files.
