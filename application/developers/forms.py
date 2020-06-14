from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    SubmitField,
    IntegerField,
    SelectField,
    SelectMultipleField,
    widgets,
)
from wtforms.validators import DataRequired
from wtforms.ext.sqlalchemy.fields import QuerySelectMultipleField, QuerySelectField
from application.services.models import Service


def services_query():
    return Service.query.all()


class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


class AddDeveloperForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    experience_level = SelectField(
        "Experience Level: ",
        choices=[(1, "Junior"), (2, "Mid"), (3, "Senior")],
        default=1,
        validators=[DataRequired()],
        coerce=int,
    )
    services = MultiCheckboxField("Services", coerce=int)
    hourly_cost = IntegerField("Cost", validators=[DataRequired()])
    submit = SubmitField("Add Developer")
