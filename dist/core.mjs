export const money=value=>new Intl.NumberFormat('pt-BR',{style:'currency',currency:'BRL'}).format(Number(value)||0);
export const norm=s=>String(s||'').normalize('NFD').replace(/[\u0300-\u036f]/g,'').toLowerCase();
export const escapeHTML=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
export function findProducts(products,term){const terms=norm(term).split(/\s+/).filter(Boolean);return products.filter(p=>terms.every(t=>norm(p.name+' '+p.slug+' '+(p.category||'')).includes(t)));}
export function itemKey(item){return [item.slug,item.option||'',item.device||'',item.custom||''].join('|');}
export function addItem(cart,item){const key=itemKey(item),old=cart.find(x=>x.key===key);return old?cart.map(x=>x.key===key?{...x,qty:Math.min(99,x.qty+(item.qty||1))}:x):[...cart,{...item,key,qty:Math.max(1,item.qty||1)}];}
export const subtotal=cart=>cart.reduce((s,x)=>s+Math.round(x.price*100)*x.qty,0)/100;
export function sortProducts(products,order){return [...products].sort(order==='price-asc'?(a,b)=>a.price-b.price:order==='price-desc'?(a,b)=>b.price-a.price:order==='name'?(a,b)=>a.name.localeCompare(b.name,'pt-BR'):order==='discount'?(a,b)=>(1-b.price/b.old_price)-(1-a.price/a.old_price):()=>0);}
