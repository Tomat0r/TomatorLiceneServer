from flask import Flask, request, jsonify
from datetime import datetime
import sqlite3
import requests
import os
import random
import string

app = Flask(__name__)

# Admin password
# Admin password aus Umgebungsvariable ziehen, kein Fallback verwendet
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")
if not ADMIN_PASSWORD:
    raise ValueError("Die Umgebungsvariable ADMIN_PASSWORD ist nicht gesetzt.")

# Datenbankpfad direkt im Arbeitsverzeichnis von /app
DATABASE_PATH = os.path.join(os.getcwd(), "licenses.db")


# Datenbank initialisieren
def init_db():
    print(f"Initializing database at: {DATABASE_PATH}")
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS licenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            key TEXT UNIQUE NOT NULL,
            uuid TEXT DEFAULT NULL,
            creation_date TEXT NOT NULL
        );
        """
    )
    conn.commit()
    conn.close()


def generate_key():
    """Generate a license key in xxxxx-xxxxx-xxxxx-xxxxx format."""
    return "-".join(
        [
            "".join(random.choices(string.ascii_uppercase + string.digits, k=5)),
            "".join(random.choices(string.ascii_uppercase + string.digits, k=5)),
            "".join(random.choices(string.ascii_uppercase + string.digits, k=5)),
            "".join(random.choices(string.ascii_uppercase + string.digits, k=5)),
        ]
    )


@app.route("/generate", methods=["POST"])
def generate_license():
    """Generate a license key (requires admin password)."""
    data = request.json
    if not data or "password" not in data:
        return jsonify({"error": "Admin password required"}), 401

    if data["password"] != ADMIN_PASSWORD:
        return jsonify({"error": "Invalid admin password"}), 403

    key = generate_key()
    creation_date = datetime.utcnow().isoformat()

    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO licenses (key, creation_date) VALUES (?, ?)", (key, creation_date)
    )
    conn.commit()
    conn.close()

    return jsonify({"success": True, "key": key})


@app.route("/list", methods=["GET"])
def list_licenses():
    """List all licenses (requires admin password)."""
    password = request.args.get("password")
    if not password or password != ADMIN_PASSWORD:
        return jsonify({"error": "Invalid or missing admin password"}), 403

    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM licenses")
    licenses = cursor.fetchall()
    conn.close()

    result = [
        {"key": row[1], "uuid": row[2], "creation_date": row[3]} for row in licenses
    ]
    return jsonify(result)


@app.route("/delete", methods=["DELETE"])
def delete_license():
    """Delete a license by key (requires admin password)."""
    data = request.json
    if not data or "password" not in data or "key" not in data:
        return jsonify({"error": "Password and license key required"}), 400

    if data["password"] != ADMIN_PASSWORD:
        return jsonify({"error": "Invalid admin password"}), 403

    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM licenses WHERE key = ?", (data["key"],))
    conn.commit()
    deleted = cursor.rowcount
    conn.close()

    if deleted == 0:
        return jsonify({"error": "License key not found"}), 404

    return jsonify({"success": True})


if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000)
