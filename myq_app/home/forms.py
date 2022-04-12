from flask import Flask
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired, NumberRange

class QueueForm(FlaskForm):
    name = StringField(
        'Queue name',
        [DataRequired(message="Your queue must have a name")]
    )
    passkey = StringField(
        'Passkey',
        [DataRequired(message="Your queue must have a passkey")]
    )
    max_quantity = IntegerField(
        'Max. members',
        [
            DataRequired(message="You must set the manimum amount of members"),
            NumberRange(
                min=1,
                max=99,
                )
        ]
    )
    submit = SubmitField('Create Queue')

class FindQueueForm(FlaskForm):
    name = StringField(
        'Queue name',
        [DataRequired(message="Please enter your Queue Name")]
    )
    passkey = StringField(
        'Passkey',
        [DataRequired(message="Please enter your queue's passkey")]
    )
    submit = SubmitField('Find Queue')

class EnterQueueForm(FlaskForm):
    name = StringField(
        'Queue name',
        [DataRequired(message="Please enter your Queue Name")]
    )
    submit = SubmitField('Enter Queue')