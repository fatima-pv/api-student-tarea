
from flask import Flask, request, jsonify
import os
import sqlite3

APP_PORT = int(os.getenv("APP_PORT", "3000"))
DB_PATH = os.getenv("DB_PATH", "/data/students.sqlite")

app = Flask(__name__)

def db_connection():
    conn = None
    try:
        # check_same_thread=False allows use across requests in Flask dev server;
        # gunicorn with workers handles concurrency better, but we'll keep it safe.
        conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    except sqlite3.Error as e:
        print(e)
    return conn

@app.route("/", methods=["GET"])
def health():
    return "OK", 200

@app.route("/students", methods=["GET", "POST"])
def students():
    conn = db_connection()
    cursor = conn.cursor()

    if request.method == "GET":
        cursor = conn.execute("SELECT id, firstname, lastname, gender, age FROM students")
        students = [
            dict(id=row[0], firstname=row[1], lastname=row[2], gender=row[3], age=row[4])
            for row in cursor.fetchall()
        ]
        return jsonify(students), 200

    if request.method == "POST":
        data = request.form if request.form else request.json or {}
        firstname = data.get("firstname")
        lastname = data.get("lastname")
        gender = data.get("gender")
        age = data.get("age")

        sql = """INSERT INTO students (firstname, lastname, gender, age)
                 VALUES (?, ?, ?, ?)"""
        cur = cursor.execute(sql, (firstname, lastname, gender, age))
        conn.commit()
        return jsonify({"id": cur.lastrowid, "message": "Student created"}), 201

@app.route("/student/<int:id>", methods=["GET", "PUT", "DELETE"])
def student(id):
    conn = db_connection()
    cursor = conn.cursor()

    if request.method == "GET":
        cursor.execute("SELECT id, firstname, lastname, gender, age FROM students WHERE id = ?", (id,))
        row = cursor.fetchone()
        if row:
            return jsonify(dict(id=row[0], firstname=row[1], lastname=row[2], gender=row[3], age=row[4])), 200
        else:
            return jsonify({"error": "Student not found"}), 404

    if request.method == "PUT":
        data = request.form if request.form else request.json or {}
        firstname = data.get("firstname")
        lastname = data.get("lastname")
        gender = data.get("gender")
        age = data.get("age")

        sql = """UPDATE students SET firstname = ?, lastname = ?, gender = ?, age = ?
                 WHERE id = ?"""
        cursor.execute(sql, (firstname, lastname, gender, age, id))
        conn.commit()
        return jsonify({"id": id, "firstname": firstname, "lastname": lastname, "gender": gender, "age": age}), 200

    if request.method == "DELETE":
        cursor.execute("DELETE FROM students WHERE id = ?", (id,))
        conn.commit()
        return jsonify({"message": f"Student {id} deleted"}), 200

if __name__ == "__main__":
    # bind to 0.0.0.0:3000 for ECS
    app.run(host="0.0.0.0", port=APP_PORT, debug=False)
