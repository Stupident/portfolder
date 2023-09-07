from flask import Blueprint, render_template, request

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Handle login form submission
        username = request.form.get('username')
        password = request.form.get('password')
        # Perform login logic
        return render_template('profile.html', username=username)
    # Render the login form template for GET request
    return render_template('login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Handle registration form submission
        username = request.form.get('username')
        password = request.form.get('password')
        # Perform registration logic
        return render_template('login.html')
    # Render the registration form template for GET request
    return render_template('register.html')

@auth_bp.route('/logout')
def logout():
    # Perform logout logic
    return render_template('login.html')
