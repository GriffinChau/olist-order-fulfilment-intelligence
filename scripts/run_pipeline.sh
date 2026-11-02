#!/usr/bin/env sh
set -eu
cd "$(dirname "$0")/.."
python scripts/process_olist.py --raw data/raw --output data/processed
python scripts/build_workbook.py --processed data/processed --output workbook/Olist_Order_Fulfilment_Intelligence.xlsx
python -m unittest discover -s tests -v
printf '\nProject ready. Workbook: workbook/Olist_Order_Fulfilment_Intelligence.xlsx\n'
