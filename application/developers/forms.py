from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, SelectField
from wtforms.validators import DataRequired


class AddDeveloperForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    experience_level = SelectField(
        "Experience Level: ",
        choices=[(1, "Junior"), (2, "Mid"), (3, "Senior")],
        default=1,
        validators=[DataRequired()],
        coerce=int,
    )
    hourly_cost = IntegerField("Cost", validators=[DataRequired()])
    submit = SubmitField("Add Developer")
