#!/usr/bin/env python3
"""Download Olist public Kaggle ZIP into data/raw if publisher permits it.
Use the manual Kaggle website if the automated anonymous download is blocked.
"""
import io,sys,urllib.request,zipfile
from pathlib import Path
url='https://www.kaggle.com/api/v1/datasets/download/olistbr/brazilian-ecommerce'
target=Path(sys.argv[1]) if len(sys.argv)>1 else Path('data/raw')
target.mkdir(parents=True,exist_ok=True)
print('Downloading from:',url)
try:
    req=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0 SCM-portfolio-data-fetch/1.0'})
    with urllib.request.urlopen(req,timeout=180) as r: archive=r.read()
    with zipfile.ZipFile(io.BytesIO(archive)) as z:
        for member in z.infolist():
            if not member.filename.endswith('.csv'):continue
            name=Path(member.filename).name
            if name: (target/name).write_bytes(z.read(member))
    print('Downloaded source CSV files:',*[p.name for p in sorted(target.glob('*.csv'))],sep='\n - ')
except Exception as exc:
    print('Automatic download failed:',exc)
    print('Manual alternative: https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce')
    print('Unzip all 8 required CSV files + translation file into',target)
    sys.exit(1)
