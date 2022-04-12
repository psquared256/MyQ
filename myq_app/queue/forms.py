from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class MemberForm(FlaskForm):
    name = StringField(
        'Full Name',
        [DataRequired(message="You must enter a name to receive a number")]
    )
    submit = SubmitField('Get your number')