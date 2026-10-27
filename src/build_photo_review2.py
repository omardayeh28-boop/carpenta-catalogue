import json, base64, os, html
D=json.load(open('products_final.json')); prods=D['products']
by={p['sku']:p for p in prods}; esc=html.escape
COL=json.load(open('roll_colours.json')); COL['12c126ff']='#bfbcb9'

def b64(p,m='image/jpeg'): return f'data:{m};base64,'+base64.b64encode(open(p,'rb').read()).decode()
SHADE=b64('rm_b.png','image/png')
TEX={n:b64(f'tex_{n}.jpg') for n in ['a58e8c40','c1913c9c']}

PHOTOS=[
 ('AKD3518','AKD3518.jpg','certain','Box reads 3.5X18 SUNTA VIDASI 1000 ADET'),
 ('AKD3550','AKD3550.jpg','certain','Box reads YHB SUNTA VIDASI 3,5x50 500 Adet'),
 ('SK3535','SK3535.jpg','certain','Knauf TN 3,5 × 35 mm, 1000 Stück'),
 ('SK3535','SK3535_alt.jpg','extra','Close-up of the same screw — keep as a second image, or use instead of the box'),
 ('HBF113B50B','HBF113B50B.jpg','likely','Series 2 built-in oven, stainless + black glass. Confirm it is this model and not HBF514BS0T'),
 ('H300','H300.jpg','likely','Light joiner’s hammer, short handle — reads as the 300 g'),
 ('BH001','BH001.jpg','likely','Long-handled builder’s hammer'),
 ('LPL10W','LPL10W.jpg','certain','White leg → the WHITE 10 cm'),
 ('LPL10G','LPL10G.jpg','certain','Grey leg → the GREY 10 cm'),
 ('MKL001','MKL001.jpg','guess','Black plinth leg with clip. Could equally be ST00472 — height decides'),
 ('ST00472','ST00472.jpg','guess','The taller black plinth leg. Swap with MKL001 if I have these the wrong way round'),
]
BANDS=[
 ('3736','bee6f100',None,'likely','HG = high gloss, matched to the gloss grey roll'),
 ('3501','7dfcfb4f',None,'guess','Luna read as the plain off-white. Tell me if Luna is a woodgrain'),
 ('3501ED','7dfcfb4f',None,'guess','Same decor as 3501, 4 mm instead of 2 mm'),
 ('3602','f3840773',None,'likely','Brick red supermatt — colour taken off the red roll you sent'),
 ('738AGT','af223a45',None,'guess','Clay read as the pale ivory'),
 ('TECE','a58e8c40','a58e8c40','likely','Kumsal = sand, matched to the cream woodgrain'),
 ('TECE40','c1913c9c','c1913c9c','likely','Same family as TECE, 40 mm'),
]

def roll(colour=None, tex=None, img=None, crop=None, h=190):
    if img and crop:
        cs=" ".join("%.5f"%v for v in crop)
        s=f'<div class="rd" data-img="{esc(img)}" data-crop="{cs}"></div>'
    elif tex:
        s=(f'<div class="rd" style="background-color:{colour};background-image:url(\'{TEX[tex]}\');'
           f'background-size:62% auto;background-repeat:repeat"></div>')
    else:
        s=f'<div class="rd" style="background-color:{colour}"></div>'
    return f'<div class="roll" style="height:{h}px">{s}<div class="rs"></div></div>'

def card(sku, inner, conf, note, mini=False):
    p=by.get(sku); nm=esc(p['name']) if p else sku
    pr=f"GHS {p['price']:,.0f}" if p and p.get('price') else ''
    grp=esc(str(p['sub'] or p['cat'])) if p else ''
    tag=f'<div class="conf c-{conf}">{conf}</div>' if conf else ''
    nt=f'<div class="note">{esc(note)}</div>' if note else ''
    btn='' if mini else ('<div class="btns"><button class="ok" onclick="mark(this,1)">Use it</button>'
                         '<button class="no" onclick="mark(this,0)">No</button></div>')
    return (f'<div class="card{" mini" if mini else ""}" data-sku="{esc(sku)}"><div class="shot">{inner}</div>'
            f'<div class="meta"><div class="grp">{grp}</div><div class="nm">{nm}</div>'
            f'<div class="sku">{esc(sku)}{"  ·  "+pr if pr else ""}</div>{tag}{nt}</div>{btn}</div>')

sec1=''.join(card(s,f'<img src="{b64("../photos/"+f)}" alt="">',c,n) for s,f,c,n in PHOTOS)
sec2=''.join(card(s,roll(colour=COL[k],tex=t),c,n) for s,k,t,c,n in BANDS)
exist=[p for p in prods if p['sub']=='EDGE BANDS' and p['img'] and p['crop']][:10]
sec3=''.join(card(p['sku'],roll(img=p['img'],crop=p['crop'],h=150),None,'',mini=True) for p in exist)

HTML=f'''<!doctype html><html><head><meta charset="utf-8">
<title>Carpenta — Photo Review 2</title><style>
*{{box-sizing:border-box}}
body{{margin:0;font:15px/1.45 -apple-system,"Segoe UI",system-ui,sans-serif;background:#f4f1ec;color:#141a24}}
header{{background:#0e1420;color:#fff;padding:26px 34px}}
header h1{{margin:0;font-size:21px;letter-spacing:.04em;font-weight:600}}
header p{{margin:7px 0 0;opacity:.72;font-size:13.5px;max-width:64ch}}
h2{{margin:42px 34px 4px;font-size:16px;letter-spacing:.05em;text-transform:uppercase}}
.sub{{margin:0 34px 16px;font-size:13.5px;color:#5d6673;max-width:72ch}}
.grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(215px,1fr));gap:16px;padding:0 34px}}
.card{{background:#fff;border-radius:10px;padding:14px;display:flex;flex-direction:column;box-shadow:0 1px 3px rgba(0,0,0,.07)}}
.card.sel-1{{outline:2px solid #22b24c}} .card.sel-0{{outline:2px solid #d14343;opacity:.45}}
.shot{{display:flex;align-items:center;justify-content:center;margin-bottom:10px;min-height:150px}}
.shot img{{max-width:100%;max-height:190px;object-fit:contain}}
.roll{{position:relative;aspect-ratio:300/538}}
.rd{{position:absolute;inset:0;-webkit-mask-image:url('{SHADE}');mask-image:url('{SHADE}');
 -webkit-mask-size:contain;mask-size:contain;-webkit-mask-repeat:no-repeat;mask-repeat:no-repeat;
 -webkit-mask-position:center;mask-position:center}}
.rs{{position:absolute;inset:0;background-image:url('{SHADE}');background-size:contain;
 background-repeat:no-repeat;background-position:center;mix-blend-mode:multiply}}
.grp{{font-size:10.5px;letter-spacing:.09em;text-transform:uppercase;color:#8b94a1}}
.nm{{font-size:13.5px;font-weight:600;margin:2px 0 3px;line-height:1.3}}
.sku{{font-size:12px;color:#5d6673;font-variant-numeric:tabular-nums}}
.conf{{display:inline-block;font-size:10.5px;letter-spacing:.07em;text-transform:uppercase;padding:2px 7px;
 border-radius:3px;margin:7px 0 5px;font-weight:600}}
.c-certain{{background:#e2f5e8;color:#17793a}} .c-likely{{background:#fdf3d8;color:#8a6a06}}
.c-guess{{background:#fde4e4;color:#a62c2c}} .c-extra{{background:#e8ecf2;color:#4a5566}}
.note{{font-size:12px;color:#5d6673;line-height:1.4}}
.btns{{margin-top:auto;padding-top:11px;display:flex;gap:7px}}
button{{flex:1;padding:7px;border:1px solid #cfd5dd;background:#fff;border-radius:6px;font:inherit;font-size:12.5px;cursor:pointer}}
button.ok:hover{{background:#e2f5e8;border-color:#22b24c}} button.no:hover{{background:#fde4e4;border-color:#d14343}}
#bar{{position:fixed;bottom:0;left:0;right:0;background:#0e1420;color:#fff;padding:13px 34px;
 display:flex;gap:16px;align-items:center;font-size:13.5px}}
#bar button{{flex:0 0 auto;background:#22b24c;border:0;color:#fff;padding:9px 18px;font-weight:600}}
footer{{height:72px}}
</style></head><body>
<header><h1>CARPENTA — PHOTO REVIEW 2</h1>
<p>The photos you sent, matched to SKUs. Green = I am sure. Amber = probably right.
Red = a real guess, please check. Mark anything wrong and send the result back.</p></header>

<h2>New product photos</h2>
<p class="sub">Ten products come off the shoot list if these are right, leaving 44.</p>
<div class="grid">{sec1}</div>

<h2>Edge bands that had no artwork at all</h2>
<p class="sub">These seven had nothing. I took the colour and grain off the roll photos you sent and
rendered them on a real roll. What needs checking is the decor match, not the roll.</p>
<div class="grid">{sec2}</div>

<h2>The roll upgrade</h2>
<p class="sub">The same real roll, with your own board decors laid into it — this replaces the drawn
artwork across all 40 edge bands. A sample below.</p>
<div class="grid">{sec3}</div>

<div id="bar"><span id="count">Nothing marked yet</span>
<button onclick="copyOut()">Copy result</button>
<span style="opacity:.6">then paste it back to Claude</span></div>
<footer></footer>
<script>
document.querySelectorAll('.rd[data-crop]').forEach(el=>{{
  const [fx,fy,fw,fh]=el.dataset.crop.split(' ').map(Number);
  const im=new Image();
  im.onload=()=>{{
    const W=im.naturalWidth,H=im.naturalHeight;
    const cx=fx*W,cy=fy*H,cw=fw*W,ch=fh*H;
    const bw=el.clientWidth,bh=el.clientHeight;
    const s=Math.max(bw/cw,bh/ch);
    el.style.backgroundSize=(W*s)+'px '+(H*s)+'px';
    el.style.backgroundPosition=(-cx*s+(bw-cw*s)/2)+'px '+(-cy*s+(bh-ch*s)/2)+'px';
    el.style.backgroundRepeat='no-repeat';
  }};
  im.src=el.dataset.img;
  el.style.backgroundImage="url('"+el.dataset.img+"')";
}});
const st={{}};
function mark(b,v){{const c=b.closest('.card');const k=c.dataset.sku+'|'+[...document.querySelectorAll('.card')].indexOf(c);
 st[k]=[c.dataset.sku,v];c.classList.remove('sel-0','sel-1');c.classList.add('sel-'+v);
 document.getElementById('count').textContent=Object.keys(st).length+' marked';}}
function copyOut(){{const ok=[],no=[];for(const k in st){{(st[k][1]?ok:no).push(st[k][0]);}}
 navigator.clipboard.writeText('CARPENTA PHOTO REVIEW 2\\nUSE: '+ok.join(', ')+'\\nNO: '+no.join(', '))
 .then(()=>alert('Copied. Paste it back to Claude.'));}}
</script></body></html>'''
open('../output/Carpenta_Photo_Review_2.html','w').write(HTML)
print('written', len(HTML)//1024,'KB')
