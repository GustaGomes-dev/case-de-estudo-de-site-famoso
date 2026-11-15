import json,re,pathlib,html
from html.parser import HTMLParser
root=pathlib.Path(__file__).resolve().parents[1];ref=root/'reference';dist=root/'dist'
def decode(v):
 if isinstance(v,dict):return {k:decode(x)for k,x in v.items()}
 if isinstance(v,list)and len(v)==2 and isinstance(v[0],int):
  if v[0]==1:return [decode(x)for x in v[1]]
  return decode(v[1])
 return v
class Islands(HTMLParser):
 def __init__(self):super().__init__();self.buy=None
 def handle_starttag(self,t,a):
  d=dict(a)
  if t=='astro-island'and'BuyBox'in d.get('component-url',''):self.buy=decode(json.loads(d['props']))
updated=[]
for pg in json.loads((ref/'pages.json').read_text()):
 if not pg.get('path','').endswith('/p'):continue
 raw=(ref/pg['file']).read_text()
 if 'astro-island'not in raw:continue
 parser=Islands();parser.feed(raw);b=parser.buy
 if not b:continue
 slug=b['slug'];f=dist/'data/products'/f'{slug}.json';p=json.loads(f.read_text());p['astro']=True;p['captured_detail']=True
 p['devices']=[{'id':b['deviceId'],'name':b['deviceCode'],'code':b['deviceCode']}];p['default_case_device_id']=b['selectedCaseDeviceId']
 p['case_types']=[{'id':c['id'],'name':c['name'],'code':c['code'],'case_image':c['swatch'],'devices':[{'device_id':b['deviceId'],'case_device_id':c['caseDeviceId'],'cost_price':0,'in_stock':c['inStock']}]}for c in b['colors']]
 p['color_options']=[{'case_type_id':c['id'],'case_device_id':c['caseDeviceId'],'device_code':b['deviceCode'],'price':c['price'],'old_price':c['oldPrice'],'image':p['image'].replace(re.search(r'/govinci/[^/]+/([^/]+)/mockup',p['image']).group(1),c['code']+'-'+b['deviceCode'])}for c in b['colors']]
 selected=next(c for c in b['colors']if c['caseDeviceId']==b['selectedCaseDeviceId']);p['price']=selected['price'];p['old_price']=selected['oldPrice'];f.write_text(json.dumps(p,ensure_ascii=False,separators=(',',':')));updated.append(p)
catalog=json.loads((dist/'data/catalog.json').read_text())
for p in updated:
 for c in catalog:
  if c['slug']==p['slug']:
   c.update(price=p['price'],old_price=p['old_price'],captured_detail=True)
(dist/'data/catalog.json').write_text(json.dumps(catalog,ensure_ascii=False,separators=(',',':')))
for name in ['coverage.json','dist/data/coverage.json']:
 f=root/name;c=json.loads(f.read_text());c['productDetails']=sum(p.get('captured_detail',False)for p in catalog);c['localMediaFiles']=len(list((dist/'assets/media').glob('*')));f.write_text(json.dumps(c,ensure_ascii=False,indent=2))
print('Repaired Astro product data:',len(updated))
