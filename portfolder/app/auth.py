from flask import Blueprint, render_template, request, flash, redirect, url_for
from requests.structures import CaseInsensitiveDict
from email_validator import validate_email, EmailNotValidError
from .models import User
from . import db
from werkzeug.security import generate_password_hash, check_password_hash 
from flask_login import login_user, login_required, logout_user, current_user
from .validator import *

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.form
        login = data.get('login')
        password = data.get('password')
        print(data)
        
        user = User.query.filter_by(email=login).first()
        if not user:
            user = User.query.filter_by(username=login).first()

        if user:
            if check_password_hash(user.password, password):
                flash(f'Welcome back, {user.username}', category="success")
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash(f'Incorrect password for {login}', category="error")
        else:
            flash(f'{login} doesn`t exists', category="error")

    return render_template("login.html", user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/signup', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        data = request.form
        email = data.get('email')
        username = data.get('username')
        password1 = data.get('password1')
        password2 = data.get('password2')

        email_check = valid_email(email)
        password_check = valid_password(password1)
        username_check = valid_username(username)

        if User.query.filter_by(email=email).first():
            flash(f"Email {email} already exists", category="error")
        elif User.query.filter_by(username=username).first():
            flash(f"Username {username} is already taken", category="error")
        elif not email_check[0]:
            flash(email_check[1], category="error")
        elif not password_check[0]:
            flash(password_check[1], category="error")
        elif password1 != password2:
            flash('Password don`t match', category="error")
        elif not username_check[0]:
            flash(username_check[1], category="error")
        else:
            new_user = User(email=email, username=username, 
                            password=generate_password_hash(password1, method='scrypt'))
            db.session.add(new_user)
            db.session.commit()

            flash(f'Registration success, hi {username}!', category="success")

            login_user(new_user, remember=True)
            return redirect(url_for('views.home'))
    return render_template("signup.html", user=current_user)
