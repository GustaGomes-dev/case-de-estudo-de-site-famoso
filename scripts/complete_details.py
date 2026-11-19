exec(open(__import__('pathlib').Path(__file__).resolve().with_name('capture.py')).read().split('paths=')[0])
existing=json.loads((root/'pages.json').read_text());seen={p['path'].rstrip('/') for p in existing}
products=json.loads((root.parent/'dist/data/catalog.json').read_text());paths=['/'+p['slug']+'/p' for p in products if '/'+p['slug']+'/p'not in seen]
exec('def get(p):'+open(__import__('pathlib').Path(__file__).resolve().with_name('capture.py')).read().split('def get(p):')[1].split('with concurrent.futures')[0],globals())
with concurrent.futures.ThreadPoolExecutor(max_workers=8) as ex:
 for idx,p in enumerate(ex.map(get,paths)):
  existing.append(p)
  if idx%100==0:print('Detalhes',idx,'/',len(paths),flush=True)
(root/'pages.json').write_text(json.dumps(existing,ensure_ascii=False,indent=2));print('Páginas capturadas',len(existing))
