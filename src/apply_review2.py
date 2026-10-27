import json, base64
D=json.load(open('products_final.json'))
COL=json.load(open('roll_colours.json')); COL['12c126ff']='#bfbcb9'

# local photo per SKU (approved in Review 2)
PHOTO={'AKD3518':'AKD3518.jpg','AKD3550':'AKD3550.jpg','SK3535':'SK3535.jpg',
 'HBF113B50B':'HBF113B50B.jpg','H300':'H300.jpg','BH001':'BH001.jpg',
 'LPL10W':'LPL10W.jpg','LPL10G':'LPL10G.jpg','MKL001':'MKL001.jpg','ST00472':'ST00472.jpg'}
ALT={'SK3535':'SK3535_alt.jpg'}
# edge bands with no decor photo -> flat colour, or a tiling grain texture
BAND={'3736':(COL['bee6f100'],None),'3501':(COL['7dfcfb4f'],None),'3501ED':(COL['7dfcfb4f'],None),
 '3602':(COL['f3840773'],None),'738AGT':(COL['af223a45'],None),
 'TECE':(COL['a58e8c40'],'tex_a58e8c40.jpg'),'TECE40':(COL['c1913c9c'],'tex_c1913c9c.jpg')}

n=0
for p in D['products']:
    s=p['sku']
    if s in PHOTO:
        p['local']='photos/'+PHOTO[s]; p['alt']='photos/'+ALT[s] if s in ALT else None
        p['itype']='Photo (own)'; p['note']=''; n+=1
    if s in BAND:
        c,t=BAND[s]; p['band_colour']=c; p['band_tex']='photos/'+t if t else None
        p['itype']='Roll — colour from your roll photo'
    if p['sub']=='EDGE BANDS' and p.get('crop'):
        p['itype']='Roll — your decor photo'
D['applied_review2']=True
json.dump(D, open('products_final.json','w'), indent=0)
from collections import Counter
print('photos applied', n)
print(Counter(p['itype'] for p in D['products']))
