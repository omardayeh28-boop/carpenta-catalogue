# Carpenta Product Catalogue

Generates Carpenta's printable product catalogue, trade price list, photo shoot list and
master product spreadsheet from the 644 published products on [carpenta.store](https://carpenta.store).

## Layout
| Folder | What's in it |
|---|---|
| `src/` | Build scripts + `products_final.json` (the single source of truth) |
| `photos/` | Carpenta's own product photos and edge-band textures |
| `assets/` | Logo |
| `output/` | Generated files: `Carpenta_Catalogue.html`, `Carpenta_Trade_Price_List.html`, `Carpenta_Photo_Shoot_List.html`, `Carpenta_Products.xlsx` |

## Rebuild
Run from inside `src/` (Python 3 + `pip install -r requirements.txt`):

    cd src
    python3 recover.py            # only if products_final.json is lost — rebuilds it from output/ xlsx + catalogue
    python3 apply_review2.py      # re-applies the approved photo matches
    python3 build_catalogue2.py   # -> output/Carpenta_Catalogue.html
    python3 build_trade.py        # -> output/Carpenta_Trade_Price_List.html
    python3 build_shootlist.py    # -> output/Carpenta_Photo_Shoot_List.html
    python3 build_xlsx.py         # -> output/Carpenta_Products.xlsx  (overwrites edits — run recover.py first)

**Edit prices and names in `output/Carpenta_Products.xlsx`, not the HTML**, then run
`recover.py` to pull them back into the JSON before rebuilding.

## Where the data comes from
carpenta.store runs on Ecwid (store ID `96067158`). Products are fetched from the storefront
catalog API by walking every category *and* subcategory and merging by product ID — the root
category only returns 300 of the 644 products. Product photos are hotlinked to the Ecwid CDN,
so the catalogue needs an internet connection to show them; print to PDF from a browser.

See [`src/NOTES.md`](src/NOTES.md) for the edge-band roll artwork, crop boxes and design notes.

## Working together
- **Automatic rebuild:** every push to `main` that touches `src/`, `photos/` or `assets/`
  runs `.github/workflows/rebuild.yml`, which regenerates the catalogue, trade list and shoot
  list and commits them to `output/`. You can also run it by hand from the **Actions** tab.
  It does **not** regenerate `Carpenta_Products.xlsx`, because that file holds hand edits.
- **Pull before you start, push when you're done.** Collaborators work on a branch and open a
  pull request into `main`, so changes get reviewed before they reach the live catalogue.
