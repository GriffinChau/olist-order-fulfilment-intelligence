#!/usr/bin/env python3
"""Prepare two privacy-preserving Power BI facts from Olist original source.
Grain FactOrders: month x customer state x delivery outcome.
Grain FactItems: month x customer state x product category.
Conformed month/state dimensions permit accurate coordinated filtering of both facts.
No source order IDs, customer IDs or individual customer dates are published.
"""
import argparse,csv,json
from collections import defaultdict
from datetime import datetime
from decimal import Decimal
from pathlib import Path

def read(path):
    with Path(path).open(encoding="utf-8-sig",newline="") as f:
        yield from csv.DictReader(f)

def write(path,fields,rows):
    path.parent.mkdir(parents=True,exist_ok=True)
    with path.open("w",encoding="utf-8",newline="") as f:
        wr=csv.DictWriter(f,fieldnames=fields);wr.writeheader();wr.writerows(rows)

def build(raw,processed):
    k=json.loads((processed/"kpi_summary.json").read_text(encoding="utf-8"))
    stamps={}
    for r in read(raw/"olist_orders_dataset.csv"):
        stamps[r["order_id"]]=(r["order_purchase_timestamp"],r["order_delivered_customer_date"])
    orderkeys={}
    orders=defaultdict(lambda:{"Orders":0,"Delivered":0,"EligibleDeliveries":0,
        "OnTimeDeliveries":0,"LateDeliveries":0,"CancelledOrders":0,
        "LeadDaysSum":0.0,"LeadDaysCount":0,"ReviewedOrders":0,"ReviewScoreSum":0.0,"LowReviewOrders":0})
    for r in read(processed/"orders_enriched.csv"):
        oid=r["order_id"];month=r["purchase_month"];state=r["customer_state"].strip().upper() or "UNKNOWN"
        eligible=r["on_time_eligible"]=="1";ontime=eligible and r["on_time_flag"]=="1"
        outcome="On time" if ontime else ("Late" if eligible else "Not eligible")
        orderkeys[oid]=(month,state)
        group=orders[(month,state,outcome)]
        group["Orders"]+=1
        group["Delivered"]+=int(r["order_status"]=="delivered")
        group["EligibleDeliveries"]+=int(eligible)
        group["OnTimeDeliveries"]+=int(ontime)
        group["LateDeliveries"]+=int(eligible and not ontime)
        group["CancelledOrders"]+=int(r["order_status"] in ("canceled","cancelled"))
        if eligible:
            purchase,delivered=stamps[oid]
            delta=(datetime.fromisoformat(delivered)-datetime.fromisoformat(purchase)).total_seconds()/86400
            group["LeadDaysSum"]+=delta;group["LeadDaysCount"]+=1
        if r["review_score_avg"]:
            score=float(r["review_score_avg"])
            group["ReviewedOrders"]+=1
            group["ReviewScoreSum"]+=score
            group["LowReviewOrders"]+=int(score<=2)
    ordercols=["MonthKey","State","Outcome","Orders","Delivered","EligibleDeliveries",
        "OnTimeDeliveries","LateDeliveries","CancelledOrders","LeadDaysSum","LeadDaysCount",
        "ReviewedOrders","ReviewScoreSum","LowReviewOrders"]
    orderrows=[]
    for key,d in sorted(orders.items()):
        row=dict(zip(["MonthKey","State","Outcome"],key))
        row.update(d);row["LeadDaysSum"]=format(d["LeadDaysSum"],".8f")
        row["ReviewScoreSum"]=format(d["ReviewScoreSum"],".3f")
        orderrows.append(row)
    write(processed/"pbi_fact_orders.csv",ordercols,orderrows)

    products={r["product_id"]:(r["product_category_name"] or "unclassified")
              for r in read(raw/"olist_products_dataset.csv")}
    trans={r["product_category_name"]:r["product_category_name_english"]
           for r in read(raw/"product_category_name_translation.csv")}
    items=defaultdict(lambda:{"ItemLines":0,"ItemValueBRL":Decimal("0"),"FreightBRL":Decimal("0")})
    for r in read(raw/"olist_order_items_dataset.csv"):
        month,state=orderkeys[r["order_id"]]
        orig=products.get(r["product_id"],"unclassified")
        cat=trans.get(orig,orig)
        group=items[(month,state,cat)]
        group["ItemLines"]+=1
        group["ItemValueBRL"]+=Decimal(r["price"])
        group["FreightBRL"]+=Decimal(r["freight_value"])
    itemcols=["MonthKey","State","Category","ItemLines","ItemValueBRL","FreightBRL"]
    itemrows=[]
    for key,d in sorted(items.items()):
        row=dict(zip(["MonthKey","State","Category"],key))
        row.update({k:str(v) for k,v in d.items()})
        itemrows.append(row)
    write(processed/"pbi_fact_items.csv",itemcols,itemrows)
    def sumcol(rows,col):return sum(int(r[col]) for r in rows)
    qa={
      "orders":sumcol(orderrows,"Orders"),
      "eligible":sumcol(orderrows,"EligibleDeliveries"),
      "on_time":sumcol(orderrows,"OnTimeDeliveries"),
      "late":sumcol(orderrows,"LateDeliveries"),
      "canceled":sumcol(orderrows,"CancelledOrders"),
      "reviewed_on_time":sumcol((r for r in orderrows if r["Outcome"]=="On time"),"ReviewedOrders"),
      "reviewed_late":sumcol((r for r in orderrows if r["Outcome"]=="Late"),"ReviewedOrders"),
      "item_lines":sumcol(itemrows,"ItemLines"),
      "item_value":sum((Decimal(r["ItemValueBRL"]) for r in itemrows),Decimal("0")),
      "freight_value":sum((Decimal(r["FreightBRL"]) for r in itemrows),Decimal("0")),
    }
    assert qa["orders"]==k["orders"]
    assert qa["eligible"]==k["eligible_delivered_orders"]
    assert qa["on_time"]==k["on_time_deliveries"]
    assert qa["late"]==k["late_deliveries"]
    assert qa["canceled"]==k["cancelled_orders"]
    assert qa["item_lines"]==k["source_rows"]["items"]
    assert qa["item_value"]==Decimal(k["item_value_brl"])
    assert qa["freight_value"]==Decimal(k["freight_value_brl"])
    assert len({r["MonthKey"] for r in orderrows})>=20
    assert len({r["State"] for r in orderrows})>=20
    print("PASS PowerBI conformed facts:",len(orderrows),"order groups,",len(itemrows),"item groups")
    print("PASS aggregate source reconciliation:",{k:str(v) for k,v in qa.items()})
    return qa

if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--raw",type=Path,default=Path("data/raw"))
    p.add_argument("--processed",type=Path,default=Path("data/processed"))
    a=p.parse_args();build(a.raw,a.processed)
