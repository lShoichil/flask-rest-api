from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = "login"


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile("config.py")
    db.init_app(app)

    bcrypt.init_app(app)
    login_manager.init_app(app)

    from ToDo.models import Todo, User, RegisterForm, LoginForm
    from ToDo.routes import main_routes

    app.register_blueprint(main_routes)

    return app
