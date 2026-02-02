
from flask import Flask, render_template, request, redirect, url_for, session
import os

app = Flask(__name__)
# IMPORTANT: Change this in production!
# Use a more secure way to generate/store this key, e.g., environment variable.
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your_super_secret_key_change_me_please_for_security')

# Dummy user credentials (for demonstration purposes)
# In a real application, you would store these securely and have a user management system.
ADMIN_USER = "admin"
ADMIN_PASSWORD = "password123"

@app.route('/')
def index():
    if 'username' in session:
        return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('id')
    password = request.form.get('password')

    if username == ADMIN_USER and password == ADMIN_PASSWORD:
        session['username'] = username
        return redirect(url_for('dashboard'))
    else:
        return render_template('login.html', error="Invalid ID or Password. Please try again.")

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('index'))
    return render_template('dashboard.html', username=session['username'])

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    # Running on 0.0.0.0 makes it accessible from other machines on the network if needed.
    # For local testing, '127.0.0.1' is also fine.
    # debug=True is useful for development, but should be False in production.
    app.run(debug=True, host='0.0.0.0', port=5001) # Port changed to 5001 to avoid conflict