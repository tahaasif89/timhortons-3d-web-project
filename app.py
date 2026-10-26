"""Tim Hortons 3D Menu (concept) - Flask backend.
Run:  pip install -r requirements.txt && python app.py   ->  http://127.0.0.1:5000
The menu lives in SQLite (menu.db). It is created and seeded from data/menu.json on first start.
Edit data/menu.json (or use the admin PATCH endpoint) to change items, prices and ingredients."""
import json, os, random, sqlite3, string
from datetime import datetime, timezone
from flask import Flask, g, jsonify, render_template, request, abort

BASE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.join(BASE, 'menu.db')
ADMIN_TOKEN = os.environ.get('ADMIN_TOKEN', '')          # set to enable the admin endpoint
app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

def db():
    if 'db' not in g:
        g.db = sqlite3.connect(DB)
        g.db.row_factory = sqlite3.Row
        g.db.execute('PRAGMA foreign_keys=ON')
    return g.db

@app.teardown_appcontext
def close_db(_):
    d = g.pop('db', None)
    if d is not None:
        d.close()

def init_db(force=False):
    if force and os.path.exists(DB):
        os.remove(DB)
    con = sqlite3.connect(DB)
    con.executescript(open(os.path.join(BASE, 'schema.sql')).read())
    if con.execute('SELECT COUNT(*) FROM items').fetchone()[0] == 0:
        data = json.load(open(os.path.join(BASE, 'data', 'menu.json'), encoding='utf-8'))
        for i, c in enumerate(data['categories']):
            con.execute('INSERT INTO categories(slug,name,blurb,sort) VALUES(?,?,?,?)', (c['slug'], c['name'], c['blurb'], i))
        for g_ in data['ingredients']:
            con.execute('INSERT INTO ingredients(slug,name,kind,color,info) VALUES(?,?,?,?,?)', (g_['slug'], g_['name'], g_['kind'], g_['color'], g_['info']))
        for n, it in enumerate(data['items']):
            cid = con.execute('SELECT id FROM categories WHERE slug=?', (it['cat'],)).fetchone()[0]
            cur = con.execute('INSERT INTO items(slug,category_id,name,price,description,badge,builder,params,sort) VALUES(?,?,?,?,?,?,?,?,?)',
                              (it['slug'], cid, it['name'], it['price'], it['desc'], it.get('badge'), it['builder'], json.dumps(it['params']), n))
            for pos, ig in enumerate(it['ingredients']):
                iid = con.execute('SELECT id FROM ingredients WHERE slug=?', (ig['ing'],)).fetchone()[0]
                con.execute('INSERT INTO item_ingredients(item_id,ingredient_id,position,role) VALUES(?,?,?,?)', (cur.lastrowid, iid, pos, ig['role']))
    con.commit(); con.close()

def item_json(row, ings):
    return {'id': row['id'], 'slug': row['slug'], 'category': row['cat'], 'name': row['name'], 'price': row['price'],
            'priceText': ('Rs. {:,}'.format(row['price']) if row['price'] else 'See menu'), 'desc': row['description'],
            'badge': row['badge'], 'available': bool(row['available']),
            'model': {'builder': row['builder'], 'params': json.loads(row['params'])}, 'ingredients': ings}

def all_items(where='', args=()):
    rows = db().execute('SELECT i.*, c.slug AS cat FROM items i JOIN categories c ON c.id=i.category_id ' + where + ' ORDER BY i.sort', args).fetchall()
    out = []
    for r in rows:
        ings = [dict(x) for x in db().execute('SELECT g.slug,g.name,g.kind,g.color,g.info,ii.role,ii.position FROM item_ingredients ii JOIN ingredients g ON g.id=ii.ingredient_id WHERE ii.item_id=? ORDER BY ii.position', (r['id'],))]
        out.append(item_json(r, ings))
    return out

@app.route('/')
def index():
    return render_template('index.html')

@app.get('/api/categories')
def categories():
    return jsonify([dict(r) for r in db().execute('SELECT slug,name,blurb FROM categories ORDER BY sort')])

@app.get('/api/ingredients')
def ingredients():
    return jsonify([dict(r) for r in db().execute('SELECT slug,name,kind,color,info FROM ingredients ORDER BY name')])

@app.get('/api/items')
def items():
    cat = request.args.get('category')
    return jsonify(all_items('WHERE c.slug=?', (cat,)) if cat else all_items())

@app.get('/api/items/<slug>')
def item(slug):
    r = all_items('WHERE i.slug=?', (slug,))
    if not r:
        abort(404)
    return jsonify(r[0])

@app.get('/api/menu')
def menu():
    return jsonify({'categories': json.loads(categories().get_data()), 'ingredients': json.loads(ingredients().get_data()), 'items': all_items()})

@app.post('/api/orders')
def create_order():
    d = request.get_json(silent=True) or {}
    name, phone, address = (d.get('name') or '').strip(), (d.get('phone') or '').strip(), (d.get('address') or '').strip()
    lines = d.get('items') or []
    if not name or len(''.join(ch for ch in phone if ch.isdigit())) < 7 or not address or not lines:
        return jsonify({'error': 'Name, a valid phone, address and at least one item are required.'}), 400
    total, rows = 0, []
    for ln in lines:
        r = db().execute('SELECT slug,name,price,available FROM items WHERE slug=?', (ln.get('slug'),)).fetchone()
        qty = max(1, min(20, int(ln.get('qty') or 1)))
        if not r or not r['available']:
            return jsonify({'error': 'Unknown or unavailable item: %s' % ln.get('slug')}), 400
        total += (r['price'] or 0) * qty
        rows.append((r['slug'], r['name'], qty, r['price']))
    oid = 'TH-' + ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    db().execute('INSERT INTO orders(id,created,name,phone,address,notes,total) VALUES(?,?,?,?,?,?,?)', (oid, datetime.now(timezone.utc).isoformat(), name, phone, address, d.get('notes', ''), total))
    for r in rows:
        db().execute('INSERT INTO order_items(order_id,item_slug,name,qty,price) VALUES(?,?,?,?,?)', (oid, *r))
    db().commit()
    return jsonify({'id': oid, 'total': total, 'status': 'received'}), 201

@app.get('/api/orders/<oid>')
def get_order(oid):
    o = db().execute('SELECT * FROM orders WHERE id=? AND phone=?', (oid.upper(), request.args.get('phone', ''))).fetchone()
    if not o:
        abort(404)
    its = [dict(x) for x in db().execute('SELECT item_slug,name,qty,price FROM order_items WHERE order_id=?', (oid.upper(),))]
    return jsonify({'id': o['id'], 'created': o['created'], 'total': o['total'], 'status': o['status'], 'items': its})

@app.patch('/api/admin/items/<slug>')
def admin_patch(slug):
    if not ADMIN_TOKEN or request.headers.get('X-Admin-Token') != ADMIN_TOKEN:
        abort(403)
    d = request.get_json(silent=True) or {}
    if 'price' in d:
        db().execute('UPDATE items SET price=? WHERE slug=?', (d['price'], slug))
    if 'available' in d:
        db().execute('UPDATE items SET available=? WHERE slug=?', (1 if d['available'] else 0, slug))
    db().commit()
    return item(slug)

init_db()
if __name__ == '__main__':
    app.run(debug=True)
