# Carpenta catalogue — source

`products_final.json` is the single source of truth (644 products). Everything
else is generated from it. Keep this folder — the cloud container is wiped
between sessions and in Oct 2026 a whole session's work was lost because only
the HTML outputs had been saved here.

## Rebuild
    python3 recover.py            # only if products_final.json is lost
    python3 apply_review2.py      # re-applies the approved photo matches
    python3 build_catalogue2.py   # -> ../output/Carpenta_Catalogue.html
    python3 build_trade.py        # -> Carpenta_Trade_Price_List.html
    python3 build_shootlist.py    # -> Carpenta_Photo_Shoot_List.html
    python3 build_xlsx.py         # -> Carpenta_Products.xlsx

Edit prices and names in the xlsx, then run `recover.py` to pull them back in.

## The roll artwork
`rm_b.png` is a real edge-band roll photographed on white, background removed and
reduced to a grey shading layer. It is used twice per band: as a CSS mask on the
decor, and again as a multiply overlay. Because its face is near white, multiply
keeps the decor's colour and only paints the coil's shadows. One photo makes all
40 bands photoreal.

## Crop boxes are FRACTIONS, not pixels
The CDN serves resized variants at the same aspect ratio, so pixel crops break and
fractional ones survive. Stored as `crop: [fx, fy, fw, fh]`; the original declared
size is kept in `dims` for reference only. The fill is computed in the browser,
since natural size is not known until the image loads.

## Design
Dark and premium on screen, 3 x 4 = 12 products per A4 page in print. The print
stylesheet switches the page to light paper so it does not drink toner — same
typography, same brass accent.
