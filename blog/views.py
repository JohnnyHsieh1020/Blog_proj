from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from datetime import datetime
from .models import User, Post, Comment, Like
from . import db
import os


views = Blueprint("views", __name__)


# Home Page
@views.route("/")
@views.route("/home")
@login_required  # Access this page if you have logged in.
def home():
    # Get all the posts
    posts = Post.query.all()
    return render_template("index.html", user=current_user, posts=posts)


# Create Post Page
@views.route("/create_post", methods=["Get", "POST"])
@login_required  # Access this page if you have logged in.
def create_post():
    if request.method == "POST":
        # Get data from form.
        content = request.form.get("content")
        file = request.files["image"]

        if not content:
            flash("Post Cannot Be Empty!", category="error")
        elif file.filename == "":
            post = Post(content=content, image_name=None, author_id=current_user.id)

            db.session.add(post)
            db.session.commit()

            flash("Post Created!", category="success")
            return redirect(url_for("views.home"))
        else:
            image_name = datetime.now().strftime("%Y%m%d%H%M%S") + secure_filename(
                file.filename
            )
            file.save(os.path.join("blog/static/images", image_name))
            post = Post(
                content=content, image_name=image_name, author_id=current_user.id
            )

            db.session.add(post)
            db.session.commit()

            flash("Post Created!", category="success")
            return redirect(url_for("views.home"))

    return render_template("create_post.html", user=current_user)


# View User's Posts
@views.route("/posts/<username>")
@login_required  # Access this page if you have logged in.
def posts(username):
    # Search the posts of the given user.
    user = User.query.filter_by(username=username).first()

    if not user:
        flash(f"User {username} Not exist!", category="error")
        return redirect(url_for("views.home"))

    posts = user.posts

    return render_template(
        "posts.html", user=current_user, username=username, posts=posts
    )


# Create Comment
@views.route("/create_comment/<post_id>", methods=["POST"])
@login_required  # Access this page if you have logged in.
def create_comment(post_id):
    # Get data from form.
    content = request.form.get("comment")

    if not content:
        flash("Comment cannot be empty!", category="error")
    else:
        post = Post.query.filter_by(id=post_id)

        if not post:
            flash("Post does not exist!", category="error")
        else:
            comment = Comment(
                content=content, author_id=current_user.id, post_id=post_id
            )
            db.session.add(comment)
            db.session.commit()

    return redirect(url_for("views.home"))


# Delete Post
@views.route("/delete_post/<post_id>")
@login_required  # Access this page if you have logged in.
def delete_post(post_id):
    post = Post.query.filter_by(id=post_id).first()

    if not post:
        flash("Post does not exist!", category="error")
    elif current_user.id != post.author_id:
        flash("Permission Denied!", category="error")
    else:
        image_name = post.image_name

        if image_name is None:
            db.session.delete(post)
            db.session.commit()
        else:
            os.remove(f"blog/static/images/{image_name}")
            db.session.delete(post)
            db.session.commit()

        flash("Post Deleted!", category="success")

    return redirect(url_for("views.home"))


# Delete Comment
@views.route("/delete_comment/<comment_id>")
@login_required  # Access this page if you have logged in.
def delete_comment(comment_id):
    comment = Comment.query.filter_by(id=comment_id).first()

    if not comment:
        flash("Comment does not exist!", category="error")
    elif (
        current_user.id != comment.author_id
        and current_user.id != comment.post.author_id
    ):
        flash("Permission Denied!", category="error")
    else:
        db.session.delete(comment)
        db.session.commit()

    return redirect(url_for("views.home"))


# Like Post
@views.route("/like_post/<post_id>", methods=["POST"])
@login_required  # Access this page if you have logged in.
def like_post(post_id):
    post = Post.query.filter_by(id=post_id).first()
    like = Like.query.filter_by(author_id=current_user.id, post_id=post_id).first()

    if not post:
        return jsonify({"error": "Post does not exist."}, 400)
    elif like:
        db.session.delete(like)
        db.session.commit()
    else:
        like = Like(author_id=current_user.id, post_id=post_id)
        db.session.add(like)
        db.session.commit()

    # x.author_id means Like.author_id
    return jsonify(
        {
            "sumLikes": len(post.likes),
            "likeCheck": current_user.id in map(lambda x: x.author_id, post.likes),
        }
    )
