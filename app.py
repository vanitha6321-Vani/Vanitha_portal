from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = 'mysecret123'


# 🔹 Home → redirect to login
@app.route('/')
def home():
    return redirect('/login')


# 🔹 Register
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        user = request.form['username']
        pwd = request.form['password']

        conn = sqlite3.connect('database.db')
        cur = conn.cursor()

        # check user already exists
        cur.execute("SELECT * FROM users WHERE username=?", (user,))
        existing_user = cur.fetchone()

        if existing_user:
            conn.close()
            return "User already exists!"

        # insert new user
        cur.execute("INSERT INTO users (username, password) VALUES (?, ?)", (user, pwd))
        conn.commit()
        conn.close()

        return redirect('/login')

    return render_template('register.html')


# 🔹 Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = request.form['username']
        pwd = request.form['password']

        conn = sqlite3.connect('database.db')
        cur = conn.cursor()

        cur.execute("SELECT * FROM users WHERE username=? AND password=?", (user, pwd))
        data = cur.fetchone()
        conn.close()

        if data:
            session['user'] = user
            return redirect('/dashboard')
        else:
            return "Invalid Username or Password"

    return render_template('login.html')


# 🔹 Dashboard
@app.route('/dashboard')
def dashboard():
    if 'user' in session:
        return render_template('dashboard.html', user=session['user'])
    return redirect('/login')


# 🔹 Logout
@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/login')


# 🔹 Run App (always last)
if __name__ == '__main__':
    app.run(debug=True)