#!/usr/bin/env python3
"""Publish the public Olist BI portfolio as a crisp, vector four-page PDF.

Source is the reconciled Olist public aggregate files already present in GitHub.
This script publishes NO Power BI (.pbip/.pbix) project or original customer records.
"""
from __future__ import annotations
import csv,json,math,sys
from pathlib import Path
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"reports"/"Olist_PowerBI_Report.pdf"
DATA=ROOT/"data"/"processed"
W,H=1476,846
NAVY="#152B42"; TEAL="#0C918A"; PALE="#F3F7FA"; BLUE="#365E84"
AMBER="#D88A53"; INK="#23394C"; MUTED="#63798B"; LIGHT="#E6EDF3"
WHITE="#FFFFFF"; GREEN="#E6F5F1"; TEXT="#39556C"

def loadcsv(name):
    with (DATA/name).open(encoding="utf-8",newline="") as f:
        return list(csv.DictReader(f))
k=json.loads((DATA/"kpi_summary.json").read_text(encoding="utf-8"))
months=loadcsv("monthly_metrics.csv")
states=loadcsv("customer_region_summary.csv")
reviews={r["delivery_outcome"]:r for r in loadcsv("review_by_delivery.csv")}
cats=loadcsv("category_summary.csv")
assert int(k["orders"])==99441 and int(k["eligible_delivered_orders"])==96470
assert int(k["on_time_deliveries"])+int(k["late_deliveries"])==96470
assert sum(int(x["orders"]) for x in months)==k["orders"]
assert sum(int(x["eligible_deliveries"]) for x in states)==k["eligible_delivered_orders"]
assert len(cats)>=10

def fill(c,color): c.setFillColor(HexColor(color))
def stroke(c,color): c.setStrokeColor(HexColor(color))
def rect(c,x,y,w,h,color,rad=0,border=None):
    fill(c,color)
    if border: stroke(c,border)
    c.roundRect(x,y,w,h,rad,fill=1,stroke=1 if border else 0)

def txt(c,x,y,s,size=16,color=INK,bold=False):
    c.setFont("Helvetica-Bold" if bold else "Helvetica",size)
    fill(c,color)
    c.drawString(x,y,str(s))

def right(c,x,y,s,size=16,color=INK,bold=False):
    c.setFont("Helvetica-Bold" if bold else "Helvetica",size)
    fill(c,color);c.drawRightString(x,y,str(s))

def truncate(c,s,maxw,size=14,bold=False):
    font="Helvetica-Bold" if bold else "Helvetica"
    s=str(s).replace("_"," ")
    while s and c.stringWidth(s,font,size)>maxw:s=s[:-1]
    return s if s==str(s).replace("_"," ") else s.rstrip()+"..."

def basic(c,title,subtitle,num):
    rect(c,0,0,W,H,PALE)
    rect(c,0,H-141,W,141,NAVY)
    rect(c,45,H-114,9,72,TEAL,4)
    txt(c,69,H-49,"OLIST  /  CUSTOMER FULFILMENT INTELLIGENCE",18,"#C7DDE6",True)
    txt(c,69,H-96,title,33,WHITE,True)
    txt(c,70,H-124,subtitle,14,"#C7DDE6")
    rect(c,W-210,H-91,154,34,"#244966",7)
    txt(c,W-193,H-80,"BRAZIL  |  2016-18",12,WHITE,True)
    rect(c,45,35,W-90,39,WHITE,7,border=LIGHT)
    txt(c,59,49,"SOURCE  Olist Brazilian e-commerce data  |  Historical public records  |  Customer-side measures  |  BRL",12,MUTED)
    right(c,W-64,49,f"{num} / 4",12,MUTED,True)

def cards(c,rows):
    gap=18; x0=45; total=W-90; cw=(total-gap*3)/4
    for i,(head,value,detail) in enumerate(rows):
        x=x0+i*(cw+gap)
        rect(c,x,550,cw,130,WHITE,14,border=LIGHT)
        rect(c,x+16,568,6,92,AMBER if i==2 else TEAL,3)
        txt(c,x+35,646,head.upper(),14,MUTED,True)
        txt(c,x+35,594,value,35,INK,True)
        txt(c,x+35,570,detail,12,MUTED)

def panel(c,x,y,w,h,title,subtitle=""):
    rect(c,x,y,w,h,WHITE,15,border=LIGHT)
    txt(c,x+24,y+h-40,title,19,INK,True)
    if subtitle:txt(c,x+24,y+h-63,subtitle,12,MUTED)

def xaxis(c,x,y,w,ticks,maxv,pct=False):
    for i in range(ticks+1):
        v=maxv*i/ticks; xx=x+w*i/ticks
        stroke(c,LIGHT);c.setLineWidth(1)
        c.line(xx,y,xx,y+295)
        lab=(f"{v:.0f}%" if pct else f"{v:,.0f}")
        txt(c,xx-6,y-22,lab,11,MUTED)

