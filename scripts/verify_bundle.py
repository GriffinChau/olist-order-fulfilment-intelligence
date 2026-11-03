"""Verify source seller counts and published 16-sheet real-data Excel workbook."""
import csv, json
from pathlib import Path
from zipfile import ZipFile
root=Path(__file__).resolve().parents[1]
with (root/'data/reference/olist_seller_state_profile.csv').open(newline='') as f:
    states=list(csv.DictReader(f))
count=sum(int(x['seller_count']) for x in states)
assert count==3095,(count,'seller count changed')
assert len(states)==23,'Unexpected distinct seller states'
assert next(int(x['seller_count']) for x in states if x['state']=='SP')==1849
path=root/'workbook/Olist_Order_Fulfilment_Intelligence_Real_Data.xlsx'
if path.is_file():
    with ZipFile(path) as z:
        assert z.testzip() is None
        assert 'xl/workbook.xml' in z.namelist()
        assert len([p for p in z.namelist() if p.startswith('xl/worksheets/sheet') and p.endswith('.xml')])>=16
    workbook_status='VALID'
else:
    workbook_status='NOT_PUBLISHED'
print(json.dumps({'reference_seller_ids':count,'state_codes':len(states),'workbook_status':workbook_status},indent=2))
