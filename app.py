from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)
DB = "chronova.db"

def get_db():
    conn = sqlite3.connect(DB)
    conn.execute("""CREATE TABLE IF NOT EXISTS watches
                     (id INTEGER PRIMARY KEY AUTOINCREMENT,
                      name TEXT NOT NULL,
                      brand TEXT NOT NULL,
                      price REAL NOT NULL)""")
    conn.execute("""CREATE TABLE IF NOT EXISTS orders
                     (id INTEGER PRIMARY KEY AUTOINCREMENT,
                      watch_id INTEGER NOT NULL,
                      customer_name TEXT NOT NULL)""")
    if conn.execute("SELECT COUNT(*) FROM watches").fetchone()[0] == 0:
        conn.executemany(
            "INSERT INTO watches (name, brand, price) VALUES (?, ?, ?)",
            [
                ("Aurora Classic", "Chronova", 129.99),
                ("Midnight Chrono", "Chronova", 249.50),
                ("Aviator Steel", "Chronova", 189.00),
            ],
        )
        conn.commit()
    return conn

@app.route("/")
def home():
    return jsonify({"status": "ok", "message": "Chronova — Premium Watch Store API running"})

@app.route("/health")
def health():
    return jsonify({"status": "healthy"}), 200

@app.route("/watches", methods=["GET"])
def list_watches():
    conn = get_db()
    rows = conn.execute("SELECT id, name, brand, price FROM watches").fetchall()
    conn.close()
    return jsonify([{"id": r[0], "name": r[1], "brand": r[2], "price": r[3]} for r in rows])

@app.route("/watches/<int:watch_id>", methods=["GET"])
def get_watch(watch_id):
    conn = get_db()
    row = conn.execute("SELECT id, name, brand, price FROM watches WHERE id=?", (watch_id,)).fetchone()
    conn.close()
    if not row:
        return jsonify({"error": "Watch not found"}), 404
    return jsonify({"id": row[0], "name": row[1], "brand": row[2], "price": row[3]})

@app.route("/watches", methods=["POST"])
def add_watch():
    data = request.get_json()
    conn = get_db()
    conn.execute("INSERT INTO watches (name, brand, price) VALUES (?, ?, ?)",
                 (data["name"], data["brand"], data["price"]))
    conn.commit()
    conn.close()
    return jsonify({"message": "Watch added"}), 201

@app.route("/orders", methods=["POST"])
def place_order():
    data = request.get_json()
    conn = get_db()
    watch = conn.execute("SELECT id FROM watches WHERE id=?", (data["watch_id"],)).fetchone()
    if not watch:
        conn.close()
        return jsonify({"error": "Watch not found"}), 404
    conn.execute("INSERT INTO orders (watch_id, customer_name) VALUES (?, ?)",
                 (data["watch_id"], data["customer_name"]))
    conn.commit()
    conn.close()
    return jsonify({"message": "Order placed"}), 201

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
