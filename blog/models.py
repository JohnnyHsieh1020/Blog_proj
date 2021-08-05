from . import db  # from __init__ import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True)
    email = db.Column(db.String(150), unique=True)
    pwd = db.Column(db.String(150))
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
