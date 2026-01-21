from flask import Flask, request, jsonify
import json
import random
from datetime import datetime
import os
import oracledb

app = Flask(__name__)

def get_connection():
    dsn = os.getenv("DB_DSN", "PARDB")
    return oracledb.connect(dsn=dsn)

historia = []

with open("cwiczenia.json", "r", encoding="utf-8") as f:
    cwiczenia = json.load(f)

@app.route("/health")
def health():
    return "ok"

@app.route("/api/trening")
def trening():
    trudnosc = request.args.get("trudnosc", "latwy")
    if trudnosc not in cwiczenia:
        return jsonify({"error": "Nieznana trudnosc"})
    
    wybrane = random.choice(cwiczenia[trudnosc])
    trening_item = {
        "trudnosc": trudnosc,
        "cwiczenie": wybrane,
        "created_at": datetime.now().isoformat()
    }

    historia.append(trening_item)

    return jsonify ({
        "trening": trening_item,
        "historia": historia[-3:]
    })

@app.route("/api/historia")
def get_historia():
    return jsonify(historia[-3:])

@app.route("/test")
def test_db():
    try:
        conn = get_connection()
        cur = conn.cursor()
        
        # Pobranie wszystkich tabel, do których masz dostęp
        cur.execute("SELECT owner, table_name FROM all_tables")
        tables = [{"owner": row[0], "table": row[1]} for row in cur.fetchall()]

        # Zamknięcie połączenia
        cur.close()
        conn.close()

        return jsonify({"tables": tables})

    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)