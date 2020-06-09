from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length


class OrderForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired(), Length(min=3, max=30)])
    requirements = TextAreaField(
        "Requirements", validators=[DataRequired(), Length(min=3, max=500)]
    )
    submit = SubmitField("Order")
