from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, SelectField
from wtforms.validators import DataRequired
from wtforms.ext.sqlalchemy.fields import QuerySelectMultipleField, QuerySelectField
from application.services.models import Service


def services_query():
    return Service.query.all()


class AddDeveloperForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    experience_level = SelectField(
        "Experience Level: ",
        choices=[(1, "Junior"), (2, "Mid"), (3, "Senior")],
        default=1,
        validators=[DataRequired()],
        coerce=int,
    )
    services = QuerySelectMultipleField(
        default=["1", "2"],
        query_factory=services_query,
        get_label="name",
        allow_blank=False,
    )
    hourly_cost = IntegerField("Cost", validators=[DataRequired()])
    submit = SubmitField("Add Developer")