def hbars(c,data,x,y,w,h,scale_max,kind="count",labels_limit=200):
    # data: [(label, value)], laid out top to bottom; label area 188.
    plotx=x+204; plotw=w-306; rowh=min(41,h/max(len(data),1))
    top=y+h-8
    for i,(label,val) in enumerate(data):
        yy=top-i*rowh
        txt(c,x+18,yy-5,truncate(c,label,185,13),13,TEXT)
        barw=min(plotw,max(1,plotw*float(val)/scale_max))
        rect(c,plotx,yy-9,plotw,20,LIGHT,5)
        rect(c,plotx,yy-9,barw,20,AMBER if (kind=="rate" and val<90) else TEAL,5)
        pretty=f"{val:.2f}%" if kind=="rate" else (f"BRL {val/1e6:.2f}M" if kind=="money" else f"{val:,.0f}")
        right(c,x+w-12,yy-4,pretty,13,INK,True)

def line(c,data,x,y,w,h,mn=75,mx=100):
    points=[]
    left=x+42; right=x+w-22; bottom=y+38; top=y+h-20
    for tick in [80,85,90,95,100]:
        py=bottom+(tick-mn)/(mx-mn)*(top-bottom)
        stroke(c,LIGHT);c.setLineWidth(0.8);c.line(left,py,right,py)
        rightf=f"{tick}%";right(c,left-10,py-4,rightf,11,MUTED)
    for i,(label,val) in enumerate(data):
        px=left+i*(right-left)/max(len(data)-1,1)
        py=bottom+(max(mn,min(mx,val))-mn)/(mx-mn)*(top-bottom)
        points.append((px,py))
        if i%2==0:
            txt(c,px-18,bottom-28,label[-5:],10,MUTED)
    stroke(c,TEAL);c.setLineWidth(3)
    for a,b in zip(points,points[1:]):c.line(a[0],a[1],b[0],b[1])
    for px,py in points:
        fill(c,TEAL);c.circle(px,py,4,fill=1,stroke=0)

def vbars(c,data,x,y,w,h):
    maxv=max([v for _,v in data] or [1])*1.08
    left=x+15; bottom=y+35; top=y+h-25
    gap=8; bw=(w-60)/len(data)-gap
    for i,(label,val) in enumerate(data):
        xx=left+i*((w-60)/len(data))
        bh=(top-bottom)*val/maxv
        rect(c,xx,bottom,max(5,bw),bh,AMBER if label=="2018-03" else TEAL,4)
        if i%2==0:txt(c,xx,bottom-24,label[-5:],10,MUTED)
        if val>=900:right(c,xx+bw,bottom+bh+10,f"{val:,}",10,INK,True)

def summary(c,y,left,righttxt):
    rect(c,45,y,W-90,45,GREEN,9)
    txt(c,61,y+16,left,15,INK,True)
    txt(c,675,y+16,righttxt,12,TEXT)

def draw_delivery(c):
    basic(c,"When do deliveries fall behind?","Monthly service reliability and delayed-order volume, measured by purchase cohort.",1)
    cards(c,[("On-time delivery",f'{k["on_time_delivery_rate_pct"]:.2f}%',"Eligible delivered orders"),
             ("Late delivered orders",f'{k["late_deliveries"]:,}',"After estimated customer date"),
             ("Eligible deliveries",f'{k["eligible_delivered_orders"]:,}',"Both actual and estimated dates"),
             ("Canceled orders",f'{k["cancelled_orders"]:,}',"Observed order status")])
    data=[r for r in months if int(r["on_time_eligible"])>=500][-12:]
    p1=(45,140,673,388);p2=(738,140,693,388)
    panel(c,*p1,"ON-TIME DELIVERY RATE","Most recent 12 substantial monthly cohorts")
    panel(c,*p2,"LATE ORDERS BY MONTH","Count of deliveries arriving after estimated date")
    line(c,[(r["month"],float(r["on_time_delivery_pct"])) for r in data],64,181,626,276,mn=75,mx=100)
    vbars(c,[(r["month"],int(r["late_deliveries"])) for r in data],756,181,646,276)
    summary(c,86,"March 2018: 1,328 late deliveries; 81.04% on time.",
            "Investigate operational events before assigning root causes.")
    c.showPage()

