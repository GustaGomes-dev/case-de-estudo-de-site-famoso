exec(open(__import__('pathlib').Path(__file__).resolve().with_name('capture.py')).read().split('paths=')[0])
import re,html
existing=json.loads((root/'pages.json').read_text());seen={p['path'] for p in existing}
s=(root/'home.html').read_text()
paths={html.unescape(x).split('?')[0].rstrip('/') for x in re.findall(r'href="(/lp/[^"#]+)',s)}
paths.update(['/lp/termicos','/lp/pets','/lp/futebol','/lp/floral','/lp/disney','/lp/marvel','/lp/religiao','/lp/minimalista','/lp/para-eles','/lp/borboletas','/lp/glow','/lp/sua-foto','/top-produtos-50','/acessorios-hit','/goestojos','/necessaires','/coleiras-pet','/guias-pet','/peitorais-pet'])
paths=sorted(paths-seen)
# Bounded parallel read-only capture of linked public pages.
ns={};exec(open(__import__('pathlib').Path(__file__).resolve().with_name('capture.py')).read().split('def get(p):')[1].split('with concurrent.futures')[0].join(['def get(p):','']),globals())
with concurrent.futures.ThreadPoolExecutor(max_workers=6) as ex:
 for p in ex.map(get,paths):
  existing.append(p)
(root/'pages.json').write_text(json.dumps(existing,ensure_ascii=False,indent=2))
print('Captured',len(paths),'additional pages; failures:',[p for p in existing if 'error'in p])
