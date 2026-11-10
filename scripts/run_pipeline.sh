#!/usr/bin/env sh
# Rebuild the analytical outputs from Olist's original eight CSV files.
# Set BUILD_WORKBOOK=0 to run without the optional artifact_tool dependency.
set -eu
cd "$(dirname "$0")/.."
PYTHON="${PYTHON:-python3}"
RAW_DIR="${RAW_DIR:-data/raw}"
PROCESSED_DIR="${PROCESSED_DIR:-data/processed}"
WORKBOOK_OUTPUT="${WORKBOOK_OUTPUT:-workbook/Olist_Order_Fulfilment_Intelligence_Rebuilt.xlsx}"

"$PYTHON" scripts/process_olist.py --raw "$RAW_DIR" --output "$PROCESSED_DIR"
"$PYTHON" scripts/summarise_delivery_experience.py --orders "$PROCESSED_DIR/orders_enriched.csv" --output "$PROCESSED_DIR"
"$PYTHON" scripts/check_processed_outputs.py --processed "$PROCESSED_DIR"
"$PYTHON" -m unittest discover -s tests -v
"$PYTHON" scripts/verify_bundle.py

if [ "${BUILD_WORKBOOK:-1}" = "1" ]; then
  "$PYTHON" scripts/build_workbook.py --processed "$PROCESSED_DIR" --output "$WORKBOOK_OUTPUT"
  printf '\nRebuilt reporting workbook: %s\n' "$WORKBOOK_OUTPUT"
  printf 'Note: this is the script-generated edition, not a pixel-identical reproduction of the curated 16-sheet portfolio workbook.\n'
else
  printf '\nSkipped optional workbook generation (BUILD_WORKBOOK=0).\n'
fi
printf 'Reconciled aggregates: %s\n' "$PROCESSED_DIR"
