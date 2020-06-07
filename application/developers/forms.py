from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired


class AddDeveloperForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    experience_level = IntegerField("Experience", validators=[DataRequired()])
    hourly_cost = IntegerField("Cost", validators=[DataRequired()])
    submit = SubmitField("Add Developer")
