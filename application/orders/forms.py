from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    SubmitField,
    TextAreaField,
    SelectMultipleField,
    widgets,
)
from wtforms.validators import DataRequired, Length, ValidationError
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from application.services.models import Service
from application.developers.models import Developer


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

    def validate_assignment(self, developers):
        for d in developers:
            if Developer.is_developer_available(d.id) == False:
                raise ValidationError(
                    "One of the developers cannot be assigned to the order. They have either already been assigned to the order, or are too busy."
                )
