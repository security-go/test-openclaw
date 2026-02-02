
from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
import os
import hashlib # For password hashing

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your_super_secret_key_change_me_please_for_security')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

# User model for database
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False) # Store hashed passwords

    def set_password(self, password):
        self.password_hash = hashlib.sha256(password.encode('utf-8')).hexdigest()

    def check_password(self, password):
        return self.password_hash == hashlib.sha256(password.encode('utf-8')).hexdigest()

    def __repr__(self):
        return f'<User {self.username}>'

# --- Database Initialization ---
with app.app_context():
    db.create_all()
    # Add default admin if not exists
    if not User.query.filter_by(username='admin').first():
        admin_user = User(username='admin')
        admin_user.set_password('password123')
        db.session.add(admin_user)
        db.session.commit()
        print("Default admin user 'admin' created with password 'password123'")
    else:
        print("Default admin user 'admin' already exists.")

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
        return redirect(url_for('dashboard'))
    else:
        # Redirect to index with error message for consistency with GET request
        return redirect(url_for('index', error="Invalid ID or Password. Please try again."))

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('index'))
    return render_template('dashboard.html', username=session['username'])

@app.route('/admin_management', methods=['GET', 'POST'])
def admin_management():
    if 'username' not in session:
        return redirect(url_for('index'))
    
    # Only allow 'admin' user to access this page
    if session['username'] != 'admin':
        flash('You do not have permission to access this page.', 'error')
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        action = request.form.get('action')
        
        if action == 'add':
            new_username = request.form.get('new_username')
            new_password = request.form.get('new_password')
            if new_username and new_password:
                existing_user = User.query.filter_by(username=new_username).first()
                if existing_user:
                    flash(f'User "{new_username}" already exists.', 'error')
                else:
                    user = User(username=new_username)
                    user.set_password(new_password)
                    db.session.add(user)
                    db.session.commit()
                    flash(f'Admin user "{new_username}" created successfully.', 'success')
            else:
                flash('Username and password are required to add an admin.', 'error')
        
        return redirect(url_for('admin_management'))

    users = User.query.all()
    return render_template('admin_management.html', username=session['username'], users=users)

@app.route('/delete_admin/<int:user_id>', methods=['POST'])
def delete_admin(user_id):
    if 'username' not in session:
        return redirect(url_for('index'))
    
    # Only allow 'admin' user to access this page
    if session['username'] != 'admin':
        flash('You do not have permission to delete users.', 'error')
        return redirect(url_for('dashboard'))

    user_to_delete = User.query.get_or_404(user_id)
    if user_to_delete.username == 'admin':
        flash('Cannot delete the default admin user.', 'error')
    else:
        db.session.delete(user_to_delete)
        db.session.commit()
        flash(f'User "{user_to_delete.username}" deleted successfully.', 'success')
    
    return redirect(url_for('admin_management'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001) # Port changed to 5001 to avoid conflict
