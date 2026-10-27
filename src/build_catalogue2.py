import json, base64, html, os, re
D=json.load(open('products_final.json')); P=[p for p in D['products'] if p['show']=='Y']
esc=html.escape
def b64(p,m='image/jpeg'): return f'data:{m};base64,'+base64.b64encode(open(p,'rb').read()).decode()
SHADE=b64('rm_b.png','image/png')
LOGO=b64('../assets/carpenta_logo.png','image/png')

PAINT={'PA12':'#383E42','BP 580 25 AGT':'#F2F0EB','BP 580 25':'#1A1A1A','BS600':'#6B4A2F',
 'BS600 -00':'#C49A62','BN1001810':'#E5A000','BN1008506':'#4A2B20','ST00005':'#C8961E',
 'RP1003205':'#BE1A20','TETB002':'#D4A017','TETB001':'#B6B8BA','BP580.25':'#1A1A1A',
 'PUB18KG':'#EFEDE8','RAL 5017':'#063971','RAL 1024':'#BA8F4C','RAL 3020':'#CC0605','RAL 1023':'#F0CA00'}
LOCAL={}
for f in os.listdir('../photos'): LOCAL['photos/'+f]=b64('../photos/'+f)
TEX={'photos/tex_a58e8c40.jpg':b64('tex_a58e8c40.jpg'),'photos/tex_c1913c9c.jpg':b64('tex_c1913c9c.jpg')}

def shot(p):
    if p['sub']=='EDGE BANDS':
        if p.get('crop'):
            cs=" ".join("%.5f"%v for v in p['crop'])
            inner=f'<i class="rd" data-img="{esc(p["img"])}" data-crop="{cs}"></i>'
        elif p.get('band_colour'):
            t=p.get('band_tex')
            bg=(f'background-color:{p["band_colour"]};background-image:url({TEX[t]});'
                f'background-size:62% auto;background-repeat:repeat') if t else f'background-color:{p["band_colour"]}'
            inner=f'<i class="rd" style="{bg}"></i>'
        else:
            inner=f'<i class="rd" style="background:#9aa0a8"></i>'
        return f'<div class="roll">{inner}<i class="rs"></i></div>'
    if p.get('local'): return f'<img src="{LOCAL[p["local"]]}" alt="" loading="lazy">'
    if p['itype']=='Colour guide':
        c=PAINT.get(p['sku'],'#8b8b86')
        return f'<div class="swatch" style="--c:{c}"><span>{esc(p["sku"])}</span></div>'
    if p['img']: return f'<img src="{esc(p["img"])}" alt="" loading="lazy">'
    w=[x for x in re.split(r'[^A-Za-z0-9]+',p['name']) if x][:2]
    return f'<div class="tile"><b>{esc(" ".join(w))[:16]}</b><em>photo to come</em></div>'

def money(v):
    try: return f'{float(v):,.0f}'
    except: return '—'

ORDER=['BOARDS','FURNITURE HARDWARE','CARPENTRY TOOLS','APPLIANCES','PAINTS & FINISHES']
cats={}
for p in P: cats.setdefault(p['cat'] or 'OTHER',[]).append(p)
def catkey(c):
    for i,o in enumerate(ORDER):
        if c.startswith(o.split()[0]): return (i,c)
    return (9,c)

body=''
for cat in sorted(cats,key=catkey):
    items=sorted(cats[cat],key=lambda p:((p['sub'] or 'zzz'),p['name']))
    body+=f'''<section class="divider"><div><span class="eyebrow">Carpenta</span>
      <h2>{esc(cat)}</h2><p>{len(items)} products</p></div></section>'''
    cards=''
    for p in items:
        cards+=f'''<article class="card">
          <div class="shot">{shot(p)}</div>
          <div class="info"><div class="grp">{esc(str(p['sub'] or cat))}</div>
          <h3>{esc(p['name'])}</h3>
          <div class="price">GHS <b>{money(p['price'])}</b></div>
          <div class="sku">{esc(p['sku'])}</div></div></article>'''
    body+=f'<section class="grid" data-cat="{esc(cat)}">{cards}</section>'

