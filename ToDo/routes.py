from flask import flash, redirect, render_template, request, url_for, Blueprint
from flask_login import (
    current_user,
    login_required,
    login_user,
    logout_user,
)
from flask_mail import Message
from itsdangerous import SignatureExpired

from ToDo import bcrypt, db, mail
from ToDo.config import s
from ToDo.models import (
    User,
    Todo,
    LoginForm,
    RegisterForm,
    AdminForm,
    ChangePasswordForm,
)

main_routes = Blueprint("main", __name__, template_folder="templates")


@main_routes.route("/")
def home():
    return render_template("home.html")


@main_routes.route("/admin_page", methods=["GET", "POST"])
@login_required
def go_admin_page():
    if current_user.admin:
        user_list = User.query.filter_by().all()
        return render_template("admin_page.html", user_list=user_list)
    else:
        return redirect(url_for("main.login"))


@main_routes.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for("main.go_todo"))
    return render_template("login.html", form=form)


@main_routes.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if not user:
            hashed_password = bcrypt.generate_password_hash(form.password.data)
            new_user = User(
                username=form.username.data,
                email=form.email.data,
                password=hashed_password,
                admin=0,
            )
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for("main.login"))

    return render_template("register.html", form=form)


@main_routes.route("/logout", methods=["GET", "POST"])
@login_required
def logout():
    logout_user()
    return redirect(url_for("main.login"))


@main_routes.route("/update_to_admin", methods=["GET", "POST"])
def update_to_admin():
    form = AdminForm()
    user = User.query.filter_by(email=form.email.data).first()
    if user:
        user.admin = not user.admin
        db.session.commit()
        return "<h1>User update!</h1>"

    return render_template("update_to_admin.html", form=form)


@main_routes.route("/admin_page/delete/<int:user_id>")
def delete_user(user_id):
    if user_id != current_user.id:
        user = User.query.filter_by(id=user_id).first()
        todo_list = Todo.query.filter_by(user_id=user.id).all()
        for todo in todo_list:
            db.session.delete(todo)
        db.session.delete(user)
        db.session.commit()
    return redirect(url_for("main.go_admin_page"))


@main_routes.route("/todo")
def go_todo():
    try:
        if not current_user.admin:
            todo_list = Todo.query.filter_by(user_id=current_user.id).all()
        elif current_user.admin:
            todo_list = Todo.query.filter_by().all()
        return render_template("todo.html", todo_list=todo_list)
    except AttributeError:
        flash("Сначала залогинься!", "success")
        return redirect(url_for("main.login"))


@main_routes.route("/todo/add", methods=["POST"])
def add():
    title = request.form.get("title")
    new_todo = Todo(title=title, complete=False, user_id=current_user.id)
    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for("main.go_todo"))


@main_routes.route("/todo/update/<int:todo_id>")
def update(todo_id):
    if not current_user.admin:
        todo = Todo.query.filter_by(user_id=current_user.id, id=todo_id).first()
    elif current_user.admin:
        todo = Todo.query.filter_by(id=todo_id).first()
    todo.complete = not todo.complete
    db.session.commit()
    return redirect(url_for("main.go_todo"))


@main_routes.route("/todo/delete/<int:todo_id>")
def delete(todo_id):
    if not current_user.admin:
        todo = Todo.query.filter_by(user_id=current_user.id, id=todo_id).first()
    elif current_user.admin:
        todo = Todo.query.filter_by(id=todo_id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("main.go_todo"))


@main_routes.route("/change_password", methods=["GET", "POST"])
def prechange_password():
    try:
        user = User.query.filter_by(id=current_user.id).first()
        if request.method == "GET":
            return '<form action="/change_password" method="POST"><input name="email"><input type="submit"></form>'
        email = request.form["email"]
        token = s.dumps(email, salt="email-confirm")
        msg = Message(
            "Confirm Email", sender="teamsuppormail@yandex.ru", recipients=[email]
        )
        link = url_for("main.change_password", token=token, _external=True)
        msg.body = "Your link is {}".format(link)
        mail.send(msg)
        return "<h1>The email you entered is {}. The token is {}</h1>".format(
            email, token
        )
    except AttributeError:
        return redirect(url_for("main.login"))


@main_routes.route("/change_your_new_password/<token>", methods=["GET", "POST"])
def change_password(token):
    form = ChangePasswordForm(request.form)
    try:
        email = s.loads(token, salt="email-confirm", max_age=3600)
    except SignatureExpired:
        return "<h1>The token is expired!</h1>"
    user = User.query.filter_by(email=email).first()
    if user and form.password.data:
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        user.password = hashed_password
        db.session.commit()
        return redirect(url_for("main.logout"))

    return render_template("change_your_new_password.html", form=form)
