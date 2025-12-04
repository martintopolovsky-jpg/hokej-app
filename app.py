from flask import Flask, render_template, request, redirect
import sqlite3
import os

app = Flask(__name__)

DB_PATH = os.path.join(os.path.dirname(__file__), "hokej.db")

def get_db():
    # vytvorenie DB ak neexistuje
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("""
    CREATE TABLE IF NOT EXISTS players (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        position TEXT,
        confirmed INTEGER DEFAULT 0,
        in_lineup INTEGER DEFAULT 0
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

@app.route("/toggle_lineup", methods=["POST"])
def toggle_lineup():
    player_id = request.form["id"]
    conn = get_db()
    player = conn.execute("SELECT in_lineup, position FROM players WHERE id=?", (player_id,)).fetchone()
    if player:
        if player["in_lineup"] == 0:
            # kontrola limitov
            if player["position"] == "obranca":
                count = conn.execute("SELECT COUNT(*) FROM players WHERE position='obranca' AND in_lineup=1").fetchone()[0]
                if count >= 8:
                    conn.close()
                    return "limit obrancov", 400
            else:
                count = conn.execute("SELECT COUNT(*) FROM players WHERE position='utocnik' AND in_lineup=1").fetchone()[0]
                if count >= 12:
                    conn.close()
                    return "limit utocnikov", 400
        new_value = 0 if player["in_lineup"] else 1
        conn.execute("UPDATE players SET in_lineup=? WHERE id=?", (new_value, player_id))
        conn.commit()
    conn.close()
    return "OK"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
