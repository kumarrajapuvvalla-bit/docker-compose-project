"""
A minimal Flask application that stores and retrieves messages from a
PostgreSQL database.  This project demonstrates how to use
Docker Compose to orchestrate a multi‑container environment with a web
application and database.
"""

import os
import psycopg2
from flask import Flask, request, jsonify

app = Flask(__name__)


def get_db_connection():
    conn = psycopg2.connect(
        host=os.environ.get("POSTGRES_HOST", "db"),
        database=os.environ.get("POSTGRES_DB", "messages"),
        user=os.environ.get("POSTGRES_USER", "user"),
        password=os.environ.get("POSTGRES_PASSWORD", "pass"),
    )
    return conn


@app.route("/messages", methods=["POST"])
def add_message():
    data = request.get_json(force=True)
    text = data.get("text")
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO messages (body) VALUES (%s) RETURNING id;", (text,))
    message_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"id": message_id, "text": text})


@app.route("/messages", methods=["GET"])
def list_messages():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, body FROM messages;")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify([{"id": row[0], "text": row[1]} for row in rows])


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "OK"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
