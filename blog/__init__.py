from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate


db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'blogflask202166666666'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost/postgres'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    migrate = Migrate(app, db)

    # Register Bluepirnt
    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    # Create DB
    from .models import User, Post, Comment, Like

    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'  # If the user has not logged in.
    login_manager.init_app(app)

    # Function for login_manager to find user model when it logs something in.
    @login_manager.user_loader
    def load_user(id):
        # Get user_id from session and get info from User table.
        return User.query.get(int(id))

    return app


def create_database(app):
    db.create_all(app=app)
    print('Database created!')
