#!/usr/bin/env python3
"""Build Olist Excel dashboard from verified reference CSVs and optional processed Olist data.

Requires artifact_tool. Without transaction CSVs, order-level KPI cells say Not loaded.
"""
from __future__ import annotations
import csv,json,argparse
from pathlib import Path
from artifact_tool import Workbook, SpreadsheetFile

ROOT=Path(__file__).resolve().parents[1]
NAVY='#152B42';TEAL='#087D75';LIGHT='#E9F4F3';WHITE='#FFFFFF';GREY='#63768A';PALE='#F1F4F8';INK='#223448'

def read_csv(path):
    if not path.exists(): return []
    with path.open(newline='',encoding='utf-8-sig') as h:return list(csv.DictReader(h))

def excelcol(n):
    s=''
    while n:n,r=divmod(n-1,26);s=chr(65+r)+s
    return s

def table(wb,name,headers,rows,limit=300):
    s=wb.worksheets.add(name)
    ints={'orders','delivered','on_time_eligible','on_time_deliveries','late_deliveries','item_lines','order_count_attributed','seller_count','sellers','on_time_flag','review_count'}
    numeric=ints|{'on_time_delivery_pct','avg_late_days','item_value_brl','freight_value_brl','freight_brl','payment_value_brl','delivery_days_from_estimate','review_score_avg'}
    def convert(k,v):
        if k not in numeric or v is None or v=='':return v if v is not None else ''
        try:return int(v) if k in ints else float(v)
        except (ValueError,TypeError):return v
    rows=[[convert(h,r.get(h,'')) for h in headers] for r in rows[:limit]]
    end=excelcol(len(headers))
    s.get_range(f'A1:{end}{1+len(rows)}').values=[headers]+rows
    s.get_range(f'A1:{end}1').format={'fill':NAVY,'font':{'name':'Arial','size':11,'bold':True,'color':WHITE},'row_height':28}
    for i,h in enumerate(headers):
        s.get_range(f'{excelcol(i+1)}:{excelcol(i+1)}').format.column_width=28 if len(h)>15 else 19
    s.freeze_panes.freeze_rows(1)
    return s

def build(processed,output):
    state=read_csv(ROOT/'data/reference/olist_seller_state_profile.csv')
    city=read_csv(ROOT/'data/reference/olist_seller_city_top20.csv')
    assert len(state)==23 and sum(int(x['seller_count']) for x in state)==3095
    kpi_path=processed/'kpi_summary.json'
    full=kpi_path.is_file()
    k=json.loads(kpi_path.read_text(encoding='utf-8')) if full else {}
    if full and k.get('data_status')!='FULL_OLIST_DATA_LOADED':raise ValueError('Unverified Olist summary')
    wb=Workbook.create()
    d=wb.worksheets.add('DASHBOARD')
    d.merge_cells('A1:J2')
    d.get_range('A1').values=[['ORDER FULFILMENT & DELIVERY INTELLIGENCE']]
    d.get_range('A1:J2').format={'fill':NAVY,'font':{'name':'Arial','size':18,'color':WHITE,'bold':True},'row_height':25}
    d.merge_cells('A3:J3')
    d.get_range('A3').values=[['Olist Brazil 2016-2018 | Historical public data | BRL | Portfolio case study']]
    d.get_range('A3:J3').format={'fill':LIGHT,'font':{'name':'Arial','size':10,'color':INK},'row_height':25}
    d.get_range('A:J').format.column_width=15
    d.merge_cells('A5:J5')
    d.get_range('A5').values=[['STATUS: Full Olist transaction data loaded' if full else 'STATUS: Seller footprint only - order records not loaded']]
    d.get_range('A5:J5').format={'fill':TEAL,'font':{'name':'Arial','size':11,'color':WHITE,'bold':True},'row_height':27}
    metrics=[
        ['Orders',k.get('orders','Not loaded')],
        ['Delivered orders',k.get('delivered_orders','Not loaded')],
        ['Eligible delivered orders',k.get('eligible_delivered_orders','Not loaded')],
        ['On-time customer delivery',str(k.get('on_time_delivery_rate_pct'))+'%' if full and k.get('on_time_delivery_rate_pct') is not None else 'Not loaded'],
        ['Average delivery lead',str(k.get('avg_delivery_lead_days'))+' days' if full and k.get('avg_delivery_lead_days') is not None else 'Not loaded'],
        ['Late deliveries',k.get('late_deliveries','Not loaded')],
        ['Cancelled orders',k.get('cancelled_orders','Not loaded')],
        ['Distinct seller IDs',k.get('seller_count',3095)],
    ]
    d.get_range('A8:C15').values=[[name,'',val] for name,val in metrics]
    d.get_range('A8:B15').format={'fill':PALE,'font':{'name':'Arial','size':11,'color':INK},'row_height':26}
    d.get_range('C8:C15').format={'fill':LIGHT,'font':{'name':'Arial','size':12,'color':TEAL,'bold':True},'row_height':26}
    d.merge_cells('A17:J17')
    d.get_range('A17').values=[['VERIFIED SELLER GEOGRAPHY']]
    d.get_range('A17:J17').format={'fill':TEAL,'font':{'name':'Arial','size':11,'color':WHITE,'bold':True},'row_height':26}
    d.get_range('A18:C18').values=[['State','Seller IDs','Share']]
    d.get_range('A18:C18').format={'fill':NAVY,'font':{'name':'Arial','size':10,'color':WHITE,'bold':True}}
    for i,r in enumerate(state[:10],start=19):
        d.get_range(f'A{i}:B{i}').values=[[r['state'],int(r['seller_count'])]]
    d.get_range('C19').formulas=[['=IFERROR(B19/$C$15,0)']]
    d.get_range('C19:C28').fill_down()
    d.get_range('C19:C28').set_number_format('0.0%')
    chart=d.charts.add('bar',{'title':'Olist seller IDs by state','has_legend':False})
    chart.bar_options.direction='column'
    series=chart.series.add('Seller IDs')
    series.category_formula="'DASHBOARD'!$A$19:$A$28"
    series.formula="'DASHBOARD'!$B$19:$B$28"
    chart.set_position('E18','K32')
    d.merge_cells('A32:J32')
    d.get_range('A32').values=[['Interpretation: state counts are not evidence of seller on-time delivery.']]
    d.get_range('A32:J32').format={'font':{'name':'Arial','size':10,'color':INK},'row_height':24}
    d.merge_cells('A33:J33')
    d.get_range('A33').values=[['No upstream supplier POs, inventory or warehouse receipts: supplier OTIF is not measured.']]
    d.get_range('A33:J33').format={'font':{'name':'Arial','size':10,'color':INK},'row_height':24}
    d.freeze_panes.freeze_rows(3)

    ss=table(wb,'SELLER_STATES',['state','seller_count','share'],[{'state':r['state'],'seller_count':r['seller_count'],'share':''} for r in state],50)
    ss.get_range('C2').formulas=[['=IFERROR(B2/SUM($B$2:$B$24),0)']]
    ss.get_range('C2:C24').fill_down()
    ss.get_range('C2:C24').set_number_format('0.0%')
    table(wb,'SELLER_CITIES',['seller_city','seller_state','seller_count'],city)
    tables=[
        ('MONTHLY_DELIVERY',['month','orders','delivered','on_time_eligible','on_time_deliveries','late_deliveries','on_time_delivery_pct','avg_late_days','item_value_brl','freight_value_brl'],'monthly_metrics.csv',60),
        ('CATEGORY_ANALYSIS',['category','order_count_attributed','item_lines','item_value_brl','freight_brl'],'category_summary.csv',150),
        ('SELLER_SALES',['seller_id','seller_state','seller_city','order_count_attributed','item_lines','item_value_brl','freight_brl'],'seller_summary.csv',150),
        ('ORDER_SAMPLE',['order_id','purchase_month','order_status','customer_state','purchase_date','actual_delivery_date','estimated_delivery_date','delivery_days_from_estimate','on_time_eligible','on_time_flag','item_lines','item_value_brl','freight_value_brl','payment_value_brl','review_score_avg','review_count'],'orders_enriched.csv',300),
    ]
    for name,headers,filename,n in tables:
        table(wb,name,headers,read_csv(processed/filename) if full else [],n)
    defs=[
        ('Customer on-time delivery','Actual customer delivery date <= estimate date among eligible delivered orders','Not supplier OTIF'),
        ('Average delivery lead time','Mean elapsed days from customer purchase to delivery','Eligible delivered only'),
        ('Item value (BRL)','Sum of order_items.price','Not supplier purchasing cost'),
        ('Freight value (BRL)','Sum of order_items.freight_value','Not verified carrier cost invoice'),
        ('Customer payments','Sum payments at order grain, before joins','Not supplier AP spend'),
        ('Seller footprint','Distinct seller IDs grouped by state','Not sales volume nor performance'),
        ('Inbound supplier OTIF','Not available','No PO/warehouse accepted quantities'),
    ]
    table(wb,'KPI_DICTIONARY',['metric','definition','limitation'],[dict(zip(['metric','definition','limitation'],r)) for r in defs])
    reqs=[
        ('BR-01','Customer delivery reliability','On-time among delivered orders with both dates','MONTHLY_DELIVERY'),
        ('BR-02','Financial item and freight analysis','No many-to-many duplicate order values','SELLER_SALES / CATEGORY_ANALYSIS'),
        ('BR-03','Verify seller footprint','State counts sum 3095','SELLER_STATES'),
        ('BR-04','Transparent source limitations','No unsupported supplier OTIF','KPI_DICTIONARY'),
    ]
    table(wb,'BA_REQUIREMENTS',['id','business_need','acceptance','evidence'],[dict(zip(['id','business_need','acceptance','evidence'],r)) for r in reqs])
    qa=[{'control':'Seller source population','value':3095,'status':'PASS','note':'23 Brazilian states'}]
    if full:
        for key,value in k['qa'].items():
            qa.append({'control':key,'value':str(value),'status':'PASS' if (value if isinstance(value,bool) else value==0) else 'REVIEW','note':'Inspect nonzero linkage exceptions'})
    else:
        qa += [{'control':'Raw order data','value':'Not loaded','status':'PENDING','note':'Download full Olist CSVs from Kaggle'},
               {'control':'On-time customer delivery','value':'Not loaded','status':'PENDING','note':'No source transaction data has been loaded'}]
    table(wb,'DATA_QA',['control','value','status','note'],qa)
    src=[
        ('Olist source','Kaggle Olist','https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce','Original full CSVs not bundled'),
        ('Sellers source','Public GitHub mirror','https://raw.githubusercontent.com/spdrio/Brazilian-E-Commerce-Public-Dataset-by-Olist/master/files/olist_sellers_dataset.csv','Real 3,095-seller reference'),
        ('SCM overview','User-supplied template','Prior independent SCM workbook','Functional layout reference, not copied transactions'),
    ]
    table(wb,'SOURCE_LOG',['source','publisher','source_url','scope'],[dict(zip(['source','publisher','source_url','scope'],r)) for r in src])
    steps=[
        ('1','Download','Get original eight Olist source CSVs from Kaggle into data/raw'),
        ('2','Process','Run python scripts/process_olist.py --raw data/raw --output data/processed'),
        ('3','Rebuild','Run python scripts/build_workbook.py --processed data/processed'),
        ('4','Check','Run Python unit tests and inspect data/processed/kpi_summary.json'),
        ('5','Review','Dashboard, monthly delivery, category, seller, DATA_QA'),
    ]
    table(wb,'HOW_TO_USE',['step','topic','instruction'],[dict(zip(['step','topic','instruction'],r)) for r in steps])
    output.parent.mkdir(parents=True,exist_ok=True)
    SpreadsheetFile.export_xlsx(wb).save(str(output))
    print('Workbook written:',output,'mode:','full' if full else 'seller preview')
    return wb

if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--processed',type=Path,default=Path('data/processed'))
    p.add_argument('--output',type=Path,default=Path('workbook/Olist_Order_Fulfilment_Intelligence.xlsx'))
    args=p.parse_args()
    build(args.processed,args.output)
