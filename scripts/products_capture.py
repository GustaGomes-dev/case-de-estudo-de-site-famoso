exec(open(__import__('pathlib').Path(__file__).resolve().with_name('capture.py')).read().split('paths=')[0])
existing=json.loads((root/'pages.json').read_text());seen={p['path'].rstrip('/') for p in existing}
products=json.loads((root/'products.json').read_text())
paths={('/'+k+'/p') for k in products}
for p in existing:
 try:
  data=json.loads((root/(p['file']+'.json')).read_text())['data'][0];cfg=data.get('config',{})
  base=cfg.get('basePath')
  if base:
   for sub in cfg.get('subcategories',[]): paths.add(base+'/'+sub['key'])
 except:pass
paths=sorted(paths-seen)
exec('def get(p):'+open(__import__('pathlib').Path(__file__).resolve().with_name('capture.py')).read().split('def get(p):')[1].split('with concurrent.futures')[0],globals())
with concurrent.futures.ThreadPoolExecutor(max_workers=8) as ex:
 for idx,p in enumerate(ex.map(get,paths)):
  existing.append(p)
  if idx%50==0:print('Captured',idx,'/',len(paths),flush=True)
(root/'pages.json').write_text(json.dumps(existing,ensure_ascii=False,indent=2))
print('Total pages',len(existing),'failures',sum('error'in p for p in existing))
