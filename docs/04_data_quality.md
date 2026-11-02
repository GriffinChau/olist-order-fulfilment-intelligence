# Data quality and acceptance testing

## Verified published reference
- 3,095 marketplace seller records and 3,095 distinct seller IDs across 23 Brazilian state codes.
- São Paulo (SP): 1,849 seller IDs, around 59.7%.
- Seller-state counts reconcile to 3,095.
- The processing script has a unit test with deliberately **synthetic test fixtures** covering two item lines, two payments and multiple reviews for a single order. Test fixtures must not be confused with the real dataset.

## Checks after importing full source
The pipeline reports unmatched order references for items, payments and reviews, missing linked products/sellers/customers, missing actual/estimated delivered dates, unique order IDs, monthly counts and rollup reconciliations.

Missing data are reported rather than imputed, and unmatched references require investigation. A passing unit test does not mean that every real transaction has been audited.

## Review checklist
- [ ] Source Olist CSVs match the documented release.
- [ ] Order counts reconcile to monthly aggregation.
- [ ] Item value reconciles to seller and category rollups.
- [ ] Payment totals are not multiplied through order item joins.
- [ ] All delivery rates include denominator and date coverage.
- [ ] Unsupported upstream OTIF, supplier spend and inventory measures are not claimed.
- [ ] Excel dashboard is rebuilt only after verifying generated files.

Run `python -m unittest discover -s tests -v`.
