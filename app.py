from flask import Flask, request, redirect, render_template_string
import sqlite3

app = Flask(__name__)

# =========================
# DATABASE SETUP
# =========================

def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL
        )
    ''')

    conn.commit()
    conn.close()

init_db()

# =========================
# HTML (GUI)
# =========================

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>DevOps Flask App</title>
    <style>
        body {
            font-family: Arial;
            background-color: #f2f2f2;
        }
        .container {
            width: 60%;
            margin: auto;
            margin-top: 40px;
            background: white;
            padding: 20px;
            border-radius: 10px;
        }
        h2 {
            text-align: center;
        }
        input {
            width: 100%;
            padding: 10px;
            margin-top: 10px;
        }
        button {
            margin-top: 10px;
            padding: 10px;
            width: 100%;
            background: blue;
            color: white;
            border: none;
        }
        table {
            width: 100%;
            margin-top: 20px;
            border-collapse: collapse;
        }
        th, td {
            border: 1px solid black;
            padding: 10px;
            text-align: center;
        }
        th {
            background-color: blue;
            color: white;
        }
    </style>
</head>

<body>

<div class="container">

<h2>DevOps CI/CD Flask App</h2>

<!-- FORM -->
<form action="/add" method="post">
    <input type="text" name="name" placeholder="Enter Name" required>
    <input type="email" name="email" placeholder="Enter Email" required>
    <button type="submit">Submit</button>
</form>

<!-- TABLE -->
<table>
<tr>
    <th>ID</th>
    <th>Name</th>
    <th>Email</th>
</tr>

{% for user in users %}
<tr>
    <td>{{ user[0] }}</td>
    <td>{{ user[1] }}</td>
    <td>{{ user[2] }}</td>
</tr>
{% endfor %}

</table>

</div>

</body>
</html>
"""

# =========================
# HOME ROUTE
# =========================

@app.route('/')
def home():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()

    conn.close()

    return render_template_string(HTML, users=users)

# =========================
# ADD USER (INPUT → DB)
# =========================

@app.route('/add', methods=['POST'])
def add_user():
    name = request.form['name']
    email = request.form['email']

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO users (name, email) VALUES (?, ?)",
        (name, email)
    )

    conn.commit()
    conn.close()

    return redirect('/')

# =========================
# RUN APP
# =========================

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
