import os
from flask import Flask, render_template, request, jsonify, session, redirect, url_for, flash
import sqlite3
from datetime import datetime
import uuid
from werkzeug.security import generate_password_hash, check_password_hash

# ✅ Base directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ✅ Flask config
app = Flask(
    __name__,
    template_folder=os.path.join(BASE_DIR, "templates"),
    static_folder=os.path.join(BASE_DIR, "static")
)

app.secret_key = 'your-secret-key-here'

# ✅ Vercel-safe DB path
DB_PATH = "/tmp/awt_cargo.db"


# ==================== DATABASE ====================

def get_db_connection():
    return sqlite3.connect(DB_PATH)


def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT, email TEXT UNIQUE, phone TEXT, password TEXT,
        user_type TEXT DEFAULT 'customer',
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )''')

    c.execute('''CREATE TABLE IF NOT EXISTS parcels (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tracking_number TEXT UNIQUE,
        sender_name TEXT, sender_phone TEXT, sender_address TEXT,
        receiver_name TEXT, receiver_phone TEXT, receiver_address TEXT,
        parcel_weight DECIMAL, parcel_description TEXT,
        service_type TEXT, status TEXT DEFAULT 'Booked',
        booking_date DATETIME DEFAULT CURRENT_TIMESTAMP
    )''')

    c.execute('''CREATE TABLE IF NOT EXISTS partners (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        company_name TEXT, contact_person TEXT, email TEXT, phone TEXT,
        address TEXT, service_area TEXT, business_type TEXT,
        message TEXT, status TEXT DEFAULT 'Pending'
    )''')

    c.execute('''CREATE TABLE IF NOT EXISTS tracking_updates (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tracking_number TEXT, status TEXT, location TEXT,
        update_time DATETIME DEFAULT CURRENT_TIMESTAMP, notes TEXT
    )''')

    c.execute('''CREATE TABLE IF NOT EXISTS admin_users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE, email TEXT UNIQUE,
        password TEXT, full_name TEXT, role TEXT DEFAULT 'admin'
    )''')

    default_admin_password = generate_password_hash('admin123')
    c.execute('''
        INSERT OR IGNORE INTO admin_users (username, email, password, full_name, role)
        VALUES (?, ?, ?, ?, ?)
    ''', ('admin', 'admin@awtcargo.com', default_admin_password, 'System Admin', 'superadmin'))

    conn.commit()
    conn.close()


# ✅ FIX: Run DB init ONLY when request comes (not at startup)
@app.before_request
def initialize_database():
    try:
        init_db()
    except Exception as e:
        print("DB init error:", e)


# ==================== DEBUG ROUTE ====================

@app.route('/health')
def health():
    return "OK"


# ==================== AUTH ====================

def admin_required(f):
    from functools import wraps
    @wraps(f)
    def wrapper(*args, **kwargs):
        if 'admin_logged_in' not in session:
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return wrapper


# ==================== ROUTES ====================

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/partner-registration', methods=['GET', 'POST'])
def partner_registration():
    if request.method == 'POST':
        conn = get_db_connection()
        c = conn.cursor()
        c.execute('INSERT INTO partners (company_name) VALUES (?)',
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

        c.execute('INSERT INTO parcels (tracking_number, sender_name) VALUES (?, ?)',
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


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/api/calculate-rate', methods=['POST'])
def api_calculate_rate():
    data = request.json
    weight = float(data['weight'])
    return jsonify({'rate': weight * 10})


# ==================== RUN ====================

if __name__ == "__main__":
    app.run()