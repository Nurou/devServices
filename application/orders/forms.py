from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired


class OrderForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    requirements = TextAreaField("Requirements", validators=[DataRequired()])
    submit = SubmitField("Order")
