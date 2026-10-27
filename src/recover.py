import re, json, openpyxl

h = open('../output/Carpenta_Catalogue.html').read()
pairs = re.findall(r'<svg viewBox="([^"]+)"[^>]*>\s*<image[^>]*href="([^"]+)"', h)
CROPS = {}
for v, u in pairs:
    key = u.split('/')[-1].split('.')[0]
    x, y, w, hh = [float(t) for t in v.split()]
    if key not in CROPS or w * hh > CROPS[key][2] * CROPS[key][3]:
        CROPS[key] = (x, y, w, hh)

wb = openpyxl.load_workbook('../output/Carpenta_Products.xlsx')
rows = list(wb['Products'].values)
hdr = rows[0]
prods = []
for r in rows[1:]:
    d = dict(zip(hdr, r))
    img = d['Photo link'] or ''
    key = img.split('/')[-1].split('.')[0] if img else ''
    prods.append({
        'show': d['Show'], 'cat': d['Category'], 'sub': d['Group'] or '',
        'name': d['Product name'], 'sku': str(d['SKU']).strip(),
        'price': d['Price (GHS)'], 'img': img,
        'itype': d['Image type'], 'note': d['Note'] or '',
        'crop': CROPS.get(key),
    })
json.dump({'crops': CROPS, 'products': prods}, open('products_final.json', 'w'), indent=0)
print('products', len(prods), 'crops', len(CROPS))
print('with crop', sum(1 for p in prods if p['crop']))
