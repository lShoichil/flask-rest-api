import datetime
import os
import uuid
from functools import wraps
import jwt
from dotenv import load_dotenv
from flask import request, jsonify, make_response
from werkzeug.security import generate_password_hash, check_password_hash

from app import app
from models import *


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if "x-access-token" in request.headers:
            token = request.headers["x-access-token"]

        if not token:
            return jsonify({"message": "Token is missing!"}), 401

        try:
            data = jwt.decode(token, app.config["SECRET_KEY"], algorithms=["HS256"])
            current_user = User.query.filter_by(public_id=data["public_id"]).first()
        except:
            return jsonify({"message": "Token is invalid!"}), 401

        return f(current_user, *args, **kwargs)

    return decorated


dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(dotenv_path)


@app.route("/")
def hello():
    return "<h1>Hello There!</h1>"


@app.route("/health/", methods=["GET"])
def health():
    return jsonify({"env": os.environ["SERVER_ENV"]})


@app.route("/login")
def login():
    auth = request.authorization

    if not auth or not auth.username or not auth.password:
        return make_response(
            "Could not verify",
            401,
            {"WWW-Authenticate": "Basic realm=" '"Login required!"'},
        )

    user = User.query.filter_by(name=auth.username).first()

    if not user:
        return make_response(
            "Could not verify",
            401,
            {"WWW-Authenticate": "Basic realm=" '"Login required!"'},
        )

    if check_password_hash(user.password, auth.password):
        token = jwt.encode(
            {
                "public_id": user.public_id,
                "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            },
            app.config["SECRET_KEY"],
            algorithm="HS256",
        )
        return jsonify({"token": token})

    return make_response(
        "Could not verify", 401, {"WWW-Authenticate": 'Basic realm="Login required!"'}
    )


@app.route("/user", methods=["GET", "POST"])
@app.route("/user/<public_id>", methods=["GET", "PUT", "DELETE"])
@token_required
def work_to_user(public_id=None, current_user=None):
    # Вывод всех пользователей, если вы администратор
    if request.method == "GET" and public_id is None:
        if not current_user.admin:
            return jsonify({"message": "Cannot perform that function!"})

        users = User.query.all()

        output = []

        for user in users:
            user_data = {
                "public_id": user.public_id,
                "name": user.name,
                "password": user.password,
                "admin": user.admin,
            }
            output.append(user_data)

        return jsonify({"users": output})

    # Создание пользователя
    if request.method == "POST":
        data = request.get_json()

        hashed_password = generate_password_hash(data["password"], method="sha256")

        new_user = User(
            public_id=str(uuid.uuid4()),
            name=data["name"],
            password=hashed_password,
            admin=False,
        )
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"message": "New user created!"})

    # Получение одного пользователя
    if request.method == "GET" and public_id is not None:
        user = User.query.filter_by(public_id=public_id).first()

        if not user:
            return jsonify({"message": "No user found!"})

        user_data = {
            "public_id": user.public_id,
            "name": user.name,
            "password": user.password,
            "admin": user.admin,
        }

        return jsonify({"user": user_data})

    # Дать права администратора
    if request.method == "PUT":
        user = User.query.filter_by(public_id=public_id).first()

        if not user:
            return jsonify({"message": "No user found!"})

        user.admin = True
        db.session.commit()

        return jsonify({"message": "The user has been promoted!"})

    # Удаление пользователя
    if request.method == "DELETE":
        user = User.query.filter_by(public_id=public_id).first()

        if not user:
            return jsonify({"message": "No user found!"})
        db.session.delete(user)
        db.session.commit()

        return jsonify({"message": "The user has been deleted!"})


@app.route("/todo", methods=["GET", "POST"])
@app.route("/todo/<todo_id>", methods=["GET", "PUT", "DELETE"])
@token_required
def todo_list(current_user=None, todo_id=None):
    # Вывод всех задач
    if request.method == "GET" and todo_id is None:
        todos = Todo.query.filter_by(user_id=current_user.id).all()

        output = []

        for todo in todos:
            todo_data = {"id": todo.id, "text": todo.text, "complete": todo.complete}
            output.append(todo_data)

        return jsonify({"todos": output})
    # Вывод одной задачи
    if request.method == "GET" and todo_id is not None:
        todo = Todo.query.filter_by(id=todo_id, user_id=current_user.id).first()

        if not todo:
            return jsonify({"message": "No todo found"})

        todo_data = {"id": todo.id, "text": todo.text, "complete": todo.complete}

        return jsonify(todo_data)
    # Создание задачи
    if request.method == "POST":
        data = request.form["text"]

        new_todo = Todo(text=data, complete=False, user_id=current_user.id)
        db.session.add(new_todo)
        db.session.commit()

        return jsonify({"message": "Todo created!"})
    # Изменить состояние задачи
    if request.method == "PUT":
        todo = Todo.query.filter_by(id=todo_id, user_id=current_user.id).first()

        if not todo:
            return jsonify({"message": "No todo found"})

        todo.complete = True
        db.session.commit()

        return jsonify({"message": "Todo item has been completed!"})
    # Удаление задачи
    if request.method == "DELETE":
        todo = Todo.query.filter_by(id=todo_id, user_id=current_user.id).first()

        if not todo:
            return jsonify({"message": "No todo found"})

        db.session.delete(todo)
        db.session.commit()

        return jsonify({"message": "Todo item deleted!"})