# Diagnóstico técnico de SEO – mgpecasautomotivas.com.br

Data: 27/10/2026 (15h–15h15, horário de Brasília). Somente leitura: nada foi alterado no tema, no painel nem no domínio.

## Resumo (o que mais importa)

1. **Domínio está certo.** O principal na Nuvemshop é mgpecasautomotivas.com.br. Todas as variações (mgmangueiras, www, http, lojavirtualnuvem) redirecionam com **301** para `https://mgpecasautomotivas.com.br/`, e os canonicals apontam para o domínio novo. O Google ainda tem **~889 páginas indexadas em mgmangueiras.com.br**. Isso deve sumir sozinho com o tempo por causa do 301. Dá para acelerar com o Search Console.
2. **As páginas de produto não têm dados estruturados `Product`.** Só têm `Organization` e `WebPage` com `BreadcrumbList`. Sem isso o Google não mostra estrelas, código nem imagem rica no resultado. Já nas listas (home, categorias), cada produto vem como `Product` com **`price: "0"`**. Para o Google isso é um preço errado (aparece como grátis) e pode gerar alerta no Merchant/Search Console.
3. **Nenhuma página tem `AggregateRating`.** As 3.651 avaliações do ML entram por JavaScript e não viram estrelas no Google.
4. **329 subcategorias (marca dentro de linha) têm title e description genéricos**, por exemplo "Comprar FIAT em MG Peças Automotivas" e "Compre online FIAT por . Temos…". O texto vem cortado, com "por ." vazio e cara de loja. São quase todas iguais entre si.
5. **Velocidade no celular é fraca.** Home tem nota 41 e LCP de 13,3 s em laboratório. Nos dados reais do Chrome (CrUX), as **Core Web Vitals estão reprovadas por causa do INP de 281 ms**. No PC a home vai bem (85).
6. **Search Console:** a conta logada no Chrome (filipefrancasilva10@gmail.com) **não tem acesso** à propriedade. O site tem uma meta tag `google-site-verification`, então alguma outra conta Google já verificou o site.
7. **Perfil da Empresa existe e está verificado.** O endereço e o site estão corretos. O telefone principal difere do site.
8. **Posição no Google:** para "MG001 mangueira" o site **não aparece com a página do MG001**. Só aparece em ~17º lugar (página 2), com o MG329. Para "mangueira filtro de ar palio MG", aparece em ~18º lugar (página 2), com o MG189. A página 1 inteira é ocupada por Mercado Livre, Magalu, Shopee e distribuidores.

---

## 1. Domínio, redirecionamentos e canonical

Domínios cadastrados na Nuvemshop (Configurações › Domínios), todos ativos e com SSL:

| Domínio | Papel |
|---|---|
| mgpecasautomotivas.com.br | **Principal** ★ |
| www.mgpecasautomotivas.com.br | alternativo |
| mgmangueiras.com.br | alternativo |
| www.mgmangueiras.com.br | alternativo |
| mgpecasautomotivas.lojavirtualnuvem.com.br | padrão da plataforma |

Teste com curl:

| URL de origem | Resultado |
|---|---|
| http://mgmangueiras.com.br | 301 → https://mgmangueiras.com.br/ → 301 → https://mgpecasautomotivas.com.br/ (2 saltos) |
| https://mgmangueiras.com.br | 301 → https://mgpecasautomotivas.com.br/ |
| https://www.mgmangueiras.com.br | 301 → https://mgpecasautomotivas.com.br/ |
| https://mgmangueiras.com.br/produtos/x | 301 → mesmo caminho no domínio novo (o caminho é preservado) |
| http://www.mgpecasautomotivas.com.br | 301 → https://www… → 301 → https://mgpecasautomotivas.com.br/ (2 saltos) |
| https://www.mgpecasautomotivas.com.br | 301 → https://mgpecasautomotivas.com.br/ |
| http://mgpecasautomotivas.com.br | 301 → https://mgpecasautomotivas.com.br/ |
| …lojavirtualnuvem.com.br | 301 → https://mgpecasautomotivas.com.br/ |

- Canonical em home, categorias, produtos e páginas: sempre `https://mgpecasautomotivas.com.br/...`, com barra no final. ✅
- Paginação: `?page=2` tem canonical `/mangueira-filtro-de-ar/page/2/`. ✅
- O link `mgmangueiras.com.br/produtos/...` que a API devolve é só o "permalink" interno da Nuvemshop. Para o visitante e para o Google, o 301 resolve.
- Redirecionamentos 301 manuais no painel: 4. Dois deles parecem invertidos ou estranhos: `/produtos/mg4170/ → /produtos/mg41701/` e `/produtos/mg1738/ → /produtos/mg17381/`. O produto ficou com URL "mg41701"/"mg17381" em vez do código limpo. Vale conferir depois.

## 2. robots.txt e sitemap.xml

- **robots.txt** é o padrão da Nuvemshop e está bom. Bloqueia admin, checkout, conta, busca interna e `?view=`. Aponta 2 sitemaps no CDN (`dcdn-us.mitiendanube.com/.../sitemap.xml.gz` e `sitemap_blog.xml.gz`), que têm o mesmo conteúdo do `/sitemap.xml`.
- **/sitemap.xml** existe (200) e usa só o domínio certo (0 ocorrências de mgmangueiras).
  - **2.598 URLs**: 2.239 produtos, ~343 categorias/subcategorias e 16 páginas/outros. Tem 3.334 imagens declaradas.
  - Problema: **5 URLs do sitemap dão 404**: `/garantia/`, `/qualidade/`, `/seja-representante/`, `/trabalhe-conosco/` e `/politica-de-privacidade-v2/`. Devem ser páginas em rascunho ou ocultas que continuam listadas.
  - O sitemap inclui `/sitemap_blog.xml/` como se fosse uma página. Não tem efeito, é só ruído.
  - O link antigo `/baixecatalogo/` dá 404. O menu já foi trocado para /catalogo/, mas se houver link externo ou antigo para ele, vale criar um 301 para `/catalogo/`.

## 3. Análise página por página

Legenda: H1 = quantos H1 visíveis depois do JavaScript. JSON-LD = tipos encontrados.

| Página | Title | Meta description | H1 | og:title / og:image | JSON-LD |
|---|---|---|---|---|---|
| Home `/` | "MG Peças Automotivas" (curto, sem palavra-chave) | ok (fabricante, Diadema, distribuidores) | 1, **oculto** ("MG Peças Automotivas") | sim / logo (http) | Organization, WebPage, 20× Product (price 0) |
| Catálogo `/catalogo/` | ok | ok | **2** ("Catálogo" + "O catálogo completo…") | **não tem** | Organization, WebPage |
| Quem somos | ok | ok | 1 | **não tem** | Organization, WebPage |
| Busca por veículo | "Busca por veículo" (sem marca) | ok | 1 | **não tem** | Organization, WebPage |
| Avaliações | ok | ok | **2** ("Avaliações" + "Quem usa, recomenda") | **não tem** | Organization, WebPage (sem AggregateRating) |
| Política de privacidade | ok | ok | 1 | **não tem** | Organization, WebPage |
| Eventos | ok | ok | 1 | **não tem** | Organization, WebPage |
| Cat. Mangueiras do Filtro de Ar | ok | ok | 1 (MAIÚSCULAS) | sim / logo | Org, WebPage (breadcrumb), 12× Product (price 0) |
| Cat. Mangueiras do Radiador | ok | ok | 1 (MAIÚSCULAS) | sim / logo | Org, WebPage, 12× Product (price 0) |
| Subcat. Coifas › Lado roda › Fiat | **"Comprar FIAT em MG Peças Automotivas"** | **"Compre online FIAT por . Temos coifa…"** (gerada) | 1 ("FIAT") | sim / logo | Org, WebPage, 6× Product |
| /produtos/ (todos) | "Compre online produtos de…" (tom de loja) | igual à da home | 1 | sim / logo | Org, WebPage, 12× Product |
| Produto MG001 | ok (código + carro + motor + anos) | ok (cita OEM) | 1 | sim / foto do produto | **só Organization + WebPage/Breadcrumb, sem Product** |
| Produto MG1838 | ok | ok | 1 | sim / foto | idem, sem Product |
| Produto MG020 | ok | ok | 1 | sim / foto | idem, sem Product |

