# Login, Logout and Signup
from flask import Blueprint, render_template, redirect, url_for, request, flash
from . import db
from .models import User
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash


auth = Blueprint('auth', __name__)


# Login page
@auth.route('/login', methods=['Get', 'POST'])
def login():
    if request.method == 'POST':
        # Get data from form.
        email = request.form.get('email')
        pwd = request.form.get('password')

        # Check login info is correct
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.pwd, pwd):
                flash('Logged in successfully!', category='success')
                # If the user visiting the website is logged in or not.
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect email or password!', category='error')
        else:
            flash('Email does not exsit!', category='error')

    return render_template('login.html')


# Sign up page
@auth.route('/sign_up', methods=['Get', 'POST'])
def sign_up():
    if request.method == 'POST':
        # Get data from form.
        username = request.form.get('username')
        email = request.form.get('email')
        pwd_1 = request.form.get('password1')
        pwd_2 = request.form.get('password2')

        # If the user is exist or not.
        email_exists = User.query.filter_by(email=email).first()
        username_exists = User.query.filter_by(username=username).first()

        # Info restrictions
        if username_exists:
            flash('Name is already in use!', category='error')
        elif len(username) <= 2:
            flash('Name must be greater than 2 characters.', category='error')
        elif email_exists:
            flash('Email is already in use!', category='error')
        elif len(email) <= 4:
            flash('Email must be greater than 4 characters.', category='error')
        elif pwd_1 != pwd_2:
            flash('Password don\'t match!', category='error')
        elif len(pwd_1) <= 5:
            flash('Password must be greater than 5 characters.', category='error')
        else:
            new_user = User(username=username, email=email,
                            pwd=generate_password_hash(pwd_1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('User Created!', category='success')
            return redirect(url_for('views.home'))

    return render_template('sign_up.html')


# Logout
@auth.route('/logout')
@login_required  # Access this page if you have logged in.
def logout():
    logout_user()
    return redirect(url_for('views.home'))
