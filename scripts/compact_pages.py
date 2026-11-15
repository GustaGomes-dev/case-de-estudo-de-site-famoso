import pathlib,gzip,re,hashlib,html,json
root=pathlib.Path(__file__).resolve().parents[1];dist=root/'dist';out=dist/'snapshots';out.mkdir(exist_ok=True)
# Keep the first page immediately renderable; store repeated deep-page markup once.
count=0
for p in dist.rglob('index.html'):
 if p==dist/'index.html':continue
 raw=p.read_bytes()
 if b'data-snapshot='in raw:continue
 name=hashlib.sha256(raw).hexdigest()[:24]+'.html.gz';target=out/name
 if not target.exists():target.write_bytes(gzip.compress(raw,compresslevel=9,mtime=0))
 title=re.search(rb'<title>(.*?)</title>',raw,re.S);title=title.group(1).decode()if title else'Gocase'
 p.write_text('<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="robots" content="noindex,nofollow"><title>'+title+'</title><style>body{margin:0;background:#fff;color:#777;font:14px Arial,sans-serif}.loading{padding:60px;text-align:center}</style></head><body data-snapshot="/snapshots/'+name+'"><div class="loading" role="status">Carregando Gocase…</div><script type="module" src="/loader.js"></script></body></html>')
 count+=1
print('Compacted pages:',count,'unique snapshots:',len(list(out.glob('*'))))
print('Expanded deployment bytes:',sum(p.stat().st_size for p in dist.rglob('*')if p.is_file()))
