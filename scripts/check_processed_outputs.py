#!/usr/bin/env python3
"""Verify fresh, independently generated Olist aggregates (not a financial audit)."""
import argparse
import csv
import json
from decimal import Decimal
from pathlib import Path


def rows(path):
    with path.open(newline="", encoding="utf-8") as stream:
        return list(csv.DictReader(stream))


def verify(processed):
    processed = Path(processed)
    k = json.loads((processed / "kpi_summary.json").read_text(encoding="utf-8"))
    assert k["data_status"] == "FULL_OLIST_DATA_LOADED", "Full Olist source was not loaded"
    assert k["on_time_deliveries"] + k["late_deliveries"] == k["eligible_delivered_orders"]
    for name in ("unique_order_ids", "monthly_reconciles", "item_aggregation_reconciles",
                 "category_aggregation_reconciles"):
        assert k["qa"].get(name) is True, f"Source QA failed: {name}"

    months = rows(processed / "monthly_metrics.csv")
    assert sum(int(r["orders"]) for r in months) == k["orders"], "Monthly order reconciliation"
    for field, metric in (("on_time_eligible", "eligible_delivered_orders"),
                          ("on_time_deliveries", "on_time_deliveries"),
                          ("late_deliveries", "late_deliveries")):
        assert sum(int(r[field]) for r in months) == k[metric], f"Monthly reconciliation: {metric}"
    for r in months:
        assert int(r["on_time_deliveries"]) + int(r["late_deliveries"]) == int(r["on_time_eligible"])

    states = rows(processed / "customer_region_summary.csv")
    assert sum(int(r["eligible_deliveries"]) for r in states) == k["eligible_delivered_orders"]
    assert sum(int(r["on_time_deliveries"]) for r in states) == k["on_time_deliveries"]
    assert sum(int(r["late_deliveries"]) for r in states) == k["late_deliveries"]

    reviews = rows(processed / "review_by_delivery.csv")
    assert {r["delivery_outcome"] for r in reviews} == {"on_time", "late"}
    assert sum(int(r["eligible_deliveries"]) for r in reviews) == k["eligible_delivered_orders"]
    for r in reviews:
        expected = k["on_time_deliveries"] if r["delivery_outcome"] == "on_time" else k["late_deliveries"]
        assert int(r["eligible_deliveries"]) == expected
        assert int(r["reviewed_orders"]) <= expected

    categories = rows(processed / "category_summary.csv")
    assert sum(int(r["item_lines"]) for r in categories) == k["source_rows"]["items"]
    assert sum((Decimal(r["item_value_brl"]) for r in categories), Decimal("0")) == Decimal(k["item_value_brl"])
    assert sum((Decimal(r["freight_brl"]) for r in categories), Decimal("0")) == Decimal(k["freight_value_brl"])

    print(json.dumps({"orders": k["orders"], "eligible_deliveries": k["eligible_delivered_orders"],
                      "late_deliveries": k["late_deliveries"], "source_reconciliations": "PASS"}, indent=2))
    return True


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--processed", type=Path, default=Path("data/processed"))
    args = parser.parse_args()
    verify(args.processed)
