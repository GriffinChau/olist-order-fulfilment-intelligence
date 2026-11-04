"""Source-derived Power BI fact constellation must reconcile with original Olist totals."""
import csv,json,unittest
from collections import defaultdict
from decimal import Decimal
from pathlib import Path
BASE=Path(__file__).resolve().parents[1]/"data"/"processed"
def load(name):
    with (BASE/name).open(newline="",encoding="utf-8") as f: return list(csv.DictReader(f))
class StarFactTests(unittest.TestCase):
    def test_source_reconciles(self):
        k=json.loads((BASE/"kpi_summary.json").read_text(encoding="utf-8"))
        orders=load("pbi_fact_orders.csv")
        items=load("pbi_fact_items.csv")
        self.assertEqual(sum(int(r["Orders"]) for r in orders),k["orders"])
        self.assertEqual(sum(int(r["EligibleDeliveries"]) for r in orders),k["eligible_delivered_orders"])
        self.assertEqual(sum(int(r["OnTimeDeliveries"]) for r in orders),k["on_time_deliveries"])
        self.assertEqual(sum(int(r["LateDeliveries"]) for r in orders),k["late_deliveries"])
        self.assertEqual(sum(int(r["CancelledOrders"]) for r in orders),k["cancelled_orders"])
        self.assertEqual(sum(int(r["ItemLines"]) for r in items),k["source_rows"]["items"])
        self.assertEqual(sum(Decimal(r["ItemValueBRL"]) for r in items),Decimal(k["item_value_brl"]))
        self.assertEqual(sum(Decimal(r["FreightBRL"]) for r in items),Decimal(k["freight_value_brl"]))
    def test_keys_are_safe_and_unique(self):
        orders=load("pbi_fact_orders.csv")
        items=load("pbi_fact_items.csv")
        self.assertEqual(len(orders),len({(r["MonthKey"],r["State"],r["Outcome"]) for r in orders}))
        self.assertEqual(len(items),len({(r["MonthKey"],r["State"],r["Category"]) for r in items}))
        self.assertTrue({r["Outcome"] for r in orders}<={"On time","Late","Not eligible"})
        self.assertEqual(set(orders[0]),{"MonthKey","State","Outcome","Orders","Delivered","EligibleDeliveries","OnTimeDeliveries","LateDeliveries","CancelledOrders","LeadDaysSum","LeadDaysCount","ReviewedOrders","ReviewScoreSum","LowReviewOrders"})
        self.assertEqual(set(items[0]),{"MonthKey","State","Category","ItemLines","ItemValueBRL","FreightBRL"})
        self.assertFalse("order_id" in orders[0] or "customer_id" in orders[0])
if __name__=="__main__":unittest.main()
