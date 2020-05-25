from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from application.models import Account


class RegistrationForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    username = StringField(
        "Username", validators=[DataRequired(), Length(min=3, max=20)]
    )
    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField(
        "Confirm Password", validators=[DataRequired(), EqualTo("password")]
    )
    submit = SubmitField("Sign Up")

    def validate_username(self, username):
        account = Account.query.filter_by(username=username.data).first()
        if account:
            raise ValidationError("Username taken. Choose a different one.")

    def validate_email(self, email):
        account = Account.query.filter_by(email=email.data).first()
        if account:
            raise ValidationError("Email taken. Choose a different one.")


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember = BooleanField("Remember Me")
    submit = SubmitField("Login")


class UpdateAccountForm(FlaskForm):
    username = StringField(
        "Username", validators=[DataRequired(), Length(min=2, max=20)]
    )
    email = StringField("Email", validators=[DataRequired(), Email()])
    submit = SubmitField("Update")

    def validate_username(self, username):
        account = Account.query.filter_by(username=username.data).first()
        if account:
            raise ValidationError("Username taken. Choose a different one.")

    def validate_email(self, email):
        account = Account.query.filter_by(email=email.data).first()
        if account:
            raise ValidationError("Email taken. Choose a different one.")


class DeleteAccountForm(FlaskForm):
    delete = SubmitField("Delete")


class OrderForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    requirements = TextAreaField("Requirements", validators=[DataRequired()])
    submit = SubmitField("Order")
