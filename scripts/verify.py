from pathlib import Path
from html.parser import HTMLParser
import json,re,urllib.parse,gzip
root=Path(__file__).resolve().parents[1];dist=root/'dist';missing=set();external_scripts=[];files=0
class P(HTMLParser):
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if tag=='script'and a.get('src','').startswith('http'):external_scripts.append(a['src'])
  keys=['src']if tag in ['script','img']else['href']if tag=='link'and a.get('rel')=='stylesheet'else[]
  for key in keys:
   u=urllib.parse.urlparse(a.get(key,''))
   if not u.netloc and u.path.startswith('/')and not(dist/urllib.parse.unquote(u.path).lstrip('/')).is_file():missing.add(u.path)
for p in dist.rglob('*.html'):
 if not p.is_file():continue
 files+=1;P().feed(p.read_text())
assert not missing, sorted(missing)
assert not external_scripts,external_scripts
catalog=json.loads((dist/'data/catalog.json').read_text());assert len(catalog)==713
for p in catalog:
 detail=dist/'data/products'/(p['slug']+'.json');assert detail.is_file();assert(dist/p['slug']/'p/index.html').is_file()
for p in (dist/'snapshots').glob('*.gz'):
 P().feed(gzip.decompress(p.read_bytes()).decode())
assert not missing,sorted(missing)
assert not external_scripts,external_scripts
assert sum(p.stat().st_size for p in dist.rglob('*') if p.is_file()) < 256*1024*1024
if (root/'.openai/hosting.json').is_file():
 json.loads((root/'.openai/hosting.json').read_text())
print(f'PASS: {files} documentos HTML; imagens/scripts/CSS locais presentes; 713 produtos com dados e rota; scripts de origem removidos')
