from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired


class AddServiceForm(FlaskForm):
    name = StringField("Title", validators=[DataRequired()])
    submit = SubmitField("Add Service")
