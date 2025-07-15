import os
import io
from flask import Flask, render_template, request, redirect, url_for, send_file, flash, session
from datetime import datetime
import qrcode
from PIL import Image
from data_service import event_service

app = Flask(__name__)
app.secret_key = 'your_secret_key_change_in_production'
ADMIN_PASSWORD = 'event@123'

# --- Helper Functions ---

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
    events = event_service.get_all_events()
    return render_template('index.html', events=events)

@app.route('/register', methods=['GET', 'POST'])
def register():
    events = event_service.get_all_events()
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        event_id = request.form['event_id']
        reg_id = event_service.create_registration(event_id, name, email)
        qr_url = url_for('verify', reg_id=reg_id, _external=True)
        return render_template('qr.html', qr_url=qr_url, reg_id=reg_id)
    return render_template('register.html', events=events)

@app.route('/qr/<reg_id>')
def qr_image(reg_id):
    qr_url = url_for('verify', reg_id=reg_id, _external=True)
    buf = generate_qr(qr_url)
    return send_file(buf, mimetype='image/png')

@app.route('/verify/<reg_id>', methods=['GET', 'POST'])
@admin_required
def verify(reg_id):
    reg = event_service.get_registration_by_id(reg_id)
    if not reg:
        return 'Registration not found', 404
    if request.method == 'POST':
        event_service.update_checkin_status(reg_id, True)
        feedback_link = url_for('feedback', reg_id=reg_id, _external=True)
        return render_template('checked_in.html', feedback_link=feedback_link)
    return render_template('verify.html', reg=reg)

@app.route('/feedback/<reg_id>', methods=['GET', 'POST'])
def feedback(reg_id):
    reg = event_service.get_registration_by_id(reg_id)
    if not reg or not reg.get('checked_in', False):
        return 'Not checked in or registration not found', 403
    if reg.get('feedback_given', False):
        return render_template('thankyou.html')  # Show thank you if already submitted
    if request.method == 'POST':
        rating = int(request.form['rating'])
        comment = request.form['comment']
        event_service.create_feedback(reg_id, rating, comment)
        event_service.update_feedback_status(reg_id, True)
        return render_template('thankyou.html')
    return render_template('feedback.html', reg=reg)

@app.route('/admin', methods=['GET', 'POST'])
@admin_required
def admin():
    events = event_service.get_all_events()
    participants = []
    selected_event = None
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        date = request.form['date']
        event_service.create_event(title, description, date)
    event_id = request.args.get('event_id')
    if event_id:
        selected_event = event_service.get_event_by_id(event_id)
        participants = event_service.get_registrations_by_event(event_id)
    return render_template('admin.html', events=events, participants=participants, selected_event=selected_event)

@app.route('/admin/feedback/<event_id>')
@admin_required
def view_feedback(event_id):
    event = event_service.get_event_by_id(event_id)
    if not event:
        return 'Event not found', 404
    
    feedback_data = event_service.get_feedback_by_event(event_id)
    stats = event_service.get_event_statistics(event_id)
    rating_stats = event_service.get_rating_statistics(event_id)
    
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
        registrations = event_service.get_registrations_by_email(email)
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
    app.run(debug=True)
