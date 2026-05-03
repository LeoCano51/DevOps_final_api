from flask import Flask, jsonify
import pymysql

app = Flask(__name__)

# -----------------------------
# CONFIG RDS
# -----------------------------
DB_CONFIG = {
    "host": "devopsdbinstance.chg6o2suqnpf.us-east-2.rds.amazonaws.com",
    "user": "admin",
    "password": "superdupercontraseniaBD",
    "database": "etl_db",
    "cursorclass": pymysql.cursors.DictCursor
}

# -----------------------------
# CONEXIÓN
# -----------------------------
def get_connection():
    return pymysql.connect(**DB_CONFIG)

# -----------------------------
# ENDPOINT 1: TODOS LOS PROYECTOS
# -----------------------------
@app.route("/projects", methods=["GET"])
def get_projects():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM projects_clean LIMIT 100")
    data = cursor.fetchall()

    conn.close()
    return jsonify(data)

# -----------------------------
# ENDPOINT 2: PROYECTOS CON ALTO RETRASO
# -----------------------------
@app.route("/projects/high-delay", methods=["GET"])
def high_delay_projects():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM projects_clean
        WHERE high_delay_flag = TRUE
        LIMIT 100
    """)
    data = cursor.fetchall()

    conn.close()
    return jsonify(data)

# -----------------------------
# ENDPOINT 3: MÉTRICAS GENERALES
# -----------------------------
@app.route("/metrics", methods=["GET"])
def metrics():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            COUNT(*) AS total_projects,
            AVG(final_margin) AS avg_margin,
            AVG(delay_ratio) AS avg_delay,
            AVG(risk_mitigation_rate) AS avg_risk_mitigation
        FROM projects_clean
    """)

    data = cursor.fetchone()

    conn.close()
    return jsonify(data)

# -----------------------------
# ENDPOINT 4: PROYECTOS CON BAJO MARGEN
# -----------------------------
@app.route("/projects/low-margin", methods=["GET"])
def low_margin_projects():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM projects_clean
        WHERE low_margin_flag = TRUE
        LIMIT 100
    """)

    data = cursor.fetchall()

    conn.close()
    return jsonify(data)

# -----------------------------
# HEALTH CHECK
# -----------------------------
@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "API funcionando correctamente 🚀"})

# -----------------------------
# RUN
# -----------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)