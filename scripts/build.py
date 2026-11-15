import pathlib,re,json,hashlib,html,urllib.parse
R=pathlib.Path(__file__).resolve().parents[1];ref=R/'reference';dist=R/'dist'
(dist/'assets/css').mkdir(parents=True,exist_ok=True);(dist/'data/products').mkdir(parents=True,exist_ok=True)
pages=json.loads((ref/'pages.json').read_text());products={};groups={};docs={};pdp=set()
def walk(v,route):
 if isinstance(v,list):
  for x in v:walk(x,route)
 elif isinstance(v,dict):
  if v.get('slug') and v.get('name') and (v.get('image') or v.get('images')) and ('price'in v or 'price_with_cost'in v):
   slug=v['slug'];old=products.get(slug,{})
   if 'price'in v:
    old.update({k:v[k] for k in ['id','sku','slug','name','price','old_price','image','in_stock','color_options','reviews','product_type_code'] if k in v});groups.setdefault(route,[]).append(slug)
   else:
    old.update({k:v[k] for k in ['id','sku','slug','name','description','images','case_types','devices','customizations','default_case_device_id','category','in_stock','product_type_code','default_customization_params'] if k in v})
    old['price']=v['price_with_cost'];old['old_price']=v.get('old_price_with_cost');old.setdefault('image',v['images'][0]['url'] if v['images'] else '')
   products[slug]=old;return
  for k,x in v.items():
   if k not in ['config','homeContent']:walk(x,route)
for pg in pages:
 if 'file' not in pg:continue
 try:st=json.loads((ref/(pg['file']+'.json')).read_text())
 except:continue
 walk(st.get('data'),pg['path']);walk(st.get('fetch'),pg['path']);walk(st.get('state',{}).get('product',{}).get('product'),pg['path'])
 if pg['path'].endswith('/p'):pdp.add(pg['path'].split('/')[1])
# Preserve every captured route and the final path of public redirects.
known={}
for pg in [{'path':'/','file':'home.html','url':'https://www.gocase.com.br/'}]+pages:
 if 'file' not in pg or 'goconnect' in pg.get('url',''):continue
 raw=(ref/pg['file']).read_text();path=pg['path'].rstrip('/') or '/'
 if '<html' not in raw:continue
 docs[path]=raw
 known[path]=path
 final=urllib.parse.urlparse(pg.get('url','')).path.rstrip('/') or '/'
 if final!=path and final not in docs:docs[final]=raw;known[final]=final
 for route in [path,final]:
  if path in groups:groups[route]=list(dict.fromkeys(groups[path]))
assets=set()
def clean(raw):
 raw=re.sub(r'<script\b[^>]*>.*?</script\s*>','',raw,flags=re.S|re.I)
 raw=re.sub(r'<link\b[^>]*(?:rel="(?:preconnect|dns-prefetch|canonical|alternate)"|as="script")[^>]*>','',raw,flags=re.I)
 raw=re.sub(r'\son\w+="[^"]*"','',raw,flags=re.I)
 raw=re.sub(r'(href=")https://www\.gocase\.com\.br(?=/)',r'\1',raw)
 def css(m):
  text=m.group(1);h=hashlib.sha1(text.encode()).hexdigest()[:14];(dist/'assets/css'/f'{h}.css').write_text(text)
  return f'<link rel="stylesheet" href="/assets/css/{h}.css">'
 raw=re.sub(r'<style[^>]*>(.*?)</style>',css,raw,flags=re.S)
 raw=raw.replace('</head>','<meta name="robots" content="noindex,nofollow"><link rel="stylesheet" href="/replica.css"></head>')
 raw=raw.replace('</body>','<a class="r-study" href="/sobre-a-copia" title="Cobertura e limites desta cópia">Cópia de estudo · ambiente de demonstração</a><div id="r-toast" role="status" aria-live="polite"></div><script type="module" src="/app.js"></script></body>')
 return raw
for path,raw in docs.items():
 text=clean(raw);out=dist/path.lstrip('/')/'index.html';out.parent.mkdir(parents=True,exist_ok=True);out.write_text(text)
# Shared shell: replacing the balanced pages div preserves the exact original header/footer.
def replace_pages(text,content):
 start=text.find('<div class="pages">');pos=start;depth=0
 for m in re.finditer(r'</?div\b[^>]*>',text[start:]):
  tag=m.group();depth+=(-1 if tag.startswith('</') else 1)
  if depth==0:return text[:start]+'<div class="pages"><main id="r-main">'+content+'</main></div>'+text[start+m.end():]
 raise ValueError('pages container not found')
shell=replace_pages(clean(docs['/']),'<div class="r-loading">Carregando…</div>')
for path in ['search','cart','checkout','wishlist','account','central-de-ajuda','sobre-a-copia']:
 out=dist/path/'index.html';out.parent.mkdir(parents=True,exist_ok=True);out.write_text(shell)
# Missing deep links get a local catalog, preserving a navigable review environment.
links=set()
for raw in docs.values():
 for link in re.findall(r'href="([^"]+)"',raw):
  link=html.unescape(link);u=urllib.parse.urlparse(link)
  if (not u.netloc or u.netloc=='www.gocase.com.br') and u.path.startswith('/') and not re.search(r'\.(svg|png|jpe?g|pdf|webp|css|m?js|woff2?|ttf|ico|json|map|gif)$',u.path):links.add(u.path.rstrip('/') or '/')
for path in links:
 if '..' in path:continue
 out=dist/path.lstrip('/')/'index.html'
 if not out.exists():out.parent.mkdir(parents=True,exist_ok=True);out.write_text(shell)
# Only publish public product fields, never the original runtime configuration.
catalog=[]
for slug,p in products.items():
 p['price']=float(p.get('price') or 0);p['old_price']=float(p.get('old_price') or p['price']);p['captured_detail']=slug in pdp
 p['groups']=[k for k,v in groups.items() if slug in v]
 (dist/'data/products'/f'{slug}.json').write_text(json.dumps(p,ensure_ascii=False,separators=(',',':')))
 catalog.append({k:p[k] for k in ['id','slug','name','price','old_price','image','in_stock','reviews','category','groups','product_type_code','captured_detail'] if k in p})
 out=dist/slug/'p/index.html'
 if not out.exists():out.parent.mkdir(parents=True,exist_ok=True);out.write_text(shell)
(dist/'data/catalog.json').write_text(json.dumps(catalog,ensure_ascii=False,separators=(',',':')))
(dist/'data/groups.json').write_text(json.dumps(groups,ensure_ascii=False,separators=(',',':')))
(dist/'data/routes.json').write_text(json.dumps(sorted(docs),ensure_ascii=False))
report={'capturedAt':'2026-11-14','source':'https://www.gocase.com.br/','capturedPages':len(pages)+1,'capturedRoutes':len(docs),'products':len(catalog),'productDetails':len(pdp),'generatedFallbackRoutes':len(links-set(docs)),'browserQA':False}
(dist/'data/coverage.json').write_text(json.dumps(report,ensure_ascii=False,indent=2));(R/'coverage.json').write_text(json.dumps(report,indent=2))
print(json.dumps(report,indent=2))
