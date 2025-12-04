from flask import Flask, render_template, request, redirect
import sqlite3
import os

app = Flask(__name__)

# Cesta k databáze
DB_PATH = os.path.join(os.path.dirname(__file__), "hokej.db")

# Funkcia na pripojenie k databáze
def get_db():
    if not os.path.exists(DB_PATH):
        # Ak databáza neexistuje, vytvoríme ju
        conn = sqlite3.connect(DB_PATH)
        conn.execute("""
        CREATE TABLE IF NOT EXISTS players (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            position TEXT,
            confirmed INTEGER
        )
        """)
        conn.commit()
        conn.close()
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/")
def index():
    conn = get_db()
    players = conn.execute("SELECT * FROM players ORDER BY position, name").fetchall()
    conn.close()
    return render_template("index.html", players=players)

@app.route("/add_player", methods=["POST"])
def add_player():
    name = request.form["name"]
    position = request.form["position"]
    conn = get_db()
    conn.execute("INSERT INTO players (name, position, confirmed) VALUES (?, ?, 0)", (name, position))
    conn.commit()
    conn.close()
    return redirect("/")

@app.route("/confirm", methods=["POST"])
def confirm():
    player_id = request.form["id"]
    confirmed = request.form["confirmed"]
    conn = get_db()
    conn.execute("UPDATE players SET confirmed=? WHERE id=?", (confirmed, player_id))
    conn.commit()
    conn.close()
    return "OK"

@app.route("/reset")
def reset():
    conn = get_db()
    conn.execute("UPDATE players SET confirmed=0")
    conn.commit()
    conn.close()
    return redirect("/")

# Spustenie Flask aplikácie (lokálne alebo Render)
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Render nastaví PORT
    app.run(host="0.0.0.0", port=port)
