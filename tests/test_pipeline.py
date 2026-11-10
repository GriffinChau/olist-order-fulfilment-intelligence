import csv
import json
import tempfile
import unittest
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from process_olist import build
from summarise_delivery_experience import aggregate
from check_processed_outputs import verify

class TestPipeline(unittest.TestCase):
    def test_reference_profile_reconciles(self):
        path=Path(__file__).resolve().parents[1]/'data/reference/olist_seller_state_profile.csv'
        with path.open(newline='') as h: rows=list(csv.DictReader(h))
        self.assertEqual(sum(int(x['seller_count']) for x in rows),3095)
        self.assertEqual(len(rows),23)

    def test_source_schema_and_no_many_to_many_inflation(self):
        # Unit test fixtures below are explicitly synthetic and are NOT business evidence.
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);raw=root/'raw';raw.mkdir();out=root/'out'
            def write(name,header,rows):
                with (raw/name).open('w',newline='') as f:
                    w=csv.writer(f);w.writerow(header);w.writerows(rows)
            write('olist_orders_dataset.csv',['order_id','customer_id','order_status','order_purchase_timestamp','order_delivered_customer_date','order_estimated_delivery_date'],[
                ['o1','c1','delivered','2018-01-01 10:00:00','2018-01-06 10:00:00','2018-01-07 00:00:00'],
                ['o2','c1','delivered','2018-01-02 10:00:00','2018-01-09 10:00:00','2018-01-07 00:00:00'],
                ['o3','c1','canceled','2018-01-03 10:00:00','','2018-01-10 00:00:00']])
            write('olist_order_items_dataset.csv',['order_id','order_item_id','product_id','seller_id','price','freight_value'],[
                ['o1','1','p1','s1','10.00','1.00'],['o1','2','p1','s1','20.00','2.00'],['o2','1','p1','s1','30.00','3.00']])
            write('olist_order_payments_dataset.csv',['order_id','payment_value','payment_type'],[
                ['o1','10.00','credit_card'],['o1','23.00','voucher'],['o2','33.00','credit_card']])
            write('olist_order_reviews_dataset.csv',['order_id','review_score'],[['o1','5'],['o1','4'],['o2','1']])
            write('olist_products_dataset.csv',['product_id','product_category_name'],[['p1','automotivo']])
            write('olist_sellers_dataset.csv',['seller_id','seller_city','seller_state'],[['s1','sao paulo','SP']])
            write('olist_customers_dataset.csv',['customer_id','customer_state'],[['c1','SP']])
            write('product_category_name_translation.csv',['product_category_name','product_category_name_english'],[['automotivo','auto']])
            x=build(raw,out)
            self.assertEqual(x['orders'],3)
            self.assertEqual(x['cancelled_orders'],1)
            self.assertEqual(x['cancellation_rate_pct'],33.33)
            self.assertEqual(x['eligible_delivered_orders'],2)
            self.assertEqual(x['on_time_deliveries'],1)
            self.assertEqual(x['on_time_delivery_rate_pct'],50.0)
            self.assertEqual(x['item_value_brl'],'60.00')
            self.assertEqual(x['payment_value_brl'],'66.00')
            self.assertTrue(x['qa']['item_aggregation_reconciles'])
            self.assertEqual(x['source_rows']['payments'],3)
            self.assertEqual(x['source_rows']['reviews'],3)
            with (out/'orders_enriched.csv').open(newline='') as h:
                enriched=list(csv.DictReader(h))
            self.assertEqual(enriched[0]['item_value_brl'],'30.00')
            self.assertEqual(enriched[0]['review_score_avg'],'4.5')
            self.assertEqual(enriched[0]['payment_value_brl'],'33.00')
            # Verify that the previously omitted pipeline stage actually runs
            # against fresh output, and that all newly derived aggregates reconcile.
            self.assertEqual(aggregate(out/'orders_enriched.csv',out),2)
            with (out/'customer_region_summary.csv').open(newline='') as h:
                states=list(csv.DictReader(h))
            self.assertEqual(len(states),1)
            self.assertEqual(states[0]['state'],'SP')
            self.assertEqual(int(states[0]['eligible_deliveries']),2)
            with (out/'review_by_delivery.csv').open(newline='') as h:
                delivery_reviews={r['delivery_outcome']:r for r in csv.DictReader(h)}
            self.assertEqual(delivery_reviews['on_time']['avg_review_score'],'4.50')
            self.assertEqual(delivery_reviews['late']['avg_review_score'],'1.00')
            self.assertTrue(verify(out))
if __name__=='__main__':unittest.main()
