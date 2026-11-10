# Delivery Intelligence PDF

This folder is for the four-page, landscape **Olist Delivery Intelligence** report. Keep the PDF here rather than in `evidence/`, which contains the individual SVG charts, or `workbook/`, which contains the Excel dashboards.

## Add the report

Upload the reviewed PDF here using this exact filename:

`reports/Olist_Delivery_Intelligence_Report.pdf`

On GitHub, open this folder and choose **Add file → Upload files**. After the upload is committed, link to the PDF itself from the main README (instead of the folder).

The PDF is a **fixed report for sharing or printing**, not the interactive Excel workbook. It covers:
- Customer delivery performance
- Destination-state comparisons
- Delivery timing and customer reviews
- Product values and listed freight

## Data check for the reviewed export

The visible report numbers were checked against the published source-derived files in `data/processed/`.

| PDF figures | Checked against | Result |
|---|---|---|
| 99,441 orders; 625 canceled; 96,470 eligible; 89,936 on time; 6,534 late; 93.23% | `kpi_summary.json` | Match |
| March 2018: 7,003 eligible, 1,328 late, 81.04% on time; 20 monthly cohorts Jan 2017–Aug 2018 | `monthly_metrics.csv` | Match |
| SP: 40,494 eligible and 95.51%; RJ: 12,350 and 87.89%; eight displayed state cohorts and late counts | `customer_region_summary.csv` | Match |
| 4.29 versus 2.27 average review; 9.23% versus 62.36% low ratings; 89,443 plus 6,381 reviewed orders | `review_by_delivery.csv` | Match |
| BRL 13.59M item value; BRL 2.26M freight; 16.60% ratio; 112,650 item lines; eight leading categories and their freight ratios | `kpi_summary.json` and `category_summary.csv` | Match |

**Rounding note:** the PDF states a **7.62 percentage-point** difference between SP (95.51%) and RJ (87.89%), obtained by subtracting the **displayed rounded percentages**. Calculating from the underlying order counts before rounding gives approximately **7.61 percentage points**. This is a minor rounding difference, not a different population.

These checks cover the displayed values and consistency with the published Olist aggregates; they are **not** an independent re-audit of the original eight CSV files.

## Interpretation limits

Delivery is measured against the **estimated customer delivery date**; a region is the **customer destination**, not the seller origin. Month-based charts use **purchase month**. The review difference is an association rather than proof of causation. Freight is the listed order-item amount, not independently audited carrier expense. Figures refer to **Brazil, 2016–2018, BRL**.

See the [analysis methods](../docs/08_technical_setup.md), [data quality checks](../docs/04_data_quality.md), and [management findings](../docs/10_delivery_performance_findings.md).
