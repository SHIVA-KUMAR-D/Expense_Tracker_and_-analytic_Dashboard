# Smart Expense Tracker — Full Stack (Flask + SQLite)
# WITH Login + Registration (Fully Working)

from flask import Flask, request, jsonify, render_template_string, session, redirect
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)
DB = "expenses.db"

# ---------- DATABASE ----------

def init_db():
    conn = sqlite3.connect(DB)
    c = conn.cursor()

    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')

    c.execute('''
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            title TEXT NOT NULL,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            date TEXT NOT NULL
        )
    ''')

    conn.commit()
    conn.close()

init_db()

# ---------- LOGIN PAGE ----------

LOGIN_HTML = """
<body style="margin:0;font-family:Arial;background:#f1f5f9;display:flex;align-items:center;justify-content:center;height:100vh;">
<div style="background:white;padding:40px;border-radius:12px;width:350px;box-shadow:0 10px 30px rgba(0,0,0,0.1);">
<h2 style="text-align:center;">Login</h2>

<form method="POST" action="/login">
<input name="username" placeholder="Username" required style="width:100%;padding:12px;margin:10px 0;">
<input type="password" name="password" placeholder="Password" required style="width:100%;padding:12px;margin:10px 0;">
<button type="submit" style="width:100%;padding:12px;background:#2563eb;color:white;border:none;">Login</button>
</form>

<p style="text-align:center;margin-top:15px;">
New user? <a href="/register">Register</a>
</p>
</div>
</body>
"""

# ---------- REGISTER PAGE ----------

REGISTER_HTML = """
<body style="margin:0;font-family:Arial;background:#f1f5f9;display:flex;align-items:center;justify-content:center;height:100vh;">
<div style="background:white;padding:40px;border-radius:12px;width:350px;box-shadow:0 10px 30px rgba(0,0,0,0.1);">
<h2 style="text-align:center;">Register</h2>

<form method="POST" action="/register">
<input name="username" placeholder="Username" required style="width:100%;padding:12px;margin:10px 0;">
<input type="password" name="password" placeholder="Password" required style="width:100%;padding:12px;margin:10px 0;">
<button type="submit" style="width:100%;padding:12px;background:#16a34a;color:white;border:none;">Create Account</button>
</form>

<p style="text-align:center;margin-top:15px;">
Already have account? <a href="/login">Login</a>
</p>
</div>
</body>
"""

# ---------- AUTH ROUTES ----------

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = generate_password_hash(request.form['password'])

        conn = sqlite3.connect(DB)
        c = conn.cursor()
        try:
            c.execute("INSERT INTO users (username,password) VALUES (?,?)",(username,password))
            conn.commit()
        except:
            return "Username already exists"
        finally:
            conn.close()

        return redirect('/login')

    return REGISTER_HTML


@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = sqlite3.connect(DB)
        c = conn.cursor()
        c.execute("SELECT id,password FROM users WHERE username=?",(username,))
        user = c.fetchone()
        conn.close()

        if user and check_password_hash(user[1], password):
            session['user_id'] = user[0]
            return redirect('/')

        return "Invalid credentials"

    return LOGIN_HTML


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

# ---------- API ROUTES ----------

@app.route('/add', methods=['POST'])
def add_expense():
    if 'user_id' not in session:
        return jsonify({"error":"login required"}), 401

    data = request.json

    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute(
        "INSERT INTO expenses (user_id,title,amount,category,date) VALUES (?,?,?,?,?)",
        (session['user_id'], data['title'], data['amount'], data['category'], data['date'])
    )
    conn.commit()
    conn.close()

    return jsonify({"status": "success"})


@app.route('/expenses')
def get_expenses():
    if 'user_id' not in session:
        return jsonify([])

    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute(
        "SELECT id,title,amount,category,date FROM expenses WHERE user_id=? ORDER BY id DESC",
        (session['user_id'],)
    )
    rows = c.fetchall()
    conn.close()

    return jsonify(rows)


