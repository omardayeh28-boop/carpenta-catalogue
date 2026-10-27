import json, html, base64
D=json.load(open('products_final.json'))
P=[p for p in D['products'] if p['itype']=='Designed tile' and p['show']=='Y']
esc=html.escape
def money(v):
    try: return f'{float(v):,.0f}'
    except: return '—'
LOGO='data:image/png;base64,'+base64.b64encode(open('../assets/carpenta_logo.png','rb').read()).decode()

ZONE=[('Paints, varnishes & solvents',lambda p:not p['sub'] and any(k in p['name'].upper() for k in
        ['VARNISH','VERNISH','HARDENER','HARDNER','THINNER','PRIMER','SEALER','PAINT','SOLVENT',
         'POLISH','FILLER','COMPAUND','ASETON','NODOSO','POLYGARD','FASTENER'])),
      ('Screws',lambda p:p['sub']=='SCREWS'),
      ('Appliances',lambda p:p['sub']=='BOSCH' or 'COOLER' in p['name'].upper()),
      ('Everything else',lambda p:True)]
groups=[]; left=list(P)
for name,f in ZONE:
    got=[p for p in left if f(p)]
    left=[p for p in left if p not in got]
    if got: groups.append((name,sorted(got,key=lambda p:p['name'])))

sec=''
for name,items in groups:
    rows=''.join(f'<tr><td class="tick"></td><td class="sku">{esc(p["sku"])}</td>'
                 f'<td>{esc(p["name"])}</td><td class="pr">{money(p["price"])}</td></tr>'
                 for p in items)
    sec+=f'''<section><h2>{esc(name)} <span>{len(items)}</span></h2>
      <table><thead><tr><th></th><th>SKU</th><th>Product</th><th>GHS</th></tr></thead>
      <tbody>{rows}</tbody></table></section>'''

HTML=f'''<!doctype html><html><head><meta charset="utf-8"><title>Carpenta — Photo Shoot List</title><style>
@page{{size:A4 portrait;margin:14mm 13mm}}
*{{box-sizing:border-box}}
body{{margin:0;font:12.5px/1.45 "Helvetica Neue",Helvetica,system-ui,sans-serif;color:#14181f;background:#fff}}
header{{display:flex;align-items:center;gap:18px;border-bottom:2px solid #0b1016;padding-bottom:12px;margin-bottom:16px}}
header img{{width:92px}}
h1{{margin:0;font-size:19px;letter-spacing:.1em;font-weight:600}}
header p{{margin:3px 0 0;color:#6b7480;font-size:12px}}
.how{{background:#f4f1ec;border-left:3px solid #c9a227;padding:12px 15px;margin-bottom:20px;font-size:12px}}
.how>b{{display:block;margin-bottom:5px;letter-spacing:.08em;text-transform:uppercase;font-size:10.5px}}
.how li{{margin:3px 0}} .how ul{{margin:0;padding-left:17px}}
section{{break-inside:avoid;margin-bottom:20px}}
h2{{font-size:13px;letter-spacing:.09em;text-transform:uppercase;margin:0 0 7px;
 border-bottom:1px solid #c8ccd3;padding-bottom:5px}}
h2 span{{color:#c9a227;font-weight:400}}
table{{width:100%;border-collapse:collapse}}
th{{text-align:left;font-size:9.5px;letter-spacing:.12em;text-transform:uppercase;color:#78818e;
 padding:3px 6px;font-weight:600}}
td{{padding:5px 6px;border-bottom:1px solid #e8eaee;font-size:12px}}
.tick{{width:17px}} .tick::before{{content:"";display:block;width:11px;height:11px;border:1.3px solid #9aa2ad;border-radius:2px}}
.sku{{width:110px;color:#5d6673;font-variant-numeric:tabular-nums;font-size:11px}}
.pr{{width:62px;text-align:right;font-variant-numeric:tabular-nums;color:#5d6673}}
@media print{{.how{{break-inside:avoid}}}}
</style></head><body>
<header><img src="{LOGO}" alt="Carpenta"><div><h1>PHOTO SHOOT LIST</h1>
<p>{len(P)} products still without a picture &nbsp;·&nbsp; tick each one as you shoot it</p></div></header>
<div class="how"><b>How to shoot these</b><ul>
<li>Plain white background — a sheet of white board or paper works.</li>
<li>Daylight, near a window. <b>No flash.</b></li>
<li>One product per frame, straight on, filling most of the frame.</li>
<li>If there is a label, turn it to face the camera.</li>
<li><b>Name every file with the SKU</b> — for example <code>AKD3518.jpg</code>. This is what lets the photo go
straight into the catalogue and the website without anyone matching it up by hand.</li>
</ul></div>
{sec}</body></html>'''
open('../output/Carpenta_Photo_Shoot_List.html','w').write(HTML)
print('shoot list', len(P), 'items /', len(groups),'groups')
