from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, TextAreaField, SubmitField, DateField
from wtforms.validators import DataRequired, Optional

class LabOrderForm(FlaskForm):
    test_type = SelectField('Test Type', choices=[
        ('Complete Blood Count (CBC)', 'Complete Blood Count (CBC)'),
        ('Basic Metabolic Panel (BMP)', 'Basic Metabolic Panel (BMP)'),
        ('Comprehensive Metabolic Panel (CMP)', 'Comprehensive Metabolic Panel (CMP)'),
        ('Lipid Panel', 'Lipid Panel'),
        ('Thyroid Stimulating Hormone (TSH)', 'Thyroid Stimulating Hormone (TSH)'),
        ('Hemoglobin A1C', 'Hemoglobin A1C'),
        ('Urinalysis', 'Urinalysis'),
        ('Other', 'Other')
    ], validators=[DataRequired()])
    notes = TextAreaField('Notes', validators=[Optional()])
    submit = SubmitField('Order Lab Test')


class LabResultForm(FlaskForm):
    result_data = TextAreaField('Result Data', validators=[DataRequired()])
    submit = SubmitField('Submit Lab Result')


class LabOrderSearchForm(FlaskForm):
    patient_name = StringField('Patient Name', validators=[Optional()])
    test_type = SelectField('Test Type', choices=[
        ('', 'All Test Types'),
        ('Complete Blood Count (CBC)', 'Complete Blood Count (CBC)'),
        ('Basic Metabolic Panel (BMP)', 'Basic Metabolic Panel (BMP)'),
        ('Comprehensive Metabolic Panel (CMP)', 'Comprehensive Metabolic Panel (CMP)'),
        ('Lipid Panel', 'Lipid Panel'),
        ('Thyroid Stimulating Hormone (TSH)', 'Thyroid Stimulating Hormone (TSH)'),
        ('Hemoglobin A1C', 'Hemoglobin A1C'),
        ('Urinalysis', 'Urinalysis'),
        ('Other', 'Other')
    ], validators=[Optional()], default='')
    ordered_by = StringField('Ordering Physician', validators=[Optional()])
    start_date = DateField('Start Date', validators=[Optional()])
    end_date = DateField('End Date', validators=[Optional()])
    status = SelectField('Status', choices=[
        ('all', 'All'),
        ('Ordered', 'Pending'),
        ('Completed', 'Completed')
    ], validators=[Optional()], default='Ordered')
    submit = SubmitField('Search')