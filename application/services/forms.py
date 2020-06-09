from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length


class AddServiceForm(FlaskForm):
    name = StringField("Title", validators=[DataRequired(), Length(min=3, max=30)])
    submit = SubmitField("Add Service")
