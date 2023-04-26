from flask_wtf import FlaskForm
from wtforms import StringField, DateField, FileField, TextAreaField, validators
from wtforms import BooleanField, SubmitField
from wtforms.validators import DataRequired


class JobForm(FlaskForm):
    job = StringField('Title of activity', validators=[DataRequired()])
    collaborators = TextAreaField('Text', [validators.length(max=90)])
    start_date = DateField('Start date')
    finished_date = DateField('End date')
    is_finished = BooleanField("IS FINISHED?")
    submit = SubmitField('Save')