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
from ToDo.models import User, Todo, LoginForm, RegisterForm

main_routes = Blueprint("main", __name__, template_folder="templates")


@main_routes.route("/")
def home():
    return render_template("home.html")


@main_routes.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.email.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for("main.go_todo"))
    return render_template("login.html", form=form)


@main_routes.route("/todo_lists", methods=["GET", "POST"])
@login_required
def todo_lists():
    return render_template("todo.html")


@main_routes.route("/logout", methods=["GET", "POST"])
@login_required
def logout():
    logout_user()
    return redirect(url_for("main.login"))


@main_routes.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        new_user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for("main.login"))

    return render_template("register.html", form=form)


@main_routes.route("/todo")
def go_todo():
    try:
        todo_list = Todo.query.filter_by(user_id=current_user.id).all()
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
    todo = Todo.query.filter_by(user_id=current_user.id, id=todo_id).first()
    todo.complete = not todo.complete
    db.session.commit()
    return redirect(url_for("main.go_todo"))


@main_routes.route("/todo/delete/<int:todo_id>")
def delete(todo_id):
    todo = Todo.query.filter_by(user_id=current_user.id, id=todo_id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("main.go_todo"))


@main_routes.route('/confirm_email', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return '<form action="/confirm_email" method="POST"><input name="email"><input type="submit"></form>'

    email = request.form['email']
    token = s.dumps(email, salt='email-confirm')

    msg = Message('Confirm Email', sender='teamsuppormail@yandex.ru', recipients=[email])

    link = url_for('main.confirm_email', token=token, _external=True)

    msg.body = 'Your link is {}'.format(link)

    mail.send(msg)

    return '<h1>The email you entered is {}. The token is {}</h1>'.format(email, token)


@main_routes.route('/confirm_email/<token>')
def confirm_email(token):
    try:
        email = s.loads(token, salt='email-confirm', max_age=3600)
    except SignatureExpired:
        return '<h1>The token is expired!</h1>'
    return '<h1>The token works!</h1>'
