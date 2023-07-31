from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SubmitField, TextAreaField, FloatField
from wtforms.validators import DataRequired, Length

class CustomerForm(FlaskForm):
    contract_number = StringField('Contract Number', validators=[DataRequired()])
    salesman = StringField('Salesman', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=100)])
    address = StringField('Address', validators=[DataRequired()])
    city = StringField('City', validators=[DataRequired()])
    phone = StringField('Phone', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    date = DateField('Date', validators=[DataRequired()]) 
    email = StringField('Email', validators=[DataRequired()])
    submit = SubmitField('Add Customer')

class JobForm(FlaskForm):
    contract_number = StringField('Contract Number', validators=[DataRequired()])
    salesman = StringField('Salesman', validators=[DataRequired()])
    customer = StringField('Customer', validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired()])
    city = StringField('City', validators=[DataRequired()])
    phone = StringField('Phone', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    date = DateField('Date', validators=[DataRequired()]) 
    email = StringField('Email', validators=[DataRequired()])
    selling_price = StringField('Selling Price', validators=[DataRequired()])
    cost = StringField('Cost', validators=[DataRequired()])
    installer = StringField('Installer', validators=[DataRequired()])
    status = StringField('Status', validators=[DataRequired()])
    notes = StringField('Notes', validators=[DataRequired()])
    submit = SubmitField('Add Job')

class QuoteForm(FlaskForm):
    job_title = StringField('Job Title', validators=[DataRequired(), Length(min=2, max=100)])
    job_description = TextAreaField('Job Description', validators=[DataRequired()])
    quote_amount = FloatField('Quote Amount', validators=[DataRequired()])
    customer_email = StringField('Customer Email', validators=[DataRequired()])
    customer_name = StringField('Customer Name', validators=[DataRequired()])
    customer_address = StringField('Customer Address', validators=[DataRequired()])
    customer_phone = StringField('Customer Phone', validators=[DataRequired()])
    your_email = StringField('Your Email', validators=[DataRequired()])
    your_phone = StringField('Your Phone', validators=[DataRequired()])
    notes = StringField('Notes')
    submit = SubmitField('Generate and Send Quote')

class PromoForm(FlaskForm):
    customer = StringField('Customer', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])

