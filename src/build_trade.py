import json, html, base64
D=json.load(open('products_final.json')); P=[p for p in D['products'] if p['show']=='Y']
esc=html.escape
def money(v):
    try: return f'{float(v):,.0f}'
    except: return '—'
LOGO='data:image/png;base64,'+base64.b64encode(open('../assets/carpenta_logo.png','rb').read()).decode()
ORDER=['BOARDS','FURNITURE','CARPENTRY','APPLIANCES','PAINTS']
def catkey(c):
    for i,o in enumerate(ORDER):
        if c.startswith(o): return (i,c)
    return (9,c)
cats={}
for p in P: cats.setdefault(p['cat'] or 'OTHER',[]).append(p)
sec=''
for cat in sorted(cats,key=catkey):
    subs={}
    for p in cats[cat]: subs.setdefault(p['sub'] or '—',[]).append(p)
    blocks=''
    for sub in sorted(subs):
        rows=''.join(f'<tr><td class="sku">{esc(p["sku"])}</td><td>{esc(p["name"])}</td>'
                     f'<td class="pr">{money(p["price"])}</td></tr>'
                     for p in sorted(subs[sub],key=lambda p:p['name']))
        blocks+=f'<tbody class="grp"><tr class="sh"><td colspan="3">{esc(sub)}</td></tr>{rows}</tbody>'
    sec+=f'''<section><h2>{esc(cat)}<span>{len(cats[cat])}</span></h2>
      <table><thead><tr><th>SKU</th><th>Product</th><th class="pr">GHS</th></tr></thead>{blocks}</table></section>'''
HTML=f'''<!doctype html><html><head><meta charset="utf-8"><title>Carpenta — Trade Price List</title><style>
@page{{size:A4 portrait;margin:13mm 12mm}}
*{{box-sizing:border-box}}
body{{margin:0;font:12px/1.4 "Helvetica Neue",Helvetica,system-ui,sans-serif;color:#14181f;background:#fff}}
header{{display:flex;align-items:center;gap:18px;border-bottom:2px solid #0b1016;padding-bottom:12px;margin-bottom:18px}}
header img{{width:92px}} h1{{margin:0;font-size:19px;letter-spacing:.1em;font-weight:600}}
header p{{margin:3px 0 0;color:#6b7480;font-size:11.5px}}
section{{margin-bottom:22px}}
h2{{font-size:13px;letter-spacing:.1em;text-transform:uppercase;margin:0 0 6px;display:flex;
 justify-content:space-between;border-bottom:2px solid #0b1016;padding-bottom:5px}}
h2 span{{color:#c9a227;font-weight:400;font-size:11px}}
table{{width:100%;border-collapse:collapse}}
th{{text-align:left;font-size:9px;letter-spacing:.14em;text-transform:uppercase;color:#78818e;padding:3px 6px}}
td{{padding:3.4px 6px;border-bottom:1px solid #eceef1;font-size:11.5px}}
.sh td{{background:#f4f1ec;font-size:9.5px;letter-spacing:.13em;text-transform:uppercase;
 font-weight:700;color:#5d6673;border-bottom:1px solid #d9dde2;padding:4px 6px}}
.grp{{break-inside:auto}} tr{{break-inside:avoid}}
.sku{{width:112px;color:#5d6673;font-size:10.5px;font-variant-numeric:tabular-nums}}
.pr{{width:74px;text-align:right;font-variant-numeric:tabular-nums;font-weight:600}}
</style></head><body>
<header><img src="{LOGO}" alt="Carpenta"><div><h1>TRADE PRICE LIST</h1>
<p>{len(P)} products &nbsp;·&nbsp; prices in Ghana Cedis</p></div></header>
{sec}</body></html>'''
open('../output/Carpenta_Trade_Price_List.html','w').write(HTML)
print('trade list', len(P),'rows /',len(cats),'categories')
