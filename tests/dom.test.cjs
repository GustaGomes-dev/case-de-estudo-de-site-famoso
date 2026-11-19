const {parseHTML}=require('linkedom');
const fs=require('fs'),path=require('path'),vm=require('vm'),assert=require('node:assert/strict');
const root=path.resolve(__dirname,'../dist');
const store=new Map();const localStorage={getItem:k=>store.get(k)??null,setItem:(k,v)=>store.set(k,v),removeItem:k=>store.delete(k)};
async function boot(route){
 const file=path.join(root,route,'index.html');let html=fs.readFileSync(file,'utf8');const snapshot=html.match(/data-snapshot="([^"]+)"/);if(snapshot)html=require('zlib').gunzipSync(fs.readFileSync(path.join(root,snapshot[1]))).toString();const {window}=parseHTML(html);const document=window.document;
 Object.defineProperty(window.HTMLSelectElement.prototype,'value',{get(){return [...this.options].find(x=>x.hasAttribute('selected'))?.getAttribute('value')||this.options[0]?.getAttribute('value')||''},set(v){[...this.options].forEach(x=>{if(x.getAttribute('value')==v)x.setAttribute('selected','');else x.removeAttribute('selected')})},configurable:true});
 window.HTMLElement.prototype.showModal=function(){this.open=true};window.HTMLElement.prototype.close=function(){this.open=false;this.dispatchEvent(new window.Event('close'))};window.HTMLElement.prototype.reportValidity=()=>true;
 const errors=[];const core=await import(path.join(root,'core.mjs'));const location=new URL('http://localhost'+route);
 const context={...core,esc:core.escapeHTML,document,window,localStorage,location,URLSearchParams,fetch:async u=>{const p=path.join(root,u.split('?')[0]);const exists=fs.existsSync(p)&&fs.statSync(p).isFile();return {ok:exists,json:async()=>exists?JSON.parse(fs.readFileSync(p)):null}},console:{log:()=>{},error:(...x)=>errors.push(x)},setInterval:()=>0,clearInterval:()=>{},setTimeout:()=>0,clearTimeout:()=>{}};
 vm.runInNewContext(fs.readFileSync(path.join(root,'app.js'),'utf8').replace(/^import .*?;\n/,''),context);
 for(let i=0;i<20;i++)await new Promise(setImmediate);
 assert.deepEqual(errors,[],`${route} init errors`);return {document,window};
}
(async()=>{
 let {document,window}=await boot('/');assert.equal(document.querySelectorAll('.new-home-offers__grid .r-card').length,20);assert.equal(document.querySelectorAll('.new-home-offers__skeleton').length,0);
 const input=document.querySelector('input[type=search]');input.value='tote';input.dispatchEvent(new window.Event('input'));assert.ok(document.querySelectorAll('.r-search-results a').length>0);
 const next=document.querySelector('.new-home-hero__arrow--next');next.click();assert.match(document.querySelector('.new-home-hero__slide').style.transform,/-1/);
 console.log('PASS: inicial, vitrines, busca e carrossel');
 ({document,window}=await boot('/totebag-daily-clear/p'));assert.ok(document.querySelector('#r-option'));assert.equal(document.querySelector('.product-form__skeleton'),null);assert.match(document.querySelector('.product-price__current').textContent,/159,90/);
 document.querySelector('.product-form').dispatchEvent(new window.Event('submit',{cancelable:true}));assert.equal(JSON.parse(store.get('gocase-study:cart')).length,1);assert.ok(document.querySelector('dialog.r-drawer'));document.querySelector('[data-qty="1"]').click();assert.equal(JSON.parse(store.get('gocase-study:cart'))[0].qty,2);
 console.log('PASS: produto, opções, preço, adicionar e alterar quantidade');
 ({document,window}=await boot('/cart'));assert.equal(document.querySelectorAll('.r-cart-item').length,1);assert.match(document.querySelector('#r-cart-content').textContent,/319,80/);
 ({document,window}=await boot('/checkout'));document.querySelector('#r-cep').value='01310-100';document.querySelector('#r-calculate').click();assert.match(document.querySelector('#r-delivery').textContent,/simulada/);document.querySelector('#r-checkout-form').dispatchEvent(new window.Event('submit',{cancelable:true}));assert.match(document.querySelector('#r-main').textContent,/demonstração concluído/);assert.equal(JSON.parse(store.get('gocase-study:cart')).length,0);assert.match(JSON.parse(store.get('gocase-study:order')).id,/^DEMO-/);
 console.log('PASS: persistência do carrinho e checkout de demonstração');
 ({document}=await boot('/sobre-a-copia'));assert.match(document.querySelector('#r-main').textContent,/Limites da cópia/);
})().catch(e=>{console.error(e);process.exitCode=1});
