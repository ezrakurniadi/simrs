from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, DateTimeField, SubmitField
from wtforms.validators import DataRequired, Optional

class ClinicalNoteForm(FlaskForm):
    date = DateTimeField('Date', validators=[DataRequired()], format='%Y-%m-%d %H:%M:%S')
    note_type = SelectField('Note Type', choices=[
        ('Progress Note', 'Progress Note'),
        ('Consultation Note', 'Consultation Note'),
        ('Discharge Summary', 'Discharge Summary'),
        ('Operative Report', 'Operative Report'),
        ('Other', 'Other')
    ], validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Save Clinical Note')