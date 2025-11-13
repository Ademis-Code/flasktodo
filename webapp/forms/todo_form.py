from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import InputRequired, Length


class TaskForm(FlaskForm):
    taskName = StringField('Nama Tugas', validators=[InputRequired(), Length(min=1, max=50)])
    submit = SubmitField('Submit')