HTML=f'''<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Carpenta Product Catalogue</title><style>
@page{{size:A4 portrait;margin:11mm 10mm 13mm}}
*{{box-sizing:border-box}}
:root{{--ink:#0b1016;--panel:#161d27;--line:#273243;--paper:#f4f1ec;--muted:#8e99a8;--brass:#c9a227}}
html,body{{margin:0}}
body{{background:var(--ink);color:#eef1f5;
 font:15px/1.4 "Helvetica Neue",Helvetica,-apple-system,"Segoe UI",system-ui,sans-serif;
 -webkit-font-smoothing:antialiased}}
.cover{{min-height:100vh;display:flex;flex-direction:column;justify-content:center;align-items:center;
 text-align:center;gap:26px;padding:60px 30px;border-bottom:1px solid var(--line)}}
.cover img{{width:210px;filter:invert(1)}}
.cover h1{{margin:0;font-size:31px;letter-spacing:.22em;font-weight:300}}
.cover .rule{{width:66px;height:2px;background:var(--brass)}}
.cover p{{margin:0;color:var(--muted);font-size:14px;letter-spacing:.11em;text-transform:uppercase}}
.divider{{display:flex;align-items:flex-end;padding:34px 30px 18px;border-bottom:1px solid var(--line);
 margin-bottom:22px}}
.eyebrow{{font-size:10px;letter-spacing:.3em;text-transform:uppercase;color:var(--brass)}}
.divider h2{{margin:6px 0 2px;font-size:25px;letter-spacing:.1em;font-weight:400}}
.divider p{{margin:0;color:var(--muted);font-size:12.5px;letter-spacing:.06em}}
.grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(208px,1fr));gap:15px;padding:0 30px 40px}}
.card{{background:var(--panel);border:1px solid var(--line);border-radius:3px;overflow:hidden;
 display:flex;flex-direction:column;break-inside:avoid}}
.shot{{background:var(--paper);aspect-ratio:4/3;display:flex;align-items:center;justify-content:center;
 padding:9px;position:relative}}
.shot img{{max-width:100%;max-height:100%;object-fit:contain;mix-blend-mode:multiply}}
.roll{{position:relative;height:100%;aspect-ratio:300/538}}
.rd{{position:absolute;inset:0;-webkit-mask-image:url({SHADE});mask-image:url({SHADE});
 -webkit-mask-size:contain;mask-size:contain;-webkit-mask-repeat:no-repeat;mask-repeat:no-repeat;
 -webkit-mask-position:center;mask-position:center}}
.rs{{position:absolute;inset:0;background:url({SHADE}) center/contain no-repeat;mix-blend-mode:multiply}}
.swatch{{width:100%;height:100%;background:var(--c);display:flex;align-items:flex-end;justify-content:flex-end;
 padding:7px;border-radius:2px}}
.swatch span{{font-size:9px;letter-spacing:.08em;color:#fff;mix-blend-mode:difference}}
.tile{{width:100%;height:100%;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:5px;
 background:repeating-linear-gradient(45deg,#eae6df 0 7px,#f4f1ec 7px 14px);color:#5d6673;border-radius:2px}}
.tile b{{font-size:12px;letter-spacing:.07em}} .tile em{{font-size:9.5px;font-style:normal;letter-spacing:.09em;
 text-transform:uppercase;color:#98a0ab}}
.info{{padding:11px 12px 13px;display:flex;flex-direction:column;flex:1}}
.grp{{font-size:9px;letter-spacing:.17em;text-transform:uppercase;color:var(--brass)}}
.card h3{{margin:5px 0 8px;font-size:12.5px;line-height:1.32;font-weight:600;letter-spacing:.01em}}
.price{{margin-top:auto;font-size:11px;letter-spacing:.09em;color:var(--muted)}}
.price b{{font-size:17.5px;color:#fff;letter-spacing:0;font-weight:600;margin-left:3px}}
.sku{{font-size:9.5px;color:#6c7786;letter-spacing:.09em;margin-top:3px;font-variant-numeric:tabular-nums}}
@media (max-width:760px){{.grid{{grid-template-columns:repeat(2,1fr);gap:11px;padding:0 16px 30px}}
 .divider{{padding:26px 16px 14px}}}}
@media print{{
 body{{background:#fff;color:#14181f}}
 .cover{{min-height:245mm;page-break-after:always;border:0}}
 .cover img{{filter:none}} .cover h1{{color:#0b1016}} .cover p{{color:#6b7480}}
 .divider{{page-break-before:always;border-bottom:1.4px solid #0b1016;padding:0 0 7mm;margin-bottom:7mm}}
 .divider h2{{color:#0b1016}} .divider p{{color:#6b7480}}
 .grid{{grid-template-columns:repeat(3,1fr);gap:4mm;padding:0}}
 .shot{{aspect-ratio:3/2;padding:2mm}}
 .info{{padding:2.4mm 2.6mm 2.8mm}}
 .grp{{font-size:6pt;letter-spacing:.13em}}
 .card h3{{font-size:7.6pt;margin:1mm 0 1.4mm;line-height:1.26}}
 .price{{font-size:6.4pt}} .price b{{font-size:11pt}}
 .sku{{font-size:5.8pt;margin-top:.6mm}}
 .card{{background:#fff;border:.7px solid #c8ccd3;break-inside:avoid;page-break-inside:avoid}}
 .shot{{background:#fff;border-bottom:.7px solid #e4e7eb}}
 .card h3{{color:#14181f}} .price b{{color:#0b1016}} .sku{{color:#78818e}}
 .grp{{color:#8a6a06}}
}}
</style></head><body>
<header class="cover"><img src="{LOGO}" alt="Carpenta">
<div class="rule"></div><h1>PRODUCT CATALOGUE</h1>
<p>{len(P)} products &nbsp;·&nbsp; Prices in Ghana Cedis</p></header>
{body}
<script>
document.querySelectorAll('.rd[data-crop]').forEach(el=>{{
  const [fx,fy,fw,fh]=el.dataset.crop.split(' ').map(Number);
  const im=new Image();
  im.onload=()=>{{const W=im.naturalWidth,H=im.naturalHeight;
    const cx=fx*W,cy=fy*H,cw=fw*W,ch=fh*H;
    const bw=el.clientWidth,bh=el.clientHeight,s=Math.max(bw/cw,bh/ch);
    el.style.backgroundSize=(W*s)+'px '+(H*s)+'px';
    el.style.backgroundPosition=(-cx*s+(bw-cw*s)/2)+'px '+(-cy*s+(bh-ch*s)/2)+'px';
    el.style.backgroundRepeat='no-repeat';}};
  im.src=el.dataset.img; el.style.backgroundImage="url('"+el.dataset.img+"')";
}});
</script></body></html>'''
open('../output/Carpenta_Catalogue.html','w').write(HTML)
print('built', len(HTML)//1024,'KB ·',len(P),'products ·',len(cats),'categories')
