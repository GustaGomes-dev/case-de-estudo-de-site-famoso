import urllib.request,concurrent.futures,json,pathlib,hashlib,time
root=pathlib.Path(__file__).resolve().parents[1] / 'reference'
root.mkdir(parents=True, exist_ok=True)
paths=['/lp/totes/daily','/lp/totes','/lp/garrafa-termica/fresh','/lp/garrafa-termica','/lp/bolsas','/lp/malas','/lp/copos','/lp/lancheiras','/lp/mochilas','/capinha-para-celular/','/vitrine','/totebag-daily-clear/p','/garrafa-termica-fresh-ebook-clear/p','/copo-termico-ebook-lemon-fruit/p','/mala-de-bordo-trip-clear/p','/capinha-para-celular-run-club/p','/bolsa-termica-fruit-pro-clear/p','/login','/signup','/find-order','/quem-somos','/termos-de-uso','/central-de-ajuda']
def get(p):
 try:
  req=urllib.request.Request('https://www.gocase.com.br'+p,headers={'User-Agent':'Mozilla/5.0'})
  with urllib.request.urlopen(req,timeout=50) as r: data=r.read();final=r.url
  name=hashlib.sha1(p.encode()).hexdigest()+'.html';(root/name).write_bytes(data)
  return {'path':p,'file':name,'url':final,'size':len(data)}
 except Exception as e:return {'path':p,'error':str(e)}
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as ex:
 res=list(ex.map(get,paths))
(root/'pages.json').write_text(json.dumps(res,ensure_ascii=False,indent=2))
print(json.dumps(res,ensure_ascii=False,indent=2))
