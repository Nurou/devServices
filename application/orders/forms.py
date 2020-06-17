from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    SubmitField,
    TextAreaField,
    SelectMultipleField,
    widgets,
)
from wtforms.validators import DataRequired, Length
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from application.services.models import Service


def service_query():
    return Service.query.filter().order_by(Service.name)


class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


class OrderForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired(), Length(min=3, max=30)])
    requirements = TextAreaField(
        "Requirements", validators=[DataRequired(), Length(min=3, max=500)]
    )
    service = QuerySelectField(
        query_factory=service_query, allow_blank=False, get_label="name"
    )
    submit = SubmitField("Order")


class AssignDevsToOrderForm(FlaskForm):
    developers = MultiCheckboxField("Developers", coerce=int)
    submit = SubmitField("Assign Selected")
