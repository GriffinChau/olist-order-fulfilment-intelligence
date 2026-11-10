# Four-page Power BI report — visual specification

These are the **actual PBIR page names, visual types, field bindings, canvas dimensions and layout** in the local `Olist_PowerBI_PDF_Style` build. They are not fabricated screenshots of a finished Power BI Desktop export.

The design reference is [Olist Delivery Intelligence Report](../../reports/Olist_Delivery_Intelligence_Report.pdf). The Power BI report reproduces the **four content pages**, not a separate executive-summary tab.

## Common page layout

- **Canvas:** 1600 × 900, Fit to page.
- **Background:** light mint/grey with a dark green left sidebar, navigation labels, four white rounded KPI cards, two chart containers and two editorial takeaway panels.
- **Static resource:** one full-page PNG template per page (`olist_report_template_01.png` through `04.png`). It supplies the decorative chrome, card labels, explanatory copy and bottom business insights.
- **Dynamic resources:** each page overlays **4 Power BI `cardVisual` objects and 2 native Power BI charts**, using the semantic model and DAX. The KPI numbers and plotted bars/lines are not baked into the PNG.
- **Coordinates:** KPI number visuals start at `(302,198)`, `(633,198)`, `(964,198)` and `(1295,198)` with size `244 × 73`. The left chart is `(285,385)`, size `605 × 204`; the right chart is `(944,385)`, size `607 × 204`. All units are Power BI canvas pixels.
- **Color rules:** main teal `#0A988B`; exception orange `#D9854C`; theme includes `#078F81`, `#D88950` and pale background `#F2F8F5`. See [theme.json](theme.json).
- **Formatting:** headline cards use `Display ...` DAX measures (text returned by `FORMAT` where needed) so they show full counts such as `6,534` rather than Power BI's `7K` shorthand. Numeric chart measures remain numeric.

The report has **no global slicer**. Each small star branch works on a different summary grain, so making every page filter every other page would imply detail the sources do not contain.

## 01 Delivery performance

**KPI cards:** On-time delivery `FactKpi[Display On-time Delivery]` (**93.23%**); late `FactKpi[Display Late Deliveries]` (**6,534**); eligible `FactKpi[Display Eligible Deliveries]` (**96,470**); canceled `FactKpi[Display Canceled Orders]` (**625**).

| Visual | Native type | Axis | Measure | Rule |
|---|---|---|---|---|
| On-time rate by purchase month | Line chart | `DimMonth[month]` | `FactMonthly[On-time Rate (Report)]` | Jan 2017–Aug 2018, at least 500 eligible in a month |
| Late deliveries by month | Clustered column chart | `DimMonth[month]` | `FactMonthly[Late Deliveries (12m)]` | Sep 2017–Aug 2018; March 2018 highlighted |

**Narrative (static):** March 2018: **81.04% on time** with **1,328 late out of 7,003 eligible orders**. The “Period to Investigate” and “How to Read These Numbers” cards explain the exception and metric denominator.

## 02 Customer regions

**KPI cards:** Eligible **96,470**; São Paulo `FactRegion[Display SP Rate]` (**95.51%**); Rio de Janeiro `FactRegion[Display RJ Rate]` (**87.89%**); late **6,534**.

| Visual | Native type | Axis | Measure | Rule |
|---|---|---|---|---|
| On-time rate by state | Clustered bar chart | `DimState[state]` | `FactRegion[Top 8 On-time Rate by State]` | Top 8 **by eligible orders**, not by highest rate |
| Late deliveries by state | Clustered bar chart | `DimState[state]` | `FactRegion[Top 8 Late by State]` | Same top 8 by eligible orders |

`FactRegion[State Accent Color]` assigns orange to **RJ and BA** and teal otherwise where conditional formatting uses the measure. State describes **customer destination**, not seller origin. The PDF's **7.62 percentage-point gap** subtracts displayed rounded rates (95.51 − 87.89).

## 03 Customer experience

**KPI cards:** `FactReviews[Display On-time Review]` (**4.29 / 5**); `FactReviews[Display Late Review]` (**2.27 / 5**); `FactReviews[Display Low Rating On-time]` (**9.23%**); `FactReviews[Display Low Rating Late]` (**62.36%**).

| Visual | Native type | Axis | Measure | Rule |
|---|---|---|---|---|
| Average customer review score | Clustered bar chart | `DimDeliveryOutcome[delivery_display]` | `FactReviews[Avg Review Score]` | Weighted by reviewed orders |
| Share of low customer ratings | Clustered bar chart | `DimDeliveryOutcome[delivery_display]` | `FactReviews[Low Rating Share]` | Ratings 1 or 2 of 5 |

The display column changes `on_time` to “On time or early” and `late` to “Late delivery.” `FactReviews[Review Accent Color]` highlights late outcomes in orange. There are **89,443 reviewed on-time orders** and **6,381 reviewed late orders** (**95,824** total). Differences are **associations, not proof that delays caused lower reviews**.

## 04 Product and freight

**KPI cards:** `FactKpi[Display Item Value]` (**BRL 13.59M**); `FactKpi[Display Listed Freight]` (**BRL 2.26M**); `FactKpi[Display Freight Ratio]` (**16.60%**); `FactCategory[Display Item Lines]` (**112,650**).

| Visual | Native type | Axis | Measure | Rule |
|---|---|---|---|---|
| Largest categories by item value | Clustered bar chart | `DimCategory[category_display]` | `FactCategory[Top 8 Item Value]` | Rank categories by total item value |
| Freight as a share of item value | Clustered bar chart | `DimCategory[category_display]` | `FactCategory[Top 8 Freight to Item Rate]` | **Same eight categories**, not top eight freight ratios |

`FactCategory[Category Accent Color]` highlights furniture & decor and housewares in orange where conditional formatting is applied. Friendly category labels are generated in Power Query. Freight is an amount listed in the source, **not an audited logistics invoice**.

## How the pages were built

1. Create the **nine-table Import model** and **56 DAX measures** described in [semantic_model.md](semantic_model.md) and [measures.dax](measures.dax).
2. Create four pages named as above at **1600 × 900**.
3. Place one PDF-inspired **static image template** on each page as its full-canvas background; place native card/chart visuals on top at the recorded coordinates.
4. Bind each visual to the exact DAX measures in the tables above. Use the friendly dimension display columns where indicated.
5. Apply the green/orange theme; set categorical ranking, report time windows, no auto-abbreviation on headline numbers and appropriate axis bounds.
6. Refresh in Power BI Desktop, check each KPI against the repository source aggregates, then **export and visually inspect** the four-page PDF.

**Honest reproducibility boundary:** This GitHub folder publishes **model calculations, table relationships, page layout/bindings and the theme**. It does not contain the editable PBIX, full PBIR page JSON or generated background PNG resources. These notes explain and document the local report, but are not a drop-in replacement for the local Power BI project. The PDF in `reports/` is the **visual reference**; it should not be presented as a Power BI export unless that export has actually been checked.
