const fs=require('fs'),vm=require('vm'),path=require('path');
const root=path.join(__dirname,'../reference');
for(const f of fs.readdirSync(root).filter(x=>x.endsWith('.html'))){
 const html=fs.readFileSync(path.join(root,f),'utf8');
 const code=html.match(/<script[^>]*>(window\.__NUXT__=.*?)<\/script>/s)?.[1];
 if(!code) continue;
 try {const ctx={window:{}};vm.runInNewContext(code,ctx,{timeout:3000});fs.writeFileSync(path.join(root,f+'.json'),JSON.stringify(ctx.window.__NUXT__,null,2));}catch(e){console.error(f,e.message);}
}
