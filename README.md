# Tim Hortons 3D Menu (concept) - Flask + Three.js

## Run
    pip install -r requirements.txt
    python app.py          # http://127.0.0.1:5000

## What it does
- Flask + SQLite serve the menu: `/api/menu`, `/api/items`, `/api/items/<slug>`, `/api/categories`, `/api/ingredients`, `POST /api/orders`, `GET /api/orders/<id>?phone=...`.
- The database (`menu.db`) is created automatically from `data/menu.json` on first start. To change the menu, edit `data/build_menu.py`, run `python data/build_menu.py`, delete `menu.db`, restart.
- Optional admin: set `ADMIN_TOKEN` and `PATCH /api/admin/items/<slug>` with header `X-Admin-Token` and JSON `{"price":700,"available":true}`.
- The browser builds every item in real-time 3D (Three.js) from the `model` parameters and ingredient `kind`s that the API returns. Open an item to see its ingredients orbit, then fly in and build the item. Drag to rotate.

## Notes
- Unofficial concept, not affiliated with Tim Hortons. The official menu page is images only, so items and prices come from public delivery-app listings and may be incomplete or out of date. Ingredient lists are illustrative.
- `three.min.js` (r128) is bundled in `static/js` so it works offline.