def draw_region(c):
    basic(c,"Where does delivery performance differ?","Customer destination differences: keep sample sizes visible when comparing service.",2)
    a=next(s for s in states if s["state"]=="SP")
    b=next(s for s in states if s["state"]=="RJ")
    cards(c,[("Eligible deliveries",f'{k["eligible_delivered_orders"]:,}',"All customer destination states"),
             ("Sao Paulo on time",f'{float(a["on_time_pct"]):.2f}%',f'{int(a["eligible_deliveries"]):,} eligible orders'),
             ("Rio de Janeiro on time",f'{float(b["on_time_pct"]):.2f}%',f'{int(b["eligible_deliveries"]):,} eligible orders'),
             ("Late deliveries",f'{k["late_deliveries"]:,}',"All destination states")])
    top=states[:10]
    panel(c,45,140,673,388,"ON-TIME RATE BY STATE","Ten largest destination cohorts")
    panel(c,738,140,693,388,"LATE ORDERS BY STATE","Absolute late-order count in same cohorts")
    hbars(c,[(r["state"],float(r["on_time_pct"])) for r in top],61,163,635,292,100,"rate")
    hbars(c,[(r["state"],int(r["late_deliveries"])) for r in top],754,163,649,292,2000,"count")
    summary(c,86,"SP 95.51% vs RJ 87.89% on time.",
            "Destination geography is not the seller origin or upstream supplier OTIF.")
    c.showPage()

def draw_reviews(c):
    basic(c,"How does delivery relate to customer reviews?","Observed review patterns by delivery timing; association is not causation.",3)
    on=reviews["on_time"]; late=reviews["late"]
    reviewed=int(on["reviewed_orders"])+int(late["reviewed_orders"])
    weighted=(float(on["avg_review_score"])*int(on["reviewed_orders"])+float(late["avg_review_score"])*int(late["reviewed_orders"]))/reviewed
    cards(c,[("Eligible reviewed orders",f'{reviewed:,}',"Valid delivery and review records"),
             ("Average review score",f'{weighted:.2f} / 5',"Weighted over reviewed orders"),
             ("On-time score",f'{float(on["avg_review_score"]):.2f} / 5',f'{int(on["reviewed_orders"]):,} reviewed orders'),
             ("Late score",f'{float(late["avg_review_score"]):.2f} / 5',f'{int(late["reviewed_orders"]):,} reviewed orders')])
    panel(c,45,140,673,388,"AVERAGE CUSTOMER REVIEW","Average score out of 5")
    panel(c,738,140,693,388,"SHARE OF LOW REVIEWS","Ratings of 1-2 out of 5")
    hbars(c,[("On time or early",float(on["avg_review_score"])),("Late",float(late["avg_review_score"]))],
          61,236,635,206,5,"score")
    hbars(c,[("On time or early",float(on["low_review_share_pct"])),("Late",float(late["low_review_share_pct"]))],
          754,236,649,206,100,"rate")
    summary(c,86,"On-time: 4.29 / 5    |    Late: 2.27 / 5.",
            "A correlation in historical reviews; not evidence of a causal effect.")
    c.showPage()

def draw_freight(c):
    basic(c,"Where is freight exposure concentrated?","Product item value and listed freight from the original Olist order items.",4)
    item=float(k["item_value_brl"]);freight=float(k["freight_value_brl"])
    cards(c,[("Listed item value",f"BRL {item/1e6:.2f}M","All source item lines"),
             ("Listed freight",f"BRL {freight/1e6:.2f}M","Customer-side freight values"),
             ("Freight / item value",f"{freight/item*100:.2f}%","Listed freight to merchandise"),
             ("Order-item lines",f'{k["source_rows"]["items"]:,}',"Original item records")])
    top=cats[:10]
    panel(c,45,140,673,388,"TOP 10 PRODUCT CATEGORIES","Listed merchandise value in BRL")
    panel(c,738,140,693,388,"FREIGHT RATIO FOR SAME CATEGORIES","Listed freight as a percentage of item value")
    hbars(c,[(r["category"],float(r["item_value_brl"])) for r in top],
          61,163,635,292,max(float(r["item_value_brl"]) for r in top),"money")
    hbars(c,[(r["category"],100*float(r["freight_brl"])/float(r["item_value_brl"])) for r in top],
          754,163,649,292,30,"rate")
    summary(c,86,"Overall listed freight / item value = 16.60%.",
            "Listed freight is not independently verified carrier cost or profit margin.")
    c.showPage()

def main():
    OUT.parent.mkdir(parents=True,exist_ok=True)
    c=canvas.Canvas(str(OUT),pagesize=(W,H),pageCompression=1)
    c.setTitle("Olist - Customer Fulfilment Intelligence (Power BI report PDF)")
    c.setAuthor("Independent Business Analysis portfolio | Olist public data")
    for f in (draw_delivery,draw_region,draw_reviews,draw_freight):f(c)
    c.save()
    print(f"Published {OUT} ({OUT.stat().st_size:,} bytes)")
if __name__=="__main__":main()
