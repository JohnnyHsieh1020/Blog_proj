from flask import Blueprint, render_template, request
from flask_login import login_required, current_user

views = Blueprint('views', __name__)


# Home page
@views.route('/')
@views.route('/home')
@login_required
def home():
    return render_template('index.html')


# Profile page
@views.route('/profile')
def profile():
    return '<h1>This is profile page</h1>'
