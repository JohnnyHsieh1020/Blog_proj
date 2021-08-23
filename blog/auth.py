# Login, Logout and Signup
from flask import Blueprint, render_template, redirect, url_for, request, flash
from . import db
from .models import User
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os
from datetime import datetime


auth = Blueprint('auth', __name__)


# Login page
@auth.route('/login', methods=['Get', 'POST'])
def login():
    if request.method == 'POST':
        # Get data from form.
        email = request.form.get('email')
        pwd = request.form.get('password')

        # Check login info
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

    return render_template('login.html', user=current_user)


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
            flash('Name is already in used!', category='error')
        elif email_exists:
            flash('Email is already in used!', category='error')
        elif pwd_1 != pwd_2:
            flash('Password don\'t match!', category='error')
        else:
            new_user = User(username=username, email=email,
                            pwd=generate_password_hash(pwd_1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('User Created!', category='success')
            return redirect(url_for('views.home'))

    return render_template('sign_up.html', user=current_user)


# Profile Page
@auth.route('/profile', methods=['Get', 'POST'])
@login_required  # Access this page if you have logged in.
def profile():
    user = User.query.filter_by(id=current_user.id).first()

    if user:
        if request.method == 'POST':
            # Get new info
            name = request.form['name'] 
            pwd_1 = request.form['password1']
            pwd_2 = request.form['password2']
            
            if current_user.username != name:
                username_exists = User.query.filter_by(username=name).first()
                if username_exists:
                    flash('Name is already in used!', category='error')
                    return render_template('profile.html', user=current_user, username=current_user.username)
                elif pwd_1 == '' and pwd_2 == '':
                    # Update data
                    user.username = name
                    db.session.commit()
                    
                    # Show message
                    flash('Saved!', category='success')
                elif pwd_1 != pwd_2:
                    flash('Password don\'t match!', category='error')
                    return render_template('profile.html', user=current_user, username=current_user.username)
                else:
                    # Update data
                    user.username = name
                    user.pwd = generate_password_hash(
                        pwd_1, method='sha256')
                    db.session.commit()

                    # Show message
                    flash('Saved!', category='success')
                # return render_template('profile.html', user=current_user, username=name)
            else:
                if pwd_1 == '' and pwd_2 == '':
                    flash('Please make some changes!', category='error')
                elif pwd_1 != pwd_2:
                    flash('Password don\'t match!', category='error')
                    return render_template('profile.html', user=current_user, username=current_user.username)
                else:
                    # Update data
                    user.username = name
                    user.pwd = generate_password_hash(
                        pwd_1, method='sha256')
                    db.session.commit()

                    # Show message
                    flash('Saved!', category='success')
            return render_template('profile.html', user=current_user, username=name)
        else:
            return render_template('profile.html', user=current_user, username=current_user.username)


# Update Photo
@auth.route('/update_photo', methods=['POST'])
@login_required  # Access this page if you have logged in.
def update_photo():
    user = User.query.filter_by(id=current_user.id).first()
    file = request.files['image']

    if not file :
        flash('Please Upload A Photo!', category='error')
    else:
        image_name = datetime.now().strftime('%Y%m%d%H%M%S') + secure_filename(file.filename)
        file.save(os.path.join('blog/static/profile_images', image_name))
        if user.image_name != 'default.png':
            os.remove(f"blog/static/profile_images/{user.image_name}")
            user.image_name = image_name
            db.session.commit()
      
        user.image_name = image_name
        db.session.commit()
        flash('Saved!', category='success')

    return render_template('profile.html', user=current_user, username=current_user.username)


# Logout
@auth.route('/logout')
@login_required  # Access this page if you have logged in.
def logout():
    logout_user()
    return redirect(url_for('views.home'))
