import os
import ssl
from pathlib import Path

import psycopg2
from flask import Flask, Response, jsonify, request
from flask_cors import CORS
from psycopg2 import sql

app = Flask(__name__, static_folder=".")
CORS(app)


def get_connection():
    return psycopg2.connect(
        dbname=os.getenv("DB_NAME", "train1234"),
        user=os.getenv("DB_USER", "train1234"),
        password=os.getenv("DB_PASSWORD", "train1234"),
        host=os.getenv("DB_HOST", "localhost"),
        port=os.getenv("DB_PORT", "5432"),
    )


def _validate_employee_payload(payload):
    if not isinstance(payload, dict):
        return None, "Request body must be a JSON object"

    name = payload.get("name")
    role = payload.get("role") or payload.get("department")
    salary = payload.get("salary")

    if not name or not isinstance(name, str):
        return None, "Field 'name' is required and must be text"
    if not role or not isinstance(role, str):
        return None, "Field 'role' is required (or use 'department') and must be text"
    if salary is None:
        return None, "Field 'salary' is required"

    try:
        salary_value = float(salary)
    except (TypeError, ValueError):
        return None, "Field 'salary' must be numeric"

    return {"name": name.strip(), "role": role.strip(), "salary": salary_value}, None


@app.route("/employees", methods=["GET"])
def get_employees():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT id, name, role, salary FROM employees ORDER BY id;")
            rows = cur.fetchall()

    return jsonify(rows)


@app.route("/employees", methods=["POST"])
def add_employee():
    payload, error = _validate_employee_payload(request.get_json(silent=True))
    if error:
        return jsonify({"status": "error", "message": error}), 400

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO employees (name, role, salary) VALUES (%s, %s, %s)",
                (payload["name"], payload["role"], payload["salary"]),
            )

    return jsonify({"status": "success"}), 201


@app.route("/database", methods=["GET"])
def get_database():
    db_dump = {}

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT tablename FROM pg_tables WHERE schemaname='public' ORDER BY tablename;")
            tables = [name for (name,) in cur.fetchall()]

            for table in tables:
                cur.execute(sql.SQL("SELECT * FROM {};").format(sql.Identifier(table)))
                rows = cur.fetchall()
                colnames = [desc[0] for desc in cur.description]
                db_dump[table] = {"columns": colnames, "rows": rows}

    return jsonify(db_dump)


@app.route("/health", methods=["GET"])
def health():
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT 1;")
                cur.fetchone()
        return jsonify({"status": "ok", "database": "connected"}), 200
    except psycopg2.Error:
        return jsonify({"status": "error", "database": "unreachable"}), 503


@app.route("/", methods=["GET"])
def home():
    content = Path("test.html").read_text(encoding="utf-8")
    return Response(content, status=200, mimetype="text/html")


if __name__ == "__main__":
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain("cert.pem", "key.pem")
    context.set_alpn_protocols([])
    app.run(debug=False, host="::", port=5000, ssl_context=context)
