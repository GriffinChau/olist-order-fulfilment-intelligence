#!/usr/bin/env python3
"""Order-level geographic delivery and review aggregates from verified Olist outputs.

No original customer or order IDs are written into publication outputs.
"""
import argparse
import csv
from collections import defaultdict
from pathlib import Path

def aggregate(input_file, out):
    stats=defaultdict(lambda:{"eligible":0,"on_time":0,"late":0,"late_days":0})
    reviews=defaultdict(lambda:{"eligible":0,"reviewed":0,"score_sum":0.0,"low":0})
    eligible=0
    with Path(input_file).open(newline="",encoding="utf-8") as stream:
        for row in csv.DictReader(stream):
            if row["on_time_eligible"]!="1":
                continue
            eligible+=1
            state=row["customer_state"].strip().upper() or "UNKNOWN"
            ontime=row["on_time_flag"]=="1"
            d=stats[state]
            d["eligible"]+=1
            d["on_time" if ontime else "late"]+=1
            if not ontime:
                d["late_days"]+=max(0,int(row["delivery_days_from_estimate"]))
            group=reviews["on_time" if ontime else "late"]
            group["eligible"]+=1
            if row["review_score_avg"]:
                score=float(row["review_score_avg"])
                if not (1<=score<=5):
                    raise ValueError("Unexpected review score outside 1-5 range")
                group["reviewed"]+=1
                group["score_sum"]+=score
                group["low"]+=int(score<=2)
    assert sum(x["eligible"] for x in stats.values())==eligible
    assert sum(x["eligible"] for x in reviews.values())==eligible
    out=Path(out);out.mkdir(parents=True,exist_ok=True)
    with (out/"customer_region_summary.csv").open("w",newline="",encoding="utf-8") as stream:
        wr=csv.writer(stream)
        wr.writerow(["state","eligible_deliveries","on_time_deliveries","late_deliveries","on_time_pct","avg_late_days"])
        for state,d in sorted(stats.items(),key=lambda x:-x[1]["eligible"]):
            wr.writerow([state,d["eligible"],d["on_time"],d["late"],
                         f'{100*d["on_time"]/d["eligible"]:.2f}',
                         f'{d["late_days"]/d["late"]:.2f}' if d["late"] else ""])
    with (out/"review_by_delivery.csv").open("w",newline="",encoding="utf-8") as stream:
        wr=csv.writer(stream)
        wr.writerow(["delivery_outcome","eligible_deliveries","reviewed_orders","review_coverage_pct","avg_review_score","low_review_share_pct"])
        for label in ["on_time","late"]:
            d=reviews[label]
            wr.writerow([label,d["eligible"],d["reviewed"],
                         f'{100*d["reviewed"]/d["eligible"]:.2f}' if d["eligible"] else "",
                         f'{d["score_sum"]/d["reviewed"]:.2f}' if d["reviewed"] else "",
                         f'{100*d["low"]/d["reviewed"]:.2f}' if d["reviewed"] else ""])
    print(f"Analysed {eligible:,} eligible deliveries across {len(stats)} customer states")
    return eligible

if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--orders",type=Path,default=Path("data/processed/orders_enriched.csv"))
    p.add_argument("--output",type=Path,default=Path("data/processed"))
    a=p.parse_args()
    aggregate(a.orders,a.output)
