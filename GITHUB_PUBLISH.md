# Repository publication and reproducibility

This repository contains the verified Stage 1 Olist supply-chain portfolio: an Excel workbook, a source-derived seller-state/city profile, original Python ETL code, tests, Business Analysis documents and GitHub Actions.

The full Olist transactional CSVs are **not** part of this repository. Before claiming order-level KPIs, download the original [Olist dataset](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce) into `data/raw` and run:

```bash
python scripts/process_olist.py --raw data/raw --output data/processed
python scripts/build_workbook.py --processed data/processed --output workbook/Olist_Order_Fulfilment_Intelligence.xlsx
python -m unittest discover -s tests -v
python scripts/verify_bundle.py
```

The ETL uses only the Python standard library. The optional workbook generator requires `artifact_tool`, which may not be present in standard Python environments. A successful GitHub Actions run validates the included tests and seller references; it does **not** imply the source Olist transactions have been downloaded or the full delivery dashboard regenerated.

Do not publish personally identifying source data; honour original data licences. Do not combine transactions from unrelated companies as though they belong to one operation.
