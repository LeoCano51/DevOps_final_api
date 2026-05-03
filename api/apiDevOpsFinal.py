from flask import Flask, jsonify
from flask_cors import CORS
import pymysql

# -----------------------------
# APP + CORS
# -----------------------------
app = Flask(__name__)

# CORS totalmente abierto (para desarrollo)
CORS(app, resources={r"/*": {"origins": "*"}})

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
# HEALTH CHECK
# -----------------------------
@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "API funcionando correctamente 🚀"})

# -----------------------------
# TEST DB
# -----------------------------
@app.route("/test-db", methods=["GET"])
def test_db():
    try:
        conn = get_connection()
        conn.close()
        return jsonify({"message": "Conexión a RDS exitosa"})
    except Exception as e:
        return jsonify({"error": str(e)})

# -----------------------------
# TODOS LOS PROYECTOS
# -----------------------------
@app.route("/projects", methods=["GET"])
def get_projects():
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM projects_clean LIMIT 100")
        data = cursor.fetchall()

        conn.close()
        return jsonify(data)

    except Exception as e:
        return jsonify({"error": str(e)})

# -----------------------------
# HIGH DELAY
# -----------------------------
@app.route("/projects/high-delay", methods=["GET"])
def high_delay_projects():
    try:
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

    except Exception as e:
        return jsonify({"error": str(e)})

# -----------------------------
# LOW MARGIN
# -----------------------------
@app.route("/projects/low-margin", methods=["GET"])
def low_margin_projects():
    try:
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

    except Exception as e:
        return jsonify({"error": str(e)})

# -----------------------------
# METRICS
# -----------------------------
@app.route("/metrics", methods=["GET"])
def metrics():
    try:
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

    except Exception as e:
        return jsonify({"error": str(e)})

# -----------------------------
# RUN LOCAL (opcional)
# -----------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)