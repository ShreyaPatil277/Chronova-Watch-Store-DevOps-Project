from flask import Flask, request, jsonify, render_template
import sqlite3

app = Flask(__name__)
DB = "chronova.db"

def get_db():
    conn = sqlite3.connect(DB)
    conn.execute("""CREATE TABLE IF NOT EXISTS watches
                     (id INTEGER PRIMARY KEY AUTOINCREMENT,
                      name TEXT NOT NULL,
                      brand TEXT NOT NULL,
                      price REAL NOT NULL,
                      image TEXT NOT NULL)""")
    conn.execute("""CREATE TABLE IF NOT EXISTS orders
                     (id INTEGER PRIMARY KEY AUTOINCREMENT,
                      watch_id INTEGER NOT NULL,
                      customer_name TEXT NOT NULL)""")
    if conn.execute("SELECT COUNT(*) FROM watches").fetchone()[0] == 0:
        conn.executemany(
            "INSERT INTO watches (name, brand, price, image) VALUES (?, ?, ?, ?)",
            [
                ("Neo Analog", "Titan", 2495.0, "https://images.unsplash.com/photo-1524805444758-089113d48a6d?w=400"),
                ("Edge Slim", "Titan", 8995.0, "https://images.unsplash.com/photo-1523170335258-f5ed11844a49?w=400"),
                ("Sport Chrono", "Fastrack", 1795.0, "https://images.unsplash.com/photo-1547996160-81dfa63595aa?w=400"),
                ("Reflex Beat", "Fastrack", 1995.0, "https://images.unsplash.com/photo-1533139502658-0198f920d8e8?w=400"),
            ],
        )
        conn.commit()
    return conn

@app.route("/")
def home():
    conn = get_db()
    rows = conn.execute("SELECT id, name, brand, price, image FROM watches").fetchall()
    conn.close()
    watches = [{"id": r[0], "name": r[1], "brand": r[2], "price": r[3], "image": r[4]} for r in rows]
    return render_template("index.html", watches=watches)

@app.route("/cart")
def cart():
    return render_template("cart.html")

@app.route("/health")
def health():
    return jsonify({"status": "healthy"}), 200

@app.route("/watches", methods=["GET"])
def list_watches():
    conn = get_db()
    rows = conn.execute("SELECT id, name, brand, price, image FROM watches").fetchall()
    conn.close()
    return jsonify([{"id": r[0], "name": r[1], "brand": r[2], "price": r[3], "image": r[4]} for r in rows])

@app.route("/watches", methods=["POST"])
def add_watch():
    data = request.get_json()
    conn = get_db()
    conn.execute("INSERT INTO watches (name, brand, price, image) VALUES (?, ?, ?, ?)",
                 (data["name"], data["brand"], data["price"], data.get("image", "")))
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