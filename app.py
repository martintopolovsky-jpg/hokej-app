from flask import Flask, render_template, request, redirect
import sqlite3
import os

app = Flask(__name__)

# Cesta k databáze
DB_PATH = os.path.join(os.path.dirname(__file__), "hokej.db")

# Funkcia na pripojenie k databáze a jej vytvorenie, ak neexistuje
def get_db():
    db_exists = os.path.exists(DB_PATH)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    if not db_exists:
        conn.execute("""
        CREATE TABLE IF NOT EXISTS players (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            position TEXT,
            confirmed INTEGER
        )
        """)
        conn.commit()
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

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
    @app.route("/switch_position", methods=["POST"])
def switch_position():
    player_id = request.form["id"]
    conn = get_db()
    player = conn.execute("SELECT position FROM players WHERE id=?", (player_id,)).fetchone()
    if player:
        new_position = "utocnik" if player["position"] == "obranca" else "obranca"
        conn.execute("UPDATE players SET position=? WHERE id=?", (new_position, player_id))
        conn.commit()
    conn.close()
    return redirect("/")
    conn.execute("ALTER TABLE players ADD COLUMN in_lineup INTEGER DEFAULT 0")
def get_db():
    db_exists = os.path.exists(DB_PATH)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    if not db_exists:
        conn.execute("""
        CREATE TABLE IF NOT EXISTS players (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            position TEXT,
            confirmed INTEGER,
            in_lineup INTEGER DEFAULT 0
        )
        """)
        conn.commit()
    return conn