Observações:

- **H1 do produto**: no HTML original o H1 é o nome completo ("Mangueira do Filtro de Ar Fiat Palio 1.0 e Siena 1.0 8V 1996 a 2000 - MG001"). Depois do script, o H1 visível vira só "Mangueira do Filtro de Ar". O Google renderiza JavaScript, então pode ler o H1 curto, sem código e sem carro. Sugestão: manter o nome completo no H1, ou ao menos o código.
- **Home**: o H1 está escondido por CSS. Falta um H1 visível com a frase principal, por exemplo "Fabricante de mangueiras automotivas…".
- **Páginas de conteúdo** (Catálogo, Avaliações): 2 H1 visíveis. O título do tema e o título do bloco competem; o do bloco devia ser H2. Em todas as páginas de conteúdo, o HTML bruto também traz o H1 do bloco do catálogo, que o guard JS remove fora de /catalogo/. Não é grave.
- **og:image** é sempre `http://` (sem s) em og:image e twitter:image. O `og:image:secure_url` está em https, mas o ideal é https direto. Páginas de conteúdo não têm og:title nem og:image: ao compartilhar no WhatsApp, sai sem imagem ou com imagem aleatória.
- **Imagens sem alt**: as fotos de produto têm alt. As **15 imagens sem alt** aparecem iguais em todas as páginas: são as miniaturas do menu Produtos, colocadas pelo script do Rodapé. A home tem 19 sem alt (as 15 do menu + 4 dos blocos Código).
- **`brand` no JSON-LD** das listas está como `@type: Thing`. O certo é `Brand`.

## 4. Google Search Console e Perfil da Empresa

- **Search Console**: no Chrome está logada a conta **filipefrancasilva10@gmail.com**. Ela não tem nenhuma propriedade (a tela é de boas-vindas) e, ao abrir `sc-domain:mgpecasautomotivas.com.br`, aparece "você não tem acesso a esta propriedade".
  - O HTML do site tem `<meta name="google-site-verification" …>`, ou seja, **alguma outra conta Google já verificou o site** (talvez a conta da agência antiga, ou uma conta @mgpecasautomotivas.com.br). O Filipe precisa descobrir qual é, ou verificar com a conta dele (pelo DNS no Cloudflare, propriedade de domínio, que cobre www e http). Também vale **adicionar mgmangueiras.com.br** e usar "Mudança de endereço" para o domínio novo.
  - Também tem GA4 (`G-2FHT62TP20`) e GTM (`GTM-MWQR7NVM`) instalados.
- **Perfil da Empresa (Google Meu Negócio)**: **existe e é gerenciado** pela conta logada ("Sua empresa no Google", 995 interações, força do perfil "Tudo certo").
  - Nome: MG Peças Automotivas. Categoria: Fabricante de autopeças.
  - Endereço: **Av. Casa Grande, 1534 – Casa Grande, Diadema-SP, 09961-350** ✅
  - Site: **mgpecasautomotivas.com.br** ✅
  - Telefone: (11) 4067-5766. O site e o Baixe Catálogo usam (11) 4049-5817 como principal. Não está errado, mas vale padronizar.
  - Avaliações: 4,4 (8 avaliações). Último post do proprietário em 13/08/2026. 7.154 visualizações.
  - Sugestões do próprio Google: incluir fotos internas e gerar link/QR para pedir avaliações.

## 5. PageSpeed Insights (pagespeed.web.dev, 27/10 ~15h)

| Página | Aparelho | Desempenho | Acessib. | Boas práticas | SEO | FCP | LCP | TBT | CLS |
|---|---|---|---|---|---|---|---|---|---|
| Home | Celular | **41** | 94 | 100 | 100 | 4,2 s | **13,3 s** | 840 ms | 0,024 |
| Home | PC | 85 | 94 | 100 | 100 | 0,8 s | 1,3 s | 270 ms | 0,004 |
| Produto MG001 | Celular | **61** | 86 | 100 | 100 | 3,2 s | 3,6 s | **1.060 ms** | 0,02 |
| Produto MG001 | PC | 69 | 87 | 100 | 100 | 0,8 s | 0,9 s | **1.010 ms** | 0,063 |

