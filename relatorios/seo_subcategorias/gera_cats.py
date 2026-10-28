import json, re, collections, csv
r = json.load(open('cats.json', encoding='utf8'))

MARCAS = {'AUDI': 'Audi', 'BMW': 'BMW', 'CASE': 'Case', 'CHERY': 'Chery', 'CHEVROLET': 'Chevrolet', 'CITROEN': 'Citroën',
          'DODGE': 'Dodge', 'FIAT': 'Fiat', 'FORD': 'Ford', 'HONDA': 'Honda', 'HYUNDAI': 'Hyundai', 'IVECO': 'Iveco',
          'JEEP': 'Jeep', 'KIA': 'Kia', 'LIFAN': 'Lifan', 'MERCEDES-BENZ': 'Mercedes-Benz', 'MINI': 'Mini',
          'MITSUBISHI': 'Mitsubishi', 'NISSAN': 'Nissan', 'PEUGEOT': 'Peugeot', 'RAM': 'RAM', 'RENAULT': 'Renault',
          'SCANIA': 'Scania', 'SEAT': 'Seat', 'TOYOTA': 'Toyota', 'TROLLER': 'Troller', 'VOLKSWAGEN': 'Volkswagen',
          'VOLVO': 'Volvo', 'OUTRAS MONTADORAS': 'Outras Montadoras'}
# nome do tipo de peça (singular, legível) por caminho; chave = nomes da trilha sem a marca
TIPO = {
    ("BOMBA D’ÁGUA",): "Bomba d'Água",
    ('COIFAS', 'CAIXA DE DIREÇÃO'): 'Coifa da Caixa de Direção',
    ('COIFAS', 'INTERNA E EXTERNA'): 'Coifa da Homocinética Interna e Externa',
    ('COIFAS', 'LADO CAMBIO'): 'Coifa da Homocinética Lado Câmbio',
    ('COIFAS', 'LADO RODA'): 'Coifa da Homocinética Lado Roda',
    ('COIFAS', 'QUADRICICLO'): 'Coifa para Quadriciclo',
    ('COIFAS', 'SEMI-EIXO'): 'Coifa do Semi-eixo',
    ('DIVERSOS', 'MANG. DE ALIMENTAÇÃO'): 'Mangueira de Alimentação de Combustível',
    ('DIVERSOS', 'MANG. DO CÂNISTER'): 'Mangueira do Cânister',
    ('DIVERSOS', 'MANGUEIRA RETORNO COMBUSTÍVEL'): 'Mangueira de Retorno de Combustível',
    ('DIVERSOS', 'TAMPAS'): 'Tampa',
    ('DIVERSOS', 'OUTROS'): 'Peças Diversas',
    ('DIVERSOS', 'SISTEMA DE ARREFECIMENTO'): 'Peça do Sistema de Arrefecimento',
    ('DIVERSOS', 'SISTEMA DE DIREÇÃO'): 'Peça do Sistema de Direção',
    ('DIVERSOS', 'EMBREAGEM'): 'Peça de Embreagem',
    ('DIVERSOS', 'JUNTAS'): 'Junta',
    ('MANGUEIRAS DE DIREÇÃO HIDRÁULICA',): 'Mangueira de Direção Hidráulica',
    ('MANGUEIRAS DO FILTRO DE AR',): 'Mangueira do Filtro de Ar',
    ('MANGUEIRAS DO RADIADOR',): 'Mangueira do Radiador',
    ('MANGUEIRAS DO RADIADOR', 'FORD', 'MANGUEIRA DE ARREFECIMENTO'): 'Mangueira de Arrefecimento',
    ('METAL BORRACHA', 'BUCHAS'): 'Bucha',
    ('METAL BORRACHA', 'COMPONENTES METALICOS'): 'Componente Metálico',
    ('METAL BORRACHA', 'SUPORTE DO AMORTECEDOR'): 'Suporte do Amortecedor',
    ('METAL BORRACHA', 'SUPORTE DO MOTOR - CÂMBIO'): 'Coxim do Motor e Câmbio',
    ('METAL BORRACHA', 'BATENTE DA SUSPENSÃO '): 'Batente da Suspensão',
    ('PEÇAS PLÁSTICAS', 'ANTICHAMAS'): 'Antichamas',
    ('PEÇAS PLÁSTICAS', 'CARCAÇA DA VALVULA TERMOSTÁTICA'): 'Carcaça da Válvula Termostática',
    ('PEÇAS PLÁSTICAS', 'COMPONENTES DE VEDAÇÃO'): 'Componente de Vedação',
    ('PEÇAS PLÁSTICAS', 'FLANGES E CONECTORES'): 'Flange e Conector',
    ('PEÇAS PLÁSTICAS', 'KITS'): 'Kit de Peças Plásticas',
    ('PEÇAS PLÁSTICAS', 'TERMOSTATO'): 'Válvula Termostática',
    ('PEÇAS PLÁSTICAS', 'TUBOS'): 'Tubo de Água',
    ('PEÇAS PLÁSTICAS', 'VÁLVULAS DE CONTROLE'): 'Válvula de Controle',
    ('RESERVATÓRIOS',): 'Reservatório de Água',
    ('RESPIRO E RABICHOS',): 'Mangueira de Respiro e Rabicho',
    ('TAMPAS DE COMANDO DE VÁLVULAS',): 'Tampa de Válvulas',
    ('LINHA PESADA',): 'Peça para Linha Pesada',
    ('SUSPENSÃO - LINHA NOVA', 'BATENTES'): 'Batente da Suspensão',
    ('SUSPENSÃO - LINHA NOVA', 'BUCHAS'): 'Bucha da Suspensão',
    ('SUSPENSÃO - LINHA NOVA', 'COIFAS DE AMORTECEDOR'): 'Coifa do Amortecedor',
    ('SUSPENSÃO - LINHA NOVA', 'COXINS'): 'Coxim',
    ('SUSPENSÃO - LINHA NOVA', 'GUARNIÇÕES E VEDAÇÕES'): 'Guarnição e Vedação',
    ('SUSPENSÃO - LINHA NOVA', 'KITS DE REPARO'): 'Kit de Reparo da Suspensão',
    ('SUSPENSÃO - LINHA NOVA', 'MANCAIS E BIELETAS'): 'Mancal e Bieleta',
    ('SUSPENSÃO - LINHA NOVA', 'OUTROS'): 'Peça de Suspensão',
    ('TAMPAS DE RESERVATÓRIO',): 'Tampa de Reservatório',
}
PLURAL = {}  # títulos em singular funcionam bem para busca ("mangueira filtro de ar palio")

MARCA_RE = r'(Audi|BMW|Case|Chery|Chevrolet|GM|Citro[eë]n|Dodge|Fiat|Ford|Honda|Hyundai|Iveco|Jeep|Kia|Lifan|Mercedes[- ]Benz|Mercedes|Mini|Mitsubishi|Nissan|Peugeot|RAM|Ram|Renault|Scania|Seat|Toyota|Troller|Volkswagen|VW|Volvo)'
POP = ['gol','palio','uno','celta','corsa','onix','fiesta','ka','strada','saveiro','hb20','sandero','logan','fox','voyage','prisma','s10','hilux','civic','corolla','fit','ranger','focus','ecosport','siena','idea','punto','polo','golf','up','kwid','clio','kangoo','duster','tracker','cruze','astra','vectra','montana','spin','cobalt','meriva','agile','toro','argo','mobi','cronos','fiorino','doblo','ducato','weekend','courier','fusion','206','207','208','307','c3','c4','xsara','picasso','partner','berlingo','jumper','boxer','master','city','hr-v','cr-v','tucson','i30','creta','compass','renegade','l200','pajero','frontier','march','versa','sentra','etios','yaris','sprinter','daily','kombi','parati','santana','quantum','passat','jetta','tiguan','amarok','marea','tempra','premio','elba','escort','verona']
PARE = re.compile(r'^(\d|e$|a$|até|com|sem|motor|em|de|do|da|lado|-|–)', re.I)

def modelos(nomes, marca):
    c = collections.Counter()
    ordem = []
    for n in nomes:
        n = re.sub(r'\s[-–]\s*MG[\w-]*\s*$', '', n)
        for m in re.finditer(MARCA_RE + r'\s+(.*?)(?=$|\s' + MARCA_RE + r'\b)', n):
            resto = m.group(2)
            for parte in re.split(r',|\se\s|/', resto):
                pal = []
                for w in parte.strip().split():
                    if PARE.match(w) or re.match(r'^\d', w): break
                    pal.append(w)
                    if len(pal) == 2: break
                mod = ' '.join(pal).strip(' .')
                if len(mod) >= 2 and not re.match(MARCA_RE + '$', mod):
                    if mod not in c: ordem.append(mod)
                    c[mod] += 1
    outras = {'A3','A4','A5','A6','TT','S3','Q3','Q5','Q7'} if marca in ('Volkswagen','Seat') else set()
    ordem = [m for m in ordem if m not in outras and not re.match(r'^(\d|[IVX]+$)', m)]
    DONO = {}
    for mk, ls in {'Fiat':'palio uno strada siena idea punto toro argo mobi cronos fiorino doblo ducato marea tempra premio elba weekend',
                   'Chevrolet':'celta corsa onix prisma s10 tracker cruze astra vectra montana spin cobalt meriva agile',
                   'Volkswagen':'gol saveiro fox voyage polo golf up parati santana quantum passat jetta tiguan amarok kombi',
                   'Ford':'fiesta ka ranger focus ecosport courier fusion escort verona', 'Renault':'sandero logan kwid clio kangoo duster master',
                   'Hyundai':'hb20 tucson creta i30', 'Toyota':'hilux corolla etios yaris', 'Honda':'civic fit city hr-v cr-v', 'Citroën':'c3 c4 xsara picasso berlingo jumper aircross', 'Peugeot':'206 207 208 307 partner boxer hoggar'}.items():
        for w in ls.split(): DONO[w] = mk
    vistos = set(); limpa = []
    for m in ordem:
        p = m.split()[0].lower()
        if DONO.get(p, marca) != marca or p in vistos: continue
        vistos.add(p); limpa.append(m)
    ordem = limpa
    def peso(m):
        p = m.split()[0].lower()
        return (0 if p in POP else 1, POP.index(p) if p in POP else 0, -c[m])
    return sorted(ordem, key=peso)

def junta(l):
    return ', '.join(l[:-1]) + ' e ' + l[-1] if len(l) > 1 else ''.join(l)

out = []
for x in r:
    t = x['trilha']
    if len(t) < 2: continue  # linhas principais já têm título bom
    marca = MARCAS.get(t[-1].strip())
    chave = tuple(a for a in t if a.strip() not in MARCAS)
    if marca is None:  # subcategoria sem marca (ex.: COIFAS > LADO RODA)
        chave = tuple(t)
    tipo = TIPO.get(chave) or TIPO.get(tuple(t))
    if not tipo:
        out.append({'url': x['url'], 'erro': 'sem tipo ' + '>'.join(t)}); continue
    mods = modelos(x['produtos'], marca or '') if marca and marca != 'Outras Montadoras' else []
    alvo = tipo + (' ' + marca if marca else '')
    suf = ' | MG Peças Automotivas'
    tit = alvo + suf
    for k in range(min(4, len(mods)), 0, -1):
        cand = alvo + ' – ' + junta(mods[:k]) + suf
        if len(cand) <= 70: tit = cand; break
    if len(tit) > 70: tit = (alvo + ' | MG Peças')[:70]
    lista = junta(mods[:5])
    if marca and marca != 'Outras Montadoras':
        d = f"{tipo} para {marca}" + (f" {lista}" if lista else '') + ". Fabricação nacional MG, Diadema-SP. Veja código MG, número original (OEM) e aplicação."
    else:
        d = f"{tipo}" + (f" para {marca.lower()}" if marca else '') + ". Fabricação nacional MG, Diadema-SP. Veja código MG, número original (OEM) e aplicação de cada peça."
    if len(d) > 160:
        while len(d) > 160 and lista:
            mods = mods[:-1] if len(mods) > 1 else []
            lista = junta(mods[:min(5, len(mods))])
            d = f"{tipo} para {marca}" + (f" {lista}" if lista else '') + ". Fabricação nacional MG, Diadema-SP. Veja código MG, número original (OEM) e aplicação."
    out.append({'url': x['url'], 'trilha': ' > '.join(t), 'titulo_atual': x['title'], 'desc_atual': x['desc'],
                'titulo_novo': tit, 'desc_nova': d, 'n_tit': len(tit), 'n_desc': len(d), 'vazia': not x['produtos']})

json.dump(out, open('cats_seo.json', 'w', encoding='utf8'), ensure_ascii=False, indent=1)
with open('cats_seo.csv', 'w', encoding='utf-8-sig', newline='') as f:
    w = csv.DictWriter(f, fieldnames=['url', 'trilha', 'titulo_atual', 'titulo_novo', 'n_tit', 'desc_atual', 'desc_nova', 'n_desc', 'vazia', 'erro'], delimiter=';')
    w.writeheader(); [w.writerow(o) for o in out]
print(len(out), 'erros', [o for o in out if 'erro' in o][:5])
print('max tit', max(o.get('n_tit', 0) for o in out), 'max desc', max(o.get('n_desc', 0) for o in out))
