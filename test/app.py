
from flask import Flask, render_template_string, request, redirect, url_for, session
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
    return render_template_string('''
        <!doctype html>
        <html lang="en">
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <title>Login</title>
            <style>
                body { font-family: sans-serif; display: flex; justify-content: center; align-items: center; min-height: 80vh; background-color: #f4f4f4; }
                .login-container { background-color: #fff; padding: 30px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
                h2 { text-align: center; margin-bottom: 20px; color: #333; }
                .form-group { margin-bottom: 15px; }
                label { display: block; margin-bottom: 5px; font-weight: bold; }
                input[type="text"], input[type="password"] { width: 100%; padding: 10px; border: 1px solid #ccc; border-radius: 4px; box-sizing: border-box; }
                button { width: 100%; padding: 10px; background-color: #5cb85c; color: white; border: none; border-radius: 4px; cursor: pointer; font-size: 16px; }
                button:hover { background-color: #4cae4c; }
                .error { color: red; text-align: center; margin-bottom: 15px; }
            </style>
        </head>
        <body>
            <div class="login-container">
                <h2>Welcome Back!</h2>
                {% if error %}
                    <p class="error">{{ error }}</p>
                {% endif %}
                <form method="POST" action="{{ url_for('login') }}">
                    <div class="form-group">
                        <label for="id">ID:</label>
                        <input type="text" id="id" name="id" required>
                    </div>
                    <div class="form-group">
                        <label for="password">Password:</label>
                        <input type="password" id="password" name="password" required>
                    </div>
                    <button type="submit">Login</button>
                </form>
            </div>
        </body>
        </html>
    ''')

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('id')
    password = request.form.get('password')

    if username == ADMIN_USER and password == ADMIN_PASSWORD:
        session['username'] = username
        return redirect(url_for('dashboard'))
    else:
        # Simple error message for now
        return render_template_string('''
            <!doctype html>
            <html lang="en">
            <head>
                <meta charset="utf-8">
                <meta name="viewport" content="width=device-width, initial-scale=1">
                <title>Login</title>
                <style>
                    body { font-family: sans-serif; display: flex; justify-content: center; align-items: center; min-height: 80vh; background-color: #f4f4f4; }
                    .login-container { background-color: #fff; padding: 30px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
                    h2 { text-align: center; margin-bottom: 20px; color: #333; }
                    .form-group { margin-bottom: 15px; }
                    label { display: block; margin-bottom: 5px; font-weight: bold; }
                    input[type="text"], input[type="password"] { width: 100%; padding: 10px; border: 1px solid #ccc; border-radius: 4px; box-sizing: border-box; }
                    button { width: 100%; padding: 10px; background-color: #5cb85c; color: white; border: none; border-radius: 4px; cursor: pointer; font-size: 16px; }
                    button:hover { background-color: #4cae4c; }
                    .error { color: red; text-align: center; margin-bottom: 15px; }
                </style>
            </head>
            <body>
                <div class="login-container">
                    <h2>Welcome Back!</h2>
                    <p class="error">Invalid ID or Password. Please try again.</p>
                    <form method="POST" action="{{ url_for('login') }}">
                        <div class="form-group">
                            <label for="id">ID:</label>
                            <input type="text" id="id" name="id" required>
                        </div>
                        <div class="form-group">
                            <label for="password">Password:</label>
                            <input type="password" id="password" name="password" required>
                        </div>
                        <button type="submit">Login</button>
                    </form>
                </div>
            </body>
            </html>
        ''')

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('index'))
    
    # Placeholder for the layout with menu and content
    return render_template_string('''
        <!doctype html>
        <html lang="en">
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <title>Dashboard</title>
            <style>
                body { display: flex; margin: 0; font-family: sans-serif; background-color: #f0f2f5;}
                .sidebar { width: 250px; background-color: #ffffff; padding: 20px; height: 100vh; box-shadow: 2px 0 5px rgba(0,0,0,0.1); overflow-y: auto; display: flex; flex-direction: column;}
                .sidebar h3 { margin-top: 0; color: #333; text-align: center; margin-bottom: 25px; font-size: 22px;}
                .sidebar ul { list-style: none; padding: 0; flex-grow: 1;}
                .sidebar ul li { margin-bottom: 15px; }
                .sidebar ul li a { text-decoration: none; color: #555; display: block; padding: 10px 12px; border-radius: 5px; transition: background-color 0.2s ease;}
                .sidebar ul li a:hover { background-color: #e9ecef; color: #007bff; }
                .sidebar .footer { text-align: center; font-size: 12px; color: #aaa; margin-top: auto; padding-top: 20px;}
                .main-content { flex-grow: 1; height: 100vh; overflow-y: auto; display: flex; flex-direction: column; }
                .header { background-color: #ffffff; padding: 15px 25px; border-bottom: 1px solid #e0e0e0; display: flex; justify-content: space-between; align-items: center; box-shadow: 0 1px 3px rgba(0,0,0,0.05); }
                .header h1 { margin: 0; color: #333; font-size: 26px; font-weight: 600; }
                .header .logout-button { padding: 10px 18px; background-color: #d9534f; color: white; border: none; border-radius: 5px; cursor: pointer; text-decoration: none; font-size: 14px; transition: background-color 0.2s ease;}
                .header .logout-button:hover { background-color: #c9302c; }
                .content-area { flex-grow: 1; padding: 30px; background-color: #ffffff; margin: 20px; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.05); }
                .content-area h2 { margin-top: 0; color: #444; font-size: 28px; margin-bottom: 20px; }
                .content-area p { color: #555; font-size: 16px; line-height: 1.6; }
            </style>
        </head>
        <body>
            <div class="sidebar">
                <h3>Menu</h3>
                <ul>
                    <li><a href="#">Dashboard Home</a></li>
                    <li><a href="#">Users</a></li>
                    <li><a href="#">Settings</a></li>
                    <li><a href="#">Reports</a></li>
                    <li><a href="#">System Logs</a></li>
                </ul>
                <div class="footer">
                    &copy; 2026 Your Company
                </div>
            </div>
            <div class="main-content">
                <div class="header">
                    <h1>Welcome, {{ session.username }}!</h1>
                    <a href="{{ url_for('logout') }}" class="logout-button">Logout</a>
                </div>
                <div class="content-area">
                    <h2>Main Content Area</h2>
                    <p>This is where the details of your selected menu item will be displayed.</p>
                    <p>You are logged in as <strong>{{ session.username }}</strong>.</p>
                    <p>Use the menu on the left to navigate through the application.</p>
                </div>
            </div>
        </body>
        </html>
    ''')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    # Running on 0.0.0.0 makes it accessible from other machines on the network if needed.
    # For local testing, '127.0.0.1' is also fine.
    # debug=True is useful for development, but should be False in production.
    app.run(debug=True, host='0.0.0.0', port=5000)
