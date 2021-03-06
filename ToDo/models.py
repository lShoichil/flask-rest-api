from flask_login import UserMixin
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError

from ToDo import db, login_manager


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    email = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=True)
    admin = db.Column(db.Integer, nullable=False)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    title = db.Column(db.String(100))
    complete = db.Column(db.Boolean)

    def __iter__(self):
        return iter(self._values)


class RegisterForm(FlaskForm):
    username = StringField(
        validators=[InputRequired(), Length(min=4, max=80)],
        render_kw={"placeholder": "Username"},
    )

    email = StringField(
        validators=[InputRequired(), Length(min=5, max=80)],
        render_kw={"placeholder": "email"},
    )

    password = PasswordField(
        validators=[InputRequired(), Length(min=8, max=80)],
        render_kw={"placeholder": "Password"},
    )

    submit = SubmitField("Register")

    def validate_check(self, username, email):
        existing_user_username = User.query.filter_by(username=username.data).first()
        existing_user_email = User.query.filter_by(email=email.data).first()
        if existing_user_username or existing_user_email:
            raise ValidationError(
                "That username or email already exists. Please choose a different one."
            )


class LoginForm(FlaskForm):
    email = StringField(
        validators=[InputRequired(), Length(min=5, max=80)],
        render_kw={"placeholder": "email"},
    )

    password = PasswordField(
        validators=[InputRequired(), Length(min=8, max=80)],
        render_kw={"placeholder": "Password"},
    )

    submit = SubmitField("Login")


class AdminForm(FlaskForm):
    email = StringField(
        validators=[InputRequired(), Length(min=5, max=80)],
        render_kw={"placeholder": "email"},
    )

    password = PasswordField(
        validators=[InputRequired(), Length(min=8, max=80)],
        render_kw={"placeholder": "Password"},
    )

    submit = SubmitField("Update to admin")


class ChangePasswordForm(FlaskForm):
    password = PasswordField(
        validators=[InputRequired(), Length(min=8, max=80)],
        render_kw={"placeholder": "Password"},
    )

    submit = SubmitField("Change your password")
