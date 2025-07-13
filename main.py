import os
import sqlite3
import io
from flask import Flask, render_template, request, redirect, url_for, send_file, flash, session
from datetime import datetime
import qrcode
from PIL import Image

app = Flask(__name__)
app.secret_key = 'your_secret_key_change_in_production'
DATABASE = 'event.db'
ADMIN_PASSWORD = 'event@123'

# --- Database Initialization ---
def init_db():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS events (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        description TEXT,
        date TEXT NOT NULL
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS registrations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        event_id INTEGER,
        name TEXT NOT NULL,
        email TEXT NOT NULL,
        checked_in INTEGER DEFAULT 0,
        feedback_given INTEGER DEFAULT 0,
        FOREIGN KEY(event_id) REFERENCES events(id)
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS feedback (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        registration_id INTEGER,
        rating INTEGER,
        comment TEXT,
        FOREIGN KEY(registration_id) REFERENCES registrations(id)
    )''')
    conn.commit()
    conn.close()

# --- Helper Functions ---
def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def generate_qr(data):
    qr = qrcode.QRCode(box_size=10, border=2)
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    buf = io.BytesIO()
    img.save(buf, format='PNG')
    buf.seek(0)
    return buf

# --- Authentication Functions ---
def require_admin_auth():
    """Check if user is authenticated as admin"""
    return session.get('admin_authenticated', False)

def admin_required(f):
    """Decorator to require admin authentication"""
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not require_admin_auth():
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated_function

# --- Routes ---
@app.route('/')
def index():
    conn = get_db_connection()
    events = conn.execute('SELECT * FROM events ORDER BY date DESC').fetchall()
    conn.close()
    return render_template('index.html', events=events)

@app.route('/register', methods=['GET', 'POST'])
def register():
    conn = get_db_connection()
    events = conn.execute('SELECT * FROM events ORDER BY date DESC').fetchall()
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        event_id = request.form['event_id']
        c = conn.cursor()
        c.execute('INSERT INTO registrations (event_id, name, email) VALUES (?, ?, ?)',
                  (event_id, name, email))
        reg_id = c.lastrowid
        conn.commit()
        conn.close()
        qr_url = url_for('verify', reg_id=reg_id, _external=True)
        return render_template('qr.html', qr_url=qr_url, reg_id=reg_id)
    conn.close()
    return render_template('register.html', events=events)

@app.route('/qr/<int:reg_id>')
def qr_image(reg_id):
    qr_url = url_for('verify', reg_id=reg_id, _external=True)
    buf = generate_qr(qr_url)
    return send_file(buf, mimetype='image/png')

@app.route('/verify/<int:reg_id>', methods=['GET', 'POST'])
@admin_required
def verify(reg_id):
    conn = get_db_connection()
    reg = conn.execute('SELECT * FROM registrations WHERE id = ?', (reg_id,)).fetchone()
    if not reg:
        conn.close()
        return 'Registration not found', 404
    if request.method == 'POST':
        conn.execute('UPDATE registrations SET checked_in = 1 WHERE id = ?', (reg_id,))
        conn.commit()
        conn.close()
        feedback_link = url_for('feedback', reg_id=reg_id, _external=True)
        return render_template('checked_in.html', feedback_link=feedback_link)
    conn.close()
    return render_template('verify.html', reg=reg)

@app.route('/feedback/<int:reg_id>', methods=['GET', 'POST'])
def feedback(reg_id):
    conn = get_db_connection()
    reg = conn.execute('SELECT * FROM registrations WHERE id = ?', (reg_id,)).fetchone()
    if not reg or not reg['checked_in']:
        conn.close()
        return 'Not checked in or registration not found', 403
    if reg['feedback_given']:
        conn.close()
        return render_template('thankyou.html')  # Show thank you if already submitted
    if request.method == 'POST':
        rating = int(request.form['rating'])
        comment = request.form['comment']
        conn.execute('INSERT INTO feedback (registration_id, rating, comment) VALUES (?, ?, ?)',
                     (reg_id, rating, comment))
        conn.execute('UPDATE registrations SET feedback_given = 1 WHERE id = ?', (reg_id,))
        conn.commit()
        conn.close()
        return render_template('thankyou.html')
    conn.close()
    return render_template('feedback.html', reg=reg)

@app.route('/admin', methods=['GET', 'POST'])
@admin_required
def admin():
    conn = get_db_connection()
    events = conn.execute('SELECT * FROM events ORDER BY date DESC').fetchall()
    participants = []
    selected_event = None
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        date = request.form['date']
        conn.execute('INSERT INTO events (title, description, date) VALUES (?, ?, ?)',
                     (title, description, date))
        conn.commit()
    event_id = request.args.get('event_id')
    if event_id:
        selected_event = conn.execute('SELECT * FROM events WHERE id = ?', (event_id,)).fetchone()
        participants = conn.execute('SELECT * FROM registrations WHERE event_id = ?', (event_id,)).fetchall()
    conn.close()
    return render_template('admin.html', events=events, participants=participants, selected_event=selected_event)

@app.route('/admin/feedback/<int:event_id>')
@admin_required
def view_feedback(event_id):
    conn = get_db_connection()
    event = conn.execute('SELECT * FROM events WHERE id = ?', (event_id,)).fetchone()
    if not event:
        conn.close()
        return 'Event not found', 404
    
    feedback_data = conn.execute('''
        SELECT f.rating, f.comment, f.id as feedback_id, r.name, r.email, r.id as reg_id
        FROM feedback f
        JOIN registrations r ON f.registration_id = r.id
        WHERE r.event_id = ?
        ORDER BY f.id DESC
    ''', (event_id,)).fetchall()
    
    # Get statistics
    stats = conn.execute('''
        SELECT 
            COUNT(*) as total_registrations,
            SUM(CASE WHEN checked_in = 1 THEN 1 ELSE 0 END) as checked_in_count,
            SUM(CASE WHEN feedback_given = 1 THEN 1 ELSE 0 END) as feedback_count
        FROM registrations WHERE event_id = ?
    ''', (event_id,)).fetchone()
    
    # Get rating distribution
    rating_stats = conn.execute('''
        SELECT rating, COUNT(*) as count
        FROM feedback f
        JOIN registrations r ON f.registration_id = r.id
        WHERE r.event_id = ?
        GROUP BY rating
        ORDER BY rating
    ''', (event_id,)).fetchall()
    
    conn.close()
    
    return render_template('feedback_view.html', 
                         event=event, 
                         feedback_data=feedback_data, 
                         stats=stats,
                         rating_stats=rating_stats)

@app.route('/scan')
@admin_required
def scan():
    return render_template('scan.html')

@app.route('/manual_checkin', methods=['POST'])
@admin_required
def manual_checkin():
    reg_id = request.form['reg_id']
    return redirect(url_for('verify', reg_id=reg_id))

@app.route('/user', methods=['GET', 'POST'])
def user_panel():
    if request.method == 'POST':
        email = request.form['email']
        conn = get_db_connection()
        registrations = conn.execute('''
            SELECT r.*, e.title, e.description, e.date 
            FROM registrations r 
            JOIN events e ON r.event_id = e.id 
            WHERE r.email = ? 
            ORDER BY e.date DESC
        ''', (email,)).fetchall()
        conn.close()
        return render_template('user_panel.html', registrations=registrations, user_email=email)
    return render_template('user_panel.html', registrations=None, user_email=None)

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        password = request.form['password']
        if password == ADMIN_PASSWORD:
            session['admin_authenticated'] = True
            flash('Successfully logged in as admin!', 'success')
            return redirect(url_for('admin'))
        else:
            flash('Invalid password. Please try again.', 'error')
    return render_template('admin_login.html')

@app.route('/admin/logout')
def admin_logout():
    session.pop('admin_authenticated', None)
    flash('Successfully logged out.', 'info')
    return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
