from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from application.services.models import Service


def service_query():
    return Service.query.all()


class OrderForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired(), Length(min=3, max=30)])
    requirements = TextAreaField(
        "Requirements", validators=[DataRequired(), Length(min=3, max=500)]
    )
    service = QuerySelectField(
        query_factory=service_query, allow_blank=False, get_label="name"
    )
    submit = SubmitField("Order")
