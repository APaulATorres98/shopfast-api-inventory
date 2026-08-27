from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('inventory.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            stock INTEGER NOT NULL,
            price REAL NOT NULL
        )
    ''')
    cursor.execute("INSERT OR IGNORE INTO products (id, name, stock, price) VALUES (1, 'Laptop Gamer', 15, 1200.00)")
    cursor.execute("INSERT OR IGNORE INTO products (id, name, stock, price) VALUES (2, 'Mouse Inalámbrico', 50, 25.50)")
    conn.commit()
    conn.close()

@app.route('/')
def home():
    return jsonify({"message": "ShopFast Retail Inventory API v1.0"})

@app.route('/api/products/search', methods=['GET'])
def search_product():
    query = request.args.get('q', '')
    conn = sqlite3.connect('inventory.db')
    cursor = conn.cursor()
    
    sql = "SELECT id, name, stock, price FROM products WHERE name LIKE '%" + query + "%'"
    
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        products = [{"id": r[0], "name": r[1], "stock": r[2], "price": r[3]} for r in results]
        return jsonify(products)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()

if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5000)
