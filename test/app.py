
from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
import hashlib

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your_super_secret_key_change_me_please_for_security')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# --- Models ---
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)

    def set_password(self, password):
        self.password_hash = hashlib.sha256(password.encode('utf-8')).hexdigest()

    def check_password(self, password):
        return self.password_hash == hashlib.sha256(password.encode('utf-8')).hexdigest()

class AuditLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.now)
    username = db.Column(db.String(80), nullable=False)
    action = db.Column(db.String(50), nullable=False)
    details = db.Column(db.String(255))
    ip_address = db.Column(db.String(45))

# --- Utils ---
def log_action(action, details):
    username = session.get('username', 'Anonymous')
    new_log = AuditLog(
        username=username,
        action=action,
        details=details,
        ip_address=request.remote_addr
    )
    db.session.add(new_log)
    db.session.commit()

# --- Database Initialization ---
with app.app_context():
    db.create_all()
    if not User.query.filter_by(username='admin').first():
        admin_user = User(username='admin')
        admin_user.set_password('password123')
        db.session.add(admin_user)
        db.session.commit()

@app.route('/')
def index():
    if 'username' in session:
        return redirect(url_for('dashboard'))
    return render_template('login.html', error=request.args.get('error'))

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('id')
    password = request.form.get('password')
    user = User.query.filter_by(username=username).first()

    if user and user.check_password(password):
        session['username'] = user.username
        log_action('LOGIN', f'User {username} logged in successfully.')
        return redirect(url_for('dashboard'))
    else:
        log_action('LOGIN_FAILED', f'Failed login attempt for ID: {username}')
        return redirect(url_for('index', error="Invalid ID or Password."))

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('index'))
    return render_template('dashboard.html', username=session['username'])

@app.route('/admin_management', methods=['GET', 'POST'])
def admin_management():
    if 'username' not in session: return redirect(url_for('index'))
    if session['username'] != 'admin':
        flash('Permission denied.', 'error')
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'add':
            new_username = request.form.get('new_username')
            new_password = request.form.get('new_password')
            if new_username and new_password:
                if User.query.filter_by(username=new_username).first():
                    flash(f'User {new_username} exists.', 'error')
                else:
                    user = User(username=new_username)
                    user.set_password(new_password)
                    db.session.add(user)
                    db.session.commit()
                    log_action('CREATE_USER', f'Created admin user: {new_username}')
                    flash(f'User {new_username} created.', 'success')
        return redirect(url_for('admin_management'))

    users = User.query.all()
    return render_template('admin_management.html', username=session['username'], users=users)

@app.route('/delete_admin/<int:user_id>', methods=['POST'])
def delete_admin(user_id):
    if 'username' not in session: return redirect(url_for('index'))
    if session['username'] != 'admin': return redirect(url_for('dashboard'))

    user = User.query.get_or_404(user_id)
    if user.username == 'admin':
        flash('Cannot delete default admin.', 'error')
    else:
        uname = user.username
        db.session.delete(user)
        db.session.commit()
        log_action('DELETE_USER', f'Deleted admin user: {uname}')
        flash(f'User {uname} deleted.', 'success')
    return redirect(url_for('admin_management'))

@app.route('/audit_log')
def audit_log():
    if 'username' not in session: return redirect(url_for('index'))
    
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    logs = AuditLog.query.order_by(AuditLog.timestamp.desc()).paginate(page=page, per_page=per_page)
    return render_template('audit_log.html', username=session['username'], logs=logs, per_page=per_page)

@app.route('/logout')
def logout():
    log_action('LOGOUT', f"User {session.get('username')} logged out.")
    session.pop('username', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