@app.route('/delete/<int:eid>', methods=['DELETE'])
def delete_expense(eid):
    if 'user_id' not in session:
        return jsonify({"error":"login required"}), 401

    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("DELETE FROM expenses WHERE id=? AND user_id=?", (eid, session['user_id']))
    conn.commit()
    conn.close()

    return jsonify({"status": "deleted"})

# ---------- DASHBOARD ----------

HTML = """
<!DOCTYPE html>
<html>
<head>
<meta charset='UTF-8'>
<title>FinSight — Smart Expense Dashboard</title>
<script src='https://cdn.jsdelivr.net/npm/chart.js'></script>
<style>
body {font-family: Arial; background:#0f172a; color:white; margin:0}
.container {max-width:1100px; margin:auto; padding:20px}
.card {background:#1e293b; padding:20px; border-radius:16px; margin-bottom:20px}
h1 {text-align:center}
input, select {padding:10px; margin:6px; border-radius:8px; border:none}
button {padding:10px 16px; border:none; border-radius:8px; background:#22c55e; color:white; cursor:pointer}
button:hover {background:#16a34a}
table {width:100%; border-collapse:collapse}
th, td {padding:10px; text-align:center}
th {background:#334155}
tr:nth-child(even){background:#1e293b}
.total {font-size:28px; font-weight:bold; text-align:center}
.delete {background:#ef4444}
.logout {display:block; text-align:right; margin-bottom:10px;}
</style>
</head>
<body>
<div class='container'>
<a href="/logout" class="logout">Logout</a>
<h1>💰 FinSight — Smart Expense Dashboard</h1>

<div class='card'>
<h3>Add Expense</h3>
<input id='title' placeholder='Title'>
<input id='amount' type='number' placeholder='Amount'>
<select id='category'>
<option>Food</option><option>Travel</option>
<option>Shopping</option><option>Bills</option>
<option>Other</option>
</select>
<input id='date' type='date'>
<button onclick='addExpense()'>Add</button>
</div>

<div class='card'>
<div class='total' id='total'>Total: ₹0</div>
<canvas id='chart'></canvas>
</div>

<div class='card'>
<h3>Expense List</h3>
<table>
<thead><tr><th>Title</th><th>Amount</th><th>Category</th><th>Date</th><th>Delete</th></tr></thead>
<tbody id='list'></tbody>
</table>
</div>
</div>

<script>
let chart;

async function loadExpenses(){
 const res = await fetch('/expenses');
 const data = await res.json();
 const list = document.getElementById('list');
 list.innerHTML='';
 let total=0;
 let cats={};

 data.forEach(e=>{
  total += e[2];
  cats[e[3]] = (cats[e[3]]||0)+e[2];

  list.innerHTML += `
  <tr>
   <td>${e[1]}</td>
   <td>₹${e[2]}</td>
   <td>${e[3]}</td>
   <td>${e[4]}</td>
   <td><button class='delete' onclick='del(${e[0]})'>X</button></td>
  </tr>`;
 });

 document.getElementById('total').innerText = `Total: ₹${total}`;
 drawChart(cats);
}

async function addExpense(){
 const data = {
  title: title.value,
  amount: parseFloat(amount.value),
  category: category.value,
  date: date.value || new Date().toISOString().split('T')[0]
 };
 await fetch('/add',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(data)});
 loadExpenses();
}

async function del(id){
 await fetch('/delete/'+id,{method:'DELETE'});
 loadExpenses();
}

function drawChart(cats){
 const ctx = document.getElementById('chart');
 if(chart) chart.destroy();
 chart = new Chart(ctx,{
  type:'pie',
  data:{labels:Object.keys(cats),datasets:[{data:Object.values(cats)}]}
 });
}

loadExpenses();
</script>
</body>
</html>
"""

@app.route('/')
def home():
    if 'user_id' not in session:
        return redirect('/login')
    return render_template_string(HTML)

# ---------- RUN ----------

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)