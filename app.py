from flask import Flask, jsonify, request, Response
import psycopg2
from flask_cors import CORS
import ssl
import os

app = Flask(__name__, static_folder='.')
CORS(app)

def get_connection():
    conn = psycopg2.connect(
        dbname=os.getenv("DB_NAME", "train1234"),
        user=os.getenv("DB_USER", "train1234"),
        password=os.getenv("DB_PASSWORD", "train1234"),
        host=os.getenv("DB_HOST", "localhost"),
        port=os.getenv("DB_PORT", "5432")
    )
    return conn

@app.route("/employees", methods=["GET"])
def get_df():
    conn = get_connection()
    cur= conn.cursor()
    cur.execute("SELECT * FROM employees;")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(rows)

@app.route("/employees", methods=["POST"])
def add_employee():
    data= request.json
    name = data["name"]
    department =data["department"]
    salary = data["salary"]

    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO employees (name, department, salary) VALUES (%s, %s, %s)",
        (name, department, salary)
    )
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"status": "success"}), 201

@app.route("/database", methods=["GET"])
def get_database():
    conn = get_connection()   
    cur = conn.cursor()

    cur.execute("SELECT tablename FROM pg_tables WHERE schemaname='public';")
    tables = cur.fetchall()

    db_dump = {}
    for (table,) in tables:
        cur.execute(f"SELECT * FROM {table};")
        rows = cur.fetchall()
        colnames = [desc[0] for desc in cur.description]  # column names
        db_dump[table] = {
            "columns": colnames,
            "rows": rows
        }

    cur.close()
    conn.close()
    return jsonify(db_dump)

@app.route("/", methods=["GET"])
def home():
    with open('test.html', 'r') as f:
        content = f.read()
    return Response(content, status=200, mimetype='text/html')


if __name__ == "__main__":
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain('cert.pem', 'key.pem')
    # Ensure HTTP/1.1 is used
    context.set_alpn_protocols([])
    
    # Bind to both IPv4 and IPv6
    app.run(debug=False, host='::', port=5000, ssl_context=context)