**Dados reais (CrUX, 28 dias, celular, home):** LCP 2,2 s ✅, **INP 281 ms ⚠️**, CLS 0 ✅, FCP 1,3 s, TTFB 0,5 s. Resultado: **Core Web Vitals reprovadas por causa do INP**. O produto só tem dado da origem (site todo), também reprovado.

Os 3 principais problemas:

1. **Imagens pesadas**: "Melhorar a entrega de imagens", com economia de 591 KiB no celular e 775 KiB no PC na home. Os maiores culpados devem ser a foto em data URI e os logos e vídeo dos blocos Código da home.
2. **Recursos que bloqueiam a renderização**: economia de 780 ms na home celular e 1.170 ms no produto celular. São CSS e JS no `<head>` (os 3 `@import` do CSS personalizado entram aqui, porque @import é carregado em série).
3. **Excesso de JavaScript**: TBT de ~1 s no produto e "Reduza o tempo de execução de JavaScript" (2,1 s). É isso que derruba o INP. Entram aí os scripts do tema, GTM, avaliações e busca. Também aparecem cache curto (economia de 238–356 KiB) e "JavaScript legado" (32 KiB).

Acessibilidade: elementos `aria-hidden` com itens focáveis e contraste insuficiente de algumas cores.

## 6. Presença no Google

| Busca | Resultado |
|---|---|
| `site:mgpecasautomotivas.com.br` | **~1.670 resultados** (de 2.598 no sitemap) |
| `site:mgmangueiras.com.br` | **~889 resultados** (domínio antigo ainda indexado: coifas, produtos, mg1625…) |
| `MG001 mangueira` | Página 1: ML, Minas Peças, Adecar, D.Marcas, Bauspec, Shopee, Furlan, Zezinho + painel de IA. **A página do MG001 não aparece.** O site só aparece em ~**17º** (página 2) com `/produtos/mg329/`. |
| `mangueira filtro de ar palio MG` | Página 1 sem o site. Aparece em ~**18º** (página 2) com `/produtos/mg189/`. |
| `MG Peças Automotivas Diadema` (extra) | 1º lugar com sitelinks (Produtos, Contato, Quem somos…) + Perfil da Empresa. Um sitelink mostra "Compre online CHEVROLET por . Temos…", a description gerada das subcategorias. Em 2º aparece `www.mgmangueiras.com.br/quem-somos` (domínio antigo). |

Obs.: a busca foi feita logada (conta Google do Filipe), então as posições são aproximadas.

## 7. O que fazer depois (sugestão de prioridade, nada foi feito)

1. Ganhar acesso ao **Search Console** (verificar por DNS no Cloudflare com a conta do Filipe), enviar o sitemap e fazer a **Mudança de endereço** de mgmangueiras → mgpecasautomotivas.
2. Colocar **JSON-LD `Product`** nas páginas de produto (nome, sku = código MG, mpn/OEM, imagem, brand MG, `aggregateRating` quando houver avaliação ML). Pode ser feito pelo script do tema ou pelo GTM. **Tirar `offers` com price 0** das listas, ou usar um Offer sem preço.
3. **Titles e descriptions das 329 subcategorias** ("Coifas Lado Roda Fiat | MG…" em vez de "Comprar FIAT em…"). Dá para fazer em lote pela API de categorias (campos SEO).
4. Manter o **H1 completo** no produto; criar H1 visível na home; trocar o 2º H1 por H2 em Catálogo e Avaliações.
5. Desempenho no celular: reduzir as imagens da home (tirar data URI, usar WebP pequeno), trocar os `@import` por `<link>`, adiar scripts não essenciais (avaliações e menu depois do load).
6. Limpar o sitemap: publicar ou excluir as 5 páginas 404; criar 301 `/baixecatalogo/` → `/catalogo/`; conferir os 301 de mg4170 e mg1738.
7. Pôr og:image (https) nas páginas de conteúdo; colocar alt nas miniaturas do menu.
8. Perfil da Empresa: padronizar o telefone, postar com mais frequência e pedir avaliações (link/QR).
