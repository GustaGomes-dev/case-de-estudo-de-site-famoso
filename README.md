# Case de estudo de site famoso — Gocase

Referência: https://www.gocase.com.br/ · captura de 14/11/2026.

Estudo independente de reprodução da experiência de uma loja conhecida, preparado para analisar o estado atual e mapear melhorias futuras. Não é um projeto oficial da Gocase.

A implementação preserva o HTML, CSS, textos, imagens e preços disponíveis nas páginas públicas capturadas. O inventário exato está em `coverage.json` e em `/sobre-a-copia` na aplicação. Não representa uma cópia integral do catálogo ou dos sistemas internos da Gocase.

## Executar e editar

```bash
git clone https://github.com/GustaGomes-dev/case-de-estudo-de-site-famoso.git
cd case-de-estudo-de-site-famoso
npm ci
npm run dev
```

Abra http://localhost:3000. Requisitos: Node.js 20 ou superior e Python 3.10 ou superior. A instalação npm fornece apenas a dependência dos testes; o site estático já está incluído em `dist/`.


O site é estático: `dist/index.html` e as demais rotas em `dist/`. Pode ser servido por qualquer servidor HTTP estático com suporte a `index.html` em subdiretórios. Não há dependências de produção nem etapa de compilação.

- `dist/app.js`: interações locais e reconexão dos controles capturados.
- `dist/core.mjs`: busca, ordenação e operações de carrinho.
- `dist/replica.css`: estilos dos fluxos locais de demonstração.
- `dist/assets/css`: estilos originais extraídos das capturas.
- `dist/assets/media`: imagens e fontes preservadas localmente.
- `dist/loader.js` e `dist/snapshots`: carregamento das capturas HTML compactadas para respeitar o limite de hospedagem. A página inicial permanece em HTML direto. Não altera o conteúdo das capturas.
- `dist/data`: catálogo capturado, descrições, variantes e inventário de cobertura.
- `scripts/`: scripts usados na captura e preparação. As capturas brutas ficam em `reference/`, ignorado pelo Git.

## Fluxos implementados

Página inicial, banners responsivos, carrossel, navegação, categorias e coleções capturadas; consulta de produtos; busca, filtros e ordenação no catálogo local; seleção de cor/modelo; favoritos; carrinho persistente; checkout simulado e pedido DEMO. Valores e disponibilidade refletem a data da captura. A seleção usa as opções e os preços capturados; o estoque não é sincronizado.

## Limitações conhecidas

- Catálogo completo e todas as suas páginas não foram capturados. Rotas auxiliares sem captura usam uma vitrine local.
- As vitrines dinâmicas da página inicial são preenchidas com produtos capturados, sem reproduzir recomendações e experimentos do site original.
- Login, cadastro e rastreamento real não estão integrados. Não há processamento de senha, Pix ou cartão, nem envio de pedidos reais.
- Frete e prazo exibidos no checkout são explicitamente fictícios para testar o fluxo.
- Cupons do site original não são aplicados. Dependem do serviço de promoções.
- A personalização com nome é uma prévia simplificada, sem o motor original de edição e renderização.
- Imagens de variantes que não foram armazenadas localmente podem usar o CDN público de origem.
- Validação visual em navegador não realizada: a ferramenta de navegador indicada pelo ambiente não estava disponível. Os testes de DOM não substituem inspeção visual.

## Verificação

```bash
npm test
npm run verify
```

Os testes usam LinkeDOM para validar inicial, carrossel, busca, detalhe de produto, variantes, carrinho, persistência e checkout. A verificação também confere os arquivos locais e as capturas compactadas.

Este repositório é público e a aplicação contém identificação discreta de ambiente de estudo. A hospedagem de revisão original tem acesso privado e não é alterada pela publicação deste repositório. Marca e conteúdos pertencem aos respectivos titulares e foram preservados como referência solicitada.

## Conteúdo e direitos

Marca, fotografias e textos de terceiros são materiais de referência do estudo, pertencem aos respectivos titulares e não recebem licença adicional por estarem neste repositório.
