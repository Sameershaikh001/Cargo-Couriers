import os
from flask import Flask, render_template, request, jsonify, session, redirect, url_for, flash
import sqlite3
from datetime import datetime
import uuid
from werkzeug.security import generate_password_hash, check_password_hash

# ✅ BASE DIRECTORY (Vercel Fix)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ✅ Flask App Config (Fix static & templates path)
app = Flask(
    __name__,
    template_folder=os.path.join(BASE_DIR, "templates"),
    static_folder=os.path.join(BASE_DIR, "static")
)

app.secret_key = 'your-secret-key-here'

# ✅ Database Path (Vercel Fix)
DB_PATH = os.path.join(BASE_DIR, 'database', 'awt_cargo.db')


# ==================== DATABASE ====================

def get_db_connection():
    return sqlite3.connect(DB_PATH)


def init_db():
    conn = get_db_connection()
    c = conn.cursor()

    # Users table
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            phone TEXT,
            password TEXT,
            user_type TEXT DEFAULT 'customer',
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Parcels table
    c.execute('''
        CREATE TABLE IF NOT EXISTS parcels (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tracking_number TEXT UNIQUE NOT NULL,
            user_id INTEGER,
            sender_name TEXT NOT NULL,
            sender_phone TEXT NOT NULL,
            sender_address TEXT NOT NULL,
            receiver_name TEXT NOT NULL,
            receiver_phone TEXT NOT NULL,
            receiver_address TEXT NOT NULL,
            parcel_weight DECIMAL,
            parcel_description TEXT,
            service_type TEXT,
            status TEXT DEFAULT 'Booked',
            booking_date DATETIME DEFAULT CURRENT_TIMESTAMP,
            estimated_delivery DATE,
            current_location TEXT,
            delivery_notes TEXT,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')

    # Partners table
    c.execute('''
        CREATE TABLE IF NOT EXISTS partners (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company_name TEXT,
            contact_person TEXT,
            email TEXT,
            phone TEXT,
            address TEXT,
            service_area TEXT,
            business_type TEXT,
            message TEXT,
            status TEXT DEFAULT 'Pending',
            applied_date DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Tracking updates table
    c.execute('''
        CREATE TABLE IF NOT EXISTS tracking_updates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tracking_number TEXT NOT NULL,
            status TEXT NOT NULL,
            location TEXT,
            update_time DATETIME DEFAULT CURRENT_TIMESTAMP,
            notes TEXT
        )
    ''')

    # Admin users table
    c.execute('''
        CREATE TABLE IF NOT EXISTS admin_users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            full_name TEXT,
            role TEXT DEFAULT 'admin',
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Default admin
    default_admin_password = generate_password_hash('admin123')
    c.execute('''
        INSERT OR IGNORE INTO admin_users (username, email, password, full_name, role)
        VALUES (?, ?, ?, ?, ?)
    ''', ('admin', 'admin@awtcargo.com', default_admin_password, 'System Administrator', 'superadmin'))

    conn.commit()
    conn.close()


# Initialize DB
init_db()


# ==================== AUTH DECORATOR ====================

def admin_required(f):
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin_logged_in' not in session:
            flash('Please login as administrator', 'error')
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated_function


# ==================== ADMIN ROUTES ====================

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db_connection()
        c = conn.cursor()
        c.execute('SELECT * FROM admin_users WHERE username = ?', (username,))
        admin = c.fetchone()
        conn.close()

        if admin and check_password_hash(admin[3], password):
            session['admin_logged_in'] = True
            session['admin_id'] = admin[0]
            session['admin_username'] = admin[1]
            session['admin_role'] = admin[5]
            flash('Login successful!', 'success')
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Invalid username or password', 'error')

    return render_template('admin/login.html')


@app.route('/admin/logout')
def admin_logout():
    session.clear()
    flash('Logged out successfully', 'success')
    return redirect(url_for('admin_login'))


@app.route('/admin/dashboard')
@admin_required
def admin_dashboard():
    conn = get_db_connection()
    c = conn.cursor()

    c.execute('SELECT COUNT(*) FROM parcels')
    total_parcels = c.fetchone()[0]

    c.execute('SELECT COUNT(*) FROM parcels WHERE status = "Booked"')
    booked_parcels = c.fetchone()[0]

    c.execute('SELECT COUNT(*) FROM parcels WHERE status = "In Transit"')
    transit_parcels = c.fetchone()[0]

    c.execute('SELECT COUNT(*) FROM parcels WHERE status = "Delivered"')
    delivered_parcels = c.fetchone()[0]

    c.execute('SELECT COUNT(*) FROM partners')
    total_partners = c.fetchone()[0]

    c.execute('SELECT COUNT(*) FROM partners WHERE status = "Pending"')
    pending_partners = c.fetchone()[0]

    c.execute('SELECT COUNT(*) FROM users')
    total_users = c.fetchone()[0]

    c.execute('SELECT * FROM parcels ORDER BY booking_date DESC LIMIT 10')
    recent_parcels = c.fetchall()

    conn.close()

    return render_template('admin/dashboard.html',
                           total_parcels=total_parcels,
                           booked_parcels=booked_parcels,
                           transit_parcels=transit_parcels,
                           delivered_parcels=delivered_parcels,
                           total_partners=total_partners,
                           pending_partners=pending_partners,
                           total_users=total_users,
                           recent_parcels=recent_parcels)


@app.route('/admin/parcels')
@admin_required
def admin_parcels():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('SELECT * FROM parcels ORDER BY booking_date DESC')
    parcels = c.fetchall()
    conn.close()

    return render_template('admin/parcels.html', parcels=parcels)


@app.route('/admin/parcel/<tracking_number>')
@admin_required
def admin_parcel_detail(tracking_number):
    conn = get_db_connection()
    c = conn.cursor()

    c.execute('SELECT * FROM parcels WHERE tracking_number = ?', (tracking_number,))
    parcel = c.fetchone()

    c.execute('SELECT * FROM tracking_updates WHERE tracking_number = ? ORDER BY update_time DESC', (tracking_number,))
    updates = c.fetchall()

    conn.close()

    if parcel:
        return render_template('admin/parcel_detail.html', parcel=parcel, updates=updates)
    else:
        flash('Parcel not found', 'error')
        return redirect(url_for('admin_parcels'))


@app.route('/admin/update_parcel_status', methods=['POST'])
@admin_required
def update_parcel_status():
    tracking_number = request.form['tracking_number']
    new_status = request.form['status']
    location = request.form.get('location', '')
    notes = request.form.get('notes', '')

    conn = get_db_connection()
    c = conn.cursor()

    try:
        c.execute('UPDATE parcels SET status = ?, current_location = ? WHERE tracking_number = ?',
                  (new_status, location, tracking_number))

        c.execute('''
            INSERT INTO tracking_updates (tracking_number, status, location, notes)
            VALUES (?, ?, ?, ?)
        ''', (tracking_number, new_status, location, notes))

        conn.commit()
        flash('Parcel status updated successfully!', 'success')

    except Exception as e:
        flash(f'Error updating status: {str(e)}', 'error')
    finally:
        conn.close()

    return redirect(url_for('admin_parcel_detail', tracking_number=tracking_number))

@app.route('/partner-registration', methods=['GET', 'POST'])
def partner_registration():
    if request.method == 'POST':
        conn = get_db_connection()
        c = conn.cursor()

        try:
            c.execute('''
                INSERT INTO partners (
                    company_name, contact_person, email, phone,
                    address, service_area, business_type, message
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                request.form['company_name'],
                request.form['contact_person'],
                request.form['email'],
                request.form['phone'],
                request.form['address'],
                request.form['service_area'],
                request.form['business_type'],
                request.form['message']
            ))

            conn.commit()
            flash('Registration successful! We will contact you soon.', 'success')
            return redirect(url_for('index'))

        except Exception as e:
            flash('Error submitting registration.', 'error')
        finally:
            conn.close()

    return render_template('partner-registration.html')
# ==================== PUBLIC ROUTES ====================

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/services')
def services():
    return render_template('services.html')


@app.route('/tracking', methods=['GET', 'POST'])
def tracking():
    if request.method == 'POST':
        tracking_number = request.form['tracking_number']

        conn = get_db_connection()
        c = conn.cursor()

        c.execute('SELECT * FROM parcels WHERE tracking_number = ?', (tracking_number,))
        parcel = c.fetchone()

        c.execute('SELECT * FROM tracking_updates WHERE tracking_number = ? ORDER BY update_time DESC',
                  (tracking_number,))
        updates = c.fetchall()

        conn.close()

        if parcel:
            return render_template('tracking.html', parcel=parcel, updates=updates)
        else:
            flash('Parcel not found', 'error')

    return render_template('tracking.html')


@app.route('/booking', methods=['GET', 'POST'])
def booking():
    if request.method == 'POST':
        tracking_number = 'AWT' + str(uuid.uuid4().hex[:10]).upper()

        conn = get_db_connection()
        c = conn.cursor()

        try:
            c.execute('''
                INSERT INTO parcels (
                    tracking_number, sender_name, sender_phone, sender_address,
                    receiver_name, receiver_phone, receiver_address,
                    parcel_weight, parcel_description, service_type, status
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                tracking_number,
                request.form['sender_name'],
                request.form['sender_phone'],
                request.form['sender_address'],
                request.form['receiver_name'],
                request.form['receiver_phone'],
                request.form['receiver_address'],
                request.form['weight'],
                request.form['description'],
                request.form['service_type'],
                'Booked'
            ))

            c.execute('''
                INSERT INTO tracking_updates (tracking_number, status, notes)
                VALUES (?, ?, ?)
            ''', (tracking_number, 'Booked', 'Parcel booked'))

            conn.commit()
            flash(f'Tracking Number: {tracking_number}', 'success')
            return redirect(url_for('tracking'))

        except:
            flash('Booking failed', 'error')
        finally:
            conn.close()

    return render_template('booking.html')


@app.route('/calculator', methods=['GET', 'POST'])
def calculator():
    rate = None
    if request.method == 'POST':
        weight = float(request.form['weight'])
        service_type = request.form['service_type']

        base_rates = {'standard': 50, 'express': 80, 'same_day': 120}
        rate = base_rates.get(service_type, 50) + (weight * 10)

    return render_template('calculator.html', rate=rate)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        flash('Message sent successfully!', 'success')
    return render_template('contact.html')


@app.route('/api/calculate-rate', methods=['POST'])
def api_calculate_rate():
    data = request.json
    weight = float(data['weight'])
    service_type = data['service_type']

    base_rates = {'standard': 50, 'express': 80, 'same_day': 120}
    rate = base_rates.get(service_type, 50) + (weight * 8)

    return jsonify({'rate': round(rate, 2)})


if __name__ == "__main__":
    app.run()