from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# DB connection
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

# Initialize DB
def init_db():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS roles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# Dashboard
@app.route('/')
def index():
    conn = get_db_connection()
    roles = conn.execute('SELECT * FROM roles').fetchall()
    conn.close()
    return render_template('index.html', roles=roles)

# Create Role
@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']

        conn = get_db_connection()
        conn.execute('INSERT INTO roles (name, description) VALUES (?, ?)',
                     (name, description))
        conn.commit()
        conn.close()

        return redirect('/')

    return render_template('create_role.html')

# Update Role
@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    conn = get_db_connection()
    role = conn.execute('SELECT * FROM roles WHERE id = ?', (id,)).fetchone()

    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']

        conn.execute('UPDATE roles SET name=?, description=? WHERE id=?',
                     (name, description, id))
        conn.commit()
        conn.close()

        return redirect('/')

    conn.close()
    return render_template('update_role.html', role=role)

# Delete Role
@app.route('/delete/<int:id>')
def delete(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM roles WHERE id = ?', (id,))
    conn.commit()
    conn.close()

    return redirect('/')

import os

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)