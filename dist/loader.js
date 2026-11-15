const snapshot=document.body.dataset.snapshot;
try {
 const response=await fetch(snapshot);
 if(!response.ok)throw new Error('Snapshot unavailable');
 const stream=response.body.pipeThrough(new DecompressionStream('gzip'));
 const html=await new Response(stream).text();
 const page=new DOMParser().parseFromString(html,'text/html');
 page.querySelectorAll('script').forEach(s=>s.remove());
 document.documentElement.lang=page.documentElement.lang||'pt-BR';
 document.head.replaceWith(document.importNode(page.head,true));
 document.body.replaceWith(document.importNode(page.body,true));
 const app=document.createElement('script');app.type='module';app.src='/app.js';document.body.append(app);
} catch(error) {
 console.error('Falha ao carregar a página capturada',error);
 document.body.innerHTML='<div class="loading"><p>Não foi possível carregar esta página.</p><p>Atualize a página ou use um navegador atualizado.</p><a href="/">Voltar ao início</a></div>';
}
