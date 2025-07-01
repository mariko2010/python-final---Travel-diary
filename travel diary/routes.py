from flask import  render_template, redirect, flash, request
from forms import BlogForm, RegisterForm, LoginForm
from ext import app, db, login_manager
from models import Blog, User
from os import path
from flask_login import login_user, logout_user, login_required, current_user
@app.route('/')
def home():
    return render_template('index.html')


@app.route('/blogs')
def blogs():
    blogs=Blog.query.all()
    return render_template('blogs.html', blogs=blogs)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route("/user/<username>")
@login_required
def user_profile(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template("profile.html", user=user)

@app.route("/logout")
def logout():
    logout_user()
    return redirect("/")

from flask_login import current_user, login_required

@app.route("/profile")
@login_required
def profile():
    user = current_user
    print("➡ current_user.id:", user.id)
    user_blogs = Blog.query.filter_by(user_id=user.id).all()
    all_blogs = Blog.query.all()
    return render_template("profile.html", user=user, blogs=user_blogs)


@app.route('/register', methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        new_user = User(username=form.username.data, password=form.password.data)
        new_user.add()
        return redirect("/")
    return render_template("register.html", form=form)

@app.route("/login", methods=["GET","POST"])
def login():
    form=LoginForm()
    if form.validate_on_submit():
        user = User.query.filter(User.username == form.username.data).first()
        check_pass=user.check_password(form.password.data)
        if user and check_pass:
            login_user(user)
            return redirect("/")
    return render_template("login.html", form=form)

@app.route("/openblog/<int:blog_id>")
def blog_details(blog_id):
    blog=Blog.query.get(blog_id)
    return render_template("openblog.html", blog=blog)

@app.route("/addblog", methods=["GET", "POST"])
@login_required
def add_blog():
    form = BlogForm()  # ჯერ form ცვლადი შექმენი
    if form.validate_on_submit():
        image = form.image.data
        directory = path.join(app.root_path, "static", "images", image.filename)
        image.save(directory)

        new_blog = Blog(
            name=form.name.data,
            description=form.description.data,
            image=image.filename,
            user_id=current_user.id
        )

        new_blog.add()

        flash("ბლოგი წარმატებით დაემატა!", "success")
        return redirect("/blogs")

    # მხოლოდ ბოლოს დაბრუნება
    return render_template("addblog.html", form=form)


@app.route("/delete_blog/<int:blog_id>")
def delete_blog(blog_id):
    blog=Blog.query.get(blog_id)
    Blog.delete(blog)
    return redirect("/blogs")

@app.route("/edit_blog/<int:blog_id>", methods=["GET", "POST"])
def edit_blog(blog_id):
    blog = Blog.query.get_or_404(blog_id)
    form = BlogForm()

    if form.validate_on_submit():
        # ფორმიდან ვიღებთ მონაცემს და ვანახლებთ პროდუქტს
        blog.name = form.name.data
        blog.description = form.description.data
        image = form.image.data
        directory = path.join(app.root_path, "static", "images", image.filename)
        image.save(directory)
        blog.image = image.filename
        db.session.commit()
        return redirect("/blogs")  # გადამისამართება წარმატების შემთხვევაში

    elif request.method == "GET":
        # GET-ზე ფორმის წინასწარი შევსება
        form.name.data = blog.name
        form.description.data = blog.description

    return render_template("editblog.html", form=form)


blogs = []
