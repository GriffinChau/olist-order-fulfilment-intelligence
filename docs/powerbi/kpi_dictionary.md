# KPI dictionary and validation checks

Values are from the project's [published Olist aggregate sources](../../data/processed/) (Brazil, 2016–2018; currency BRL). The **numeric DAX measures** are in [measures.dax](measures.dax). The **`Display ...` measures** turn them into human-readable text for KPI cards; they are not used to compute chart heights.

## All-time KPI cards

| Metric | Definition and source | Numeric measure | Expected |
|---|---|---|---:|
| Historical customer orders | Unique source order IDs, `FactKpi[orders]` | `FactKpi[Total Orders]` | **99,441** |
| Delivered orders | Delivered order-status count, `FactKpi[delivered_orders]` | Source column / QA reference | **96,478** |
| Delivery-eligible orders | Delivered and both actual + estimate dates available | `FactKpi[Total Eligible Deliveries]` | **96,470** |
| On-time deliveries | Eligible delivered orders with actual date ≤ estimated customer date | `FactKpi[Total On-time Deliveries]` | **89,936** |
| Late deliveries | Eligible delivered orders after estimated customer date | `FactKpi[Total Late Deliveries]` | **6,534** |
| On-time rate | On-time / eligible | `FactKpi[Total On-time Rate]` | **93.23%** |
| Late rate | Late / eligible | `[Total Late Deliveries] / [Total Eligible Deliveries]` | **6.77%** |
| Canceled orders | Source order-status count | `FactKpi[Total Canceled Orders]` | **625** |
| Cancellation share | Canceled / all customer orders (not eligible orders) | `FactKpi[Total Cancellation Rate]` | **0.63%** |
| Item value | Sum of original item `price` | `FactKpi[Total Item Value]` | **BRL 13,591,643.70** |
| Listed freight | Sum of original item `freight_value` | `FactKpi[Total Listed Freight]` | **BRL 2,256,599.44** |
| Freight-to-item ratio | Listed freight / item value | `FactKpi[Total Freight to Item Rate]` | **16.60%** |
| Order-item lines | Number of original item rows | `FactCategory[Order Item Lines]` | **112,650** |

**Calculation note:** `96,478 - 96,470 = 8` delivered orders are excluded from on-time denominator because the actual delivery date is missing. Numerator and denominator must be defined at **order grain**, not item or payment row grain.

## Purchase-month measures

| Measure | Computation / usage | Published checkpoint |
|---|---|---|
| `FactMonthly[Eligible Deliveries]` | `SUM(FactMonthly[on_time_eligible])` | 96,470 across full source |
| `FactMonthly[On-time Deliveries]` | `SUM(FactMonthly[on_time_deliveries])` | 89,936 |
| `FactMonthly[Late Deliveries]` | `SUM(FactMonthly[late_deliveries])` | 6,534 |
| `FactMonthly[On-time Rate]` | On-time / eligible; calculate from counts | 93.23% overall |
| `FactMonthly[On-time Rate (Report)]` | Jan 2017–Aug 2018, eligible ≥ 500 | March 2018: **81.04%** |
| `FactMonthly[Late Deliveries (12m)]` | Sep 2017–Aug 2018 | March 2018: **1,328** |

March 2018 has **7,003 eligible deliveries**, **5,675 on time**, **1,328 late**. The source's final tiny September/October 2018 cohorts have no eligible deliveries, so they must not become zero-valued points on an on-time line.

## Regional measures

`FactRegion[On-time Rate by State] = DIVIDE([On-time by State], [Eligible by State])`. Do **not** take an unweighted average of state percentages.

| Customer destination | Eligible | On time | Late | Published rate |
|---|---:|---:|---:|---:|
| São Paulo (SP) | 40,494 | 38,674 | 1,820 | **95.51%** |
| Rio de Janeiro (RJ) | 12,350 | 10,855 | 1,495 | **87.89%** |
| Bahia (BA) | 3,256 | 2,860 | 396 | **87.84%** |

The report compares SP and RJ as **7.62 percentage points using their displayed, rounded rates**; subtraction using unrounded rates can differ slightly. `Top 8...` state measures rank by **eligible delivery count**, not best/worst performance.

## Customer review measures

Review outcomes are grouped at **one reviewed order**, after averaging multiple valid review events associated with a given order. The published grouped means are rounded.

| Delivery outcome | Reviewed orders | Average review / 5 | Share rated 1 or 2 |
|---|---:|---:|---:|
| On time or early | 89,443 | **4.29** | **9.23%** |
| Late | 6,381 | **2.27** | **62.36%** |
| Total | **95,824** | Weighted calculation | Weighted calculation |

`Avg Review Score` uses `SUMX(FactReviews, avg_review_score * reviewed_orders) / SUM(reviewed_orders)`. `Low Rating Share` similarly weights `low_review_share_pct`, then divides by 100. This produces a reasonable aggregate measure from the **rounded** grouped statistics and does not reconstruct exact raw-review events. The review gap is **associational**, not a causal estimate.

## Category / freight measures

`FactCategory[Item Value] = SUM(FactCategory[item_value_brl])` and `Freight to Item Rate = [Listed Freight] / [Item Value]`.

The two category charts use the **same eight categories by item value**. Examples of category-specific freight ratios:

| Category | Freight / item |
|---|---:|
| Health & beauty | 14.52% |
| Watches & gifts | 8.34% |
| Bed, bath & table | 19.74% |
| Furniture & decor | **23.77%** |
| Housewares | **23.26%** |

`FactCategory[order_count_attributed]` must **not** be summed to report unique orders across product categories. Item categories can overlap within the same order. Listed freight is a **dataset amount**, not an independently reconciled shipping expense paid to a carrier.

## Source and QA references

- [Source KPI snapshot](../../data/processed/kpi_summary.json)
- [Monthly aggregate](../../data/processed/monthly_metrics.csv)
- [Customer-state aggregate](../../data/processed/customer_region_summary.csv)
- [Delivery/review aggregate](../../data/processed/review_by_delivery.csv)
- [Category aggregate](../../data/processed/category_summary.csv)
- [Python QA and reconciliation](../04_data_quality.md)
- [Power BI page bindings](report_pages.md)
