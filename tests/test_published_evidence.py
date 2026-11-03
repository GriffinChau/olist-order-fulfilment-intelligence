"""Check the published Olist source-derived aggregates for internal consistency."""
import csv
import json
import unittest
from decimal import Decimal
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]/"data"/"processed"

def load(name):
    return json.loads((ROOT/name).read_text(encoding="utf-8"))

def rows(name):
    with (ROOT/name).open(newline="",encoding="utf-8") as f:
        return list(csv.DictReader(f))

class TestPublishedSourceEvidence(unittest.TestCase):
    def test_orders_and_monthly_results(self):
        k=load("kpi_summary.json")
        m=rows("monthly_metrics.csv")
        self.assertEqual(k["orders"],99441)
        self.assertEqual(sum(int(x["orders"]) for x in m),k["orders"])
        self.assertEqual(sum(int(x["on_time_eligible"]) for x in m),k["eligible_delivered_orders"])
        self.assertEqual(sum(int(x["on_time_deliveries"]) for x in m),k["on_time_deliveries"])
        self.assertEqual(sum(int(x["late_deliveries"]) for x in m),k["late_deliveries"])
        self.assertEqual(k["on_time_deliveries"]+k["late_deliveries"],k["eligible_delivered_orders"])
        self.assertEqual(k["delivered_orders"]-k["eligible_delivered_orders"],8)
        self.assertEqual(k["cancelled_orders"],625)
        self.assertEqual(k["on_time_delivery_rate_pct"],round(100*k["on_time_deliveries"]/k["eligible_delivered_orders"],2))
    def test_geography_and_reviews(self):
        k=load("kpi_summary.json")
        r=rows("customer_region_summary.csv")
        v=rows("review_by_delivery.csv")
        self.assertEqual(sum(int(x["eligible_deliveries"]) for x in r),k["eligible_delivered_orders"])
        self.assertEqual(sum(int(x["late_deliveries"]) for x in r),k["late_deliveries"])
        self.assertEqual(sum(int(x["on_time_deliveries"]) for x in r),k["on_time_deliveries"])
        self.assertEqual(sum(int(x["eligible_deliveries"]) for x in v),k["eligible_delivered_orders"])
        self.assertEqual(len(v),2)
        self.assertTrue(all(int(x["reviewed_orders"])<=int(x["eligible_deliveries"]) for x in v))
    def test_category_and_freight(self):
        k=load("kpi_summary.json")
        cats=rows("category_summary.csv")
        self.assertEqual(sum(int(x["item_lines"]) for x in cats),k["source_rows"]["items"])
        self.assertEqual(sum((Decimal(x["item_value_brl"]) for x in cats),Decimal("0")),Decimal(k["item_value_brl"]))
        self.assertEqual(sum((Decimal(x["freight_brl"]) for x in cats),Decimal("0")),Decimal(k["freight_value_brl"]))
        self.assertTrue(k["qa"]["monthly_reconciles"])
        self.assertTrue(k["qa"]["category_aggregation_reconciles"])
        self.assertTrue(k["qa"]["item_aggregation_reconciles"])
    def test_provenance(self):
        p=load("PROVENANCE.json")
        self.assertEqual(p["source_publisher"],"Olist")
        self.assertTrue(p["original_commit_sha"])
        self.assertFalse(p["original_row_level_data_committed"])

if __name__=="__main__":
    unittest.main()
