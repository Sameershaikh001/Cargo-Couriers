import os
from flask import Flask, render_template, request, jsonify, session, redirect, url_for, flash
import sqlite3
import uuid
from werkzeug.security import generate_password_hash, check_password_hash

# ================= CONFIG =================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = Flask(
    __name__,
    template_folder=os.path.join(BASE_DIR, "templates"),
    static_folder=os.path.join(BASE_DIR, "static")
)

app.secret_key = 'your-secret-key-here'

# ✅ Vercel-safe DB path
DB_PATH = "/tmp/awt_cargo.db"


# ================= DATABASE =================

def get_db_connection():
    return sqlite3.connect(DB_PATH)


def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT, email TEXT UNIQUE, phone TEXT, password TEXT,
        user_type TEXT DEFAULT 'customer'
    )''')

    c.execute('''CREATE TABLE IF NOT EXISTS parcels (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tracking_number TEXT UNIQUE,
        sender_name TEXT, sender_phone TEXT, sender_address TEXT,
        receiver_name TEXT, receiver_phone TEXT, receiver_address TEXT,
        parcel_weight DECIMAL, parcel_description TEXT,
        service_type TEXT, status TEXT DEFAULT 'Booked'
    )''')

    c.execute('''CREATE TABLE IF NOT EXISTS partners (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        company_name TEXT, contact_person TEXT,
        email TEXT, phone TEXT
    )''')

    c.execute('''CREATE TABLE IF NOT EXISTS tracking_updates (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tracking_number TEXT, status TEXT, location TEXT
    )''')

    c.execute('''CREATE TABLE IF NOT EXISTS admin_users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE, password TEXT
    )''')

    # default admin
    password = generate_password_hash("admin123")
    c.execute("INSERT OR IGNORE INTO admin_users (username, password) VALUES (?, ?)",
              ("admin", password))

    conn.commit()
    conn.close()


# ✅ SAFE INIT (important for Vercel)
@app.before_request
def init_database_once():
    if not hasattr(app, "db_initialized"):
        try:
            init_db()
            app.db_initialized = True
        except Exception as e:
            print("DB init error:", e)


# ================= DEBUG =================

@app.route('/health')
def health():
    return "OK"


# ================= AUTH =================

def admin_required(f):
    from functools import wraps
    @wraps(f)
    def wrapper(*args, **kwargs):
        if 'admin_logged_in' not in session:
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return wrapper


# ================= ADMIN =================

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        conn = get_db_connection()
        c = conn.cursor()
        c.execute("SELECT * FROM admin_users WHERE username=?", (request.form['username'],))
        user = c.fetchone()
        conn.close()

        if user and check_password_hash(user[2], request.form['password']):
            session['admin_logged_in'] = True
            return redirect(url_for('admin_dashboard'))

    return render_template('admin/login.html')


@app.route('/admin/dashboard')
@admin_required
def admin_dashboard():
    return render_template('admin/dashboard.html')


# ================= PUBLIC =================

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/partner-registration', methods=['GET', 'POST'])
def partner_registration():
    if request.method == 'POST':
        conn = get_db_connection()
        c = conn.cursor()
        c.execute("INSERT INTO partners (company_name) VALUES (?)",
                  (request.form['company_name'],))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    return render_template('partner-registration.html')


@app.route('/booking', methods=['GET', 'POST'])
def booking():
    if request.method == 'POST':
        tracking_number = 'AWT' + str(uuid.uuid4().hex[:8]).upper()

        conn = get_db_connection()
        c = conn.cursor()
        c.execute("INSERT INTO parcels (tracking_number, sender_name) VALUES (?, ?)",
                  (tracking_number, request.form['sender_name']))
        conn.commit()
        conn.close()

        return redirect(url_for('tracking'))

    return render_template('booking.html')


@app.route('/tracking', methods=['GET', 'POST'])
def tracking():
    return render_template('tracking.html')


@app.route('/calculator', methods=['GET', 'POST'])
def calculator():
    return render_template('calculator.html')


@app.route('/services')
def services():
    return render_template('services.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/api/calculate-rate', methods=['POST'])
def api_calculate_rate():
    data = request.json
    return jsonify({'rate': float(data['weight']) * 10})


# ================= RUN =================

if __name__ == "__main__":
    app.run()