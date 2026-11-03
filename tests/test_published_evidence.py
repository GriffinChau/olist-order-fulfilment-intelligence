"""Validate consistency of publicly published Olist aggregates.

These checks reconcile summary data, not the original source CSV bytes.
Source transformation scripts are available under scripts/.
"""
import csv
import json
import unittest
from decimal import Decimal
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "evidence"


def load_json(filename):
    return json.loads((EVIDENCE / filename).read_text(encoding="utf-8"))


class TestPublishedEvidence(unittest.TestCase):
    def test_delivery_orders_monthly_reconcile(self):
        d = load_json("order_delivery_kpis.json")
        with (EVIDENCE / "monthly_delivery_summary.csv").open(newline="", encoding="utf-8") as fh:
            monthly = list(csv.DictReader(fh))
        self.assertEqual(len(monthly), 25)
        self.assertEqual(sum(int(r["orders"]) for r in monthly), 99441)
        self.assertEqual(sum(int(r["eligible"]) for r in monthly), 96470)
        self.assertEqual(sum(int(r["on_time"]) for r in monthly), 89936)
        self.assertEqual(sum(int(r["late"]) for r in monthly), 6534)
        self.assertEqual(d["eligible_delivered_orders"], d["on_time_deliveries"] + d["late_deliveries"])
        self.assertEqual(round(100 * d["on_time_deliveries"] / d["eligible_delivered_orders"], 2), d["on_time_delivery_rate_pct"])
        self.assertEqual(d["delivered_orders"] - d["eligible_delivered_orders"], d["qa"]["missing_actual_for_delivered"])

    def test_delivery_state_and_reviews_reconcile(self):
        d = load_json("delivery_by_state_and_reviews.json")
        self.assertEqual(sum(r["eligible"] for r in d["state_delivery"]), 96470)
        self.assertEqual(sum(r["late"] for r in d["state_delivery"]), 6534)
        self.assertEqual(sum(r["on_time"] for r in d["state_delivery"]), 89936)
        self.assertEqual(sum(r["order_count"] for r in d["review_groups"]), 96470)
        self.assertEqual(d["review_records"], 99224)
        self.assertTrue(all(0 <= r["average_score"] <= 5 for r in d["review_groups"]))

    def test_item_value_and_freight_reconcile(self):
        doc = load_json("commercial_kpis.json")
        d = doc["summary"]
        self.assertEqual(d["item_rows"], 112650)
        self.assertEqual(d["seller_reference_records"], 3095)
        self.assertEqual(len(doc["categories"]), d["categories"])
        self.assertEqual(sum(Decimal(r["item_value_brl"]) for r in doc["categories"]), Decimal(d["item_value_brl"]))
        self.assertEqual(sum(Decimal(r["freight_value_brl"]) for r in doc["categories"]), Decimal(d["freight_value_brl"]))
        self.assertTrue(d["qa"]["category_totals_match"])
        self.assertTrue(d["qa"]["seller_totals_match"])

    def test_customer_payment_scope(self):
        p = load_json("customer_payment_kpis.json")
        self.assertEqual(p["rows"], 103886)
        self.assertEqual(sum(x["rows"] for x in p["by_payment_method"]), p["rows"])
        self.assertEqual(sum(Decimal(x["value_brl"]) for x in p["by_payment_method"]), Decimal(p["total_customer_payment_value_brl"]))


if __name__ == "__main__":
    unittest.main()
