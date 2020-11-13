from flask import Blueprint
from flask.helpers import flash
from flask import render_template, redirect, url_for, request
from main.posts.forms import PostForm
from main import db
from main.models import Posts
from flask_login import current_user, login_required
posts = Blueprint('posts',__name__)

@posts.route("/posts")
@login_required
def readblog():
    if current_user.is_authenticated:
        page = request.args.get('page', 1, type=int)
        posts = Posts.query.order_by(Posts.post_id.desc()).paginate(page=page, per_page=5)
        return render_template("readblog.html",posts=posts)
    else:
        return "<h2>Not Authorized!</h2>"

@posts.route("/post/new", methods=["GET","POST"])
@login_required
def writeblog():
    form=PostForm()
    if request.method == "GET":
        if current_user.is_authenticated:
            return render_template("postcontent.html", form=form)
        else:
            return "<h2>Not Authorized!</h2>"
    else:
        if form.validate_on_submit():
            post = Posts(title=form.title.data, content=form.content.data, author=current_user.username)
            db.session.add(post)
            db.session.commit()
            flash('Posted Successfully!','success')
            return redirect(url_for('posts.readblog'))
        else:
            return render_template("postcontent.html", form=form)

@posts.route("/posts/delete/<int:post_id>", methods=["POST"])
@login_required
def delete_blog(post_id):
    if request.method == "POST":
        if current_user.is_authenticated:
            post = Posts.query.filter_by(post_id=post_id).first()
            if post.author == current_user.username:
                db.session.delete(post)
                db.session.commit()
                flash('Post deleted!','success')
                return redirect(url_for('posts.readblog'))
        else:
            return "<h2>Not Authorized!</h2>"

@posts.route("/posts/update/<int:post_id>", methods=["GET","POST"])
@login_required
def update_blog(post_id):
    form=PostForm()
    if request.method == "POST":
        if current_user.is_authenticated:
            post = Posts.query.filter_by(post_id=post_id).first()
            if form.validate_on_submit():
                post.title = form.title.data
                post.content = form.content.data
                db.session.commit()
                flash('Updated Successfully!','success')
                return redirect(url_for('posts.readblog'))
            form.title.data = post.title
            form.content.data = post.content
            return render_template("postcontent.html", form=form)
        else:
            return "<h2>Not Authorized!</h2>"