import os
import sqlite3
import sys
from flask import Flask, render_template, request, jsonify, send_from_directory

# Obtener la ruta del pendrive automáticamente
BASE_DIR = os.path.dirname(os.path.abspath(sys.argv[0]))
DB_PATH = os.path.join(BASE_DIR, "database.db")

app = Flask(__name__, static_folder="static", template_folder="templates")

# Crear la base de datos si no existe
def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                          id INTEGER PRIMARY KEY AUTOINCREMENT,
                          name TEXT NOT NULL)''')
        conn.commit()

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory(os.path.join(BASE_DIR, 'static'), filename)

@app.route('/add_user', methods=['POST'])
def add_user():
    data = request.json
    name = data.get("name")
    
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (name) VALUES (?)", (name,))
        conn.commit()
    
    return jsonify({"message": "Usuario agregado correctamente"})

@app.route('/get_users', methods=['GET'])
def get_users():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()
    
    return jsonify(users)

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=8000, debug=False)