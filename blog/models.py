from . import db  # from __init__ import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True)
    email = db.Column(db.String(150), unique=True)
    pwd = db.Column(db.String(150))
    image_name = db.Column(db.String(128), nullable=False, default='default.png')
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    posts = db.relationship('Post', backref='user',
                            cascade='all, delete, delete-orphan')
    comments = db.relationship(
        'Comment', backref='user', cascade='all, delete, delete-orphan')
    likes = db.relationship(
        'Like', backref='user', cascade='all, delete, delete-orphan')

    def __init__(self, username, email, pwd):
        self.username = username
        self.email = email
        self.pwd = pwd


class Post(db.Model):
    __tablename__ = 'post'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    image_name = db.Column(db.String(128), nullable=True)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    # F-key
    author_id = db.Column(db.Integer, db.ForeignKey(
        'user.id', ondelete="CASCADE"), nullable=False)
    comments = db.relationship(
        'Comment', backref='post', cascade='all, delete, delete-orphan')
    likes = db.relationship(
        'Like', backref='post', cascade='all, delete, delete-orphan')

    def __init__(self, content, image_name, author_id):
        self.content = content
        self.image_name = image_name
        self.author_id = author_id


class Comment(db.Model):
    __tablename__ = 'comment'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    # F-key
    author_id = db.Column(db.Integer, db.ForeignKey(
        'user.id', ondelete="CASCADE"), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey(
        'post.id', ondelete="CASCADE"), nullable=False)

    def __init__(self, content, author_id, post_id):
        self.content = content
        self.author_id = author_id
        self.post_id = post_id


class Like(db.Model):
    __tablename__ = 'like'
    id = db.Column(db.Integer, primary_key=True)
    # F-key
    author_id = db.Column(db.Integer, db.ForeignKey(
        'user.id', ondelete="CASCADE"), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey(
        'post.id', ondelete="CASCADE"), nullable=False)

    def __init__(self, author_id, post_id):
        self.author_id = author_id
        self.post_id = post_id
