import pathlib,re,json,html,urllib.request,urllib.parse,concurrent.futures,hashlib,mimetypes,time
root=pathlib.Path(__file__).resolve().parents[1];dist=root/'dist';out=dist/'assets/media';out.mkdir(parents=True,exist_ok=True)
urls=set()
for p in dist.rglob('*'):
 if not p.is_file() or p.suffix not in ['.html','.css']:continue
 text=p.read_text()
 for m in re.finditer(r'(?:src|srcset)="([^"]+)"|url\([\'"]?([^\)\'\"]+)',text):
  u=html.unescape(m.group(1)or m.group(2))
  if not u.startswith('data:') and not u.startswith('/assets') and ' 'not in u:
   urls.add(u if u.startswith('http') else 'https://www.gocase.com.br'+u)
# Capture all product card images, not every unrendered variant.
for p in json.loads((dist/'data/catalog.json').read_text()):
 if p.get('image'):urls.add(p['image'])
previous={}
try:previous=json.loads((dist/'data/assets.json').read_text())
except:pass
hosts={'cdn.gocase.com.br','cdn.sanity.io','i.ytimg.com','ik.imagekit.io','www.gocase.com.br'}
urls={u for u in urls if urllib.parse.urlparse(u).hostname in hosts}
def get(url):
 if url in previous and (dist/previous[url].lstrip('/')).is_file():return url,previous[url],None
 try:
  req=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'})
  with urllib.request.urlopen(req,timeout=25) as r:
   mime=r.headers.get_content_type();data=r.read()
  if not (mime.startswith('image/')or mime.startswith('font/')or any(x in mime for x in ['font','woff','octet-stream'])):return url,None,'unexpected type '+mime
  ext=mimetypes.guess_extension(mime)or pathlib.Path(urllib.parse.urlparse(url).path).suffix or '.bin'
  if ext in ['.jpe','.jpeg']:ext='.jpg'
  name=hashlib.sha1(url.encode()).hexdigest()[:24]+ext
  (out/name).write_bytes(data);return url,'/assets/media/'+name,None
 except Exception as e:return url,None,str(e)
errors=[];mapping=previous.copy();print('Media to capture',len(urls),flush=True)
with concurrent.futures.ThreadPoolExecutor(max_workers=12)as ex:
 for n,(u,local,error)in enumerate(ex.map(get,sorted(urls))):
  if local:
   mapping[u]=local
   if u.startswith('https://www.gocase.com.br/'):mapping[u.removeprefix('https://www.gocase.com.br')]=local
  else:errors.append({'url':u,'error':error})
  if n%200==0:print('Media',n,'/',len(urls),flush=True)
(dist/'data/assets.json').write_text(json.dumps(mapping,ensure_ascii=False,separators=(',',':')))
(root/'reference/media-errors.json').write_text(json.dumps(errors,indent=2));print('Saved',len(mapping),'mappings; failed',len(errors),flush=True)
def subattr(m):
 u=html.unescape(m.group(2));return m.group(1)+html.escape(mapping.get(u,u),quote=True)+m.group(3)
def subcss(m):
 u=html.unescape(m.group(2));return m.group(1)+mapping.get(u,u)+m.group(3)
for p in dist.rglob('*'):
 if not p.is_file() or p.suffix not in ['.html','.css']:continue
 text=p.read_text();text=re.sub(r'((?:src|srcset|href)=")([^"]+)(")',subattr,text)
 text=re.sub(r'(url\([\'"]?)([^\)\'\"]+)([\'"]?\))',subcss,text)
 p.write_text(text)
print('HTML and CSS media references localized',flush=True)
