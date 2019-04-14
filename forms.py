from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, NumberRange


class UserRegistrationForm(FlaskForm): # inherits from FlaskForm
    firstName = StringField('First Name', validators=[DataRequired()])
    lastName = StringField('Last Name', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    email = StringField('Email', validators=[DataRequired(), Email()])
    emails = []
    submit = SubmitField('Sign Up')

class VisitorRegistrationForm(FlaskForm): # inherits from FlaskForm
    firstName = StringField('First Name', validators=[DataRequired()])
    lastName = StringField('Last Name', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    email = StringField('Email', validators=[DataRequired(), Email()])
    emails = []
    submit = SubmitField('Sign Up')

class EmployeeRegistrationForm(FlaskForm): # inherits from FlaskForm
    firstName = StringField('First Name', validators=[DataRequired()])
    lastName = StringField('Last Name', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    userType = SelectField(
        'User Type',
        choices=[('manager', 'Manager'), ('staff', 'Staff')]
    )
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    phone = IntegerField('Phone', validators=[DataRequired(), NumberRange(min=10, max=10, message="Phone number must be 10 digits.")])
    address = StringField('Address', validators=[DataRequired()])
    city = StringField('City', validators=[DataRequired()])
    STATE_ABBREV = ('AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA', 
                'HI', 'ID', 'IL', 'IN', 'IO', 'KS', 'KY', 'LA', 'ME', 'MD', 
                'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 
                'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 
                'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY', 'Other')
    state = SelectField(
        'State',
        choices=[(state, state) for state in STATE_ABBREV]
    )
    zipcode = IntegerField('Zipcode', validators=[DataRequired(), NumberRange(min=5, max=5, message="Zipcode must be 5 digits.")])
    email = StringField('Email', validators=[DataRequired(), Email()])
    emails = []
    submit = SubmitField('Sign Up')

class EmployeeVisitorRegistrationForm(FlaskForm): # inherits from FlaskForm
    firstName = StringField('First Name', validators=[DataRequired()])
    lastName = StringField('Last Name', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    userType = SelectField(
        'User Type',
        choices=[('manager', 'Manager'), ('staff', 'Staff')]
    )
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    phone = IntegerField('Phone', validators=[DataRequired(), NumberRange(min=10, max=10, message="Phone number must be 10 digits.")])
    address = StringField('Address', validators=[DataRequired()])
    city = StringField('City', validators=[DataRequired()])
    STATE_ABBREV = ('AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA', 
                'HI', 'ID', 'IL', 'IN', 'IO', 'KS', 'KY', 'LA', 'ME', 'MD', 
                'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 
                'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 
                'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY', 'Other')
    state = SelectField(
        'State',
        choices=[(state, state) for state in STATE_ABBREV]
    )
    zipcode = IntegerField('Zipcode', validators=[DataRequired(), NumberRange(min=5, max=5, message="Zipcode must be 5 digits.")])
    email = StringField('Email', validators=[DataRequired(), Email()])
    emails = []
    submit = SubmitField('Sign Up')

class LoginForm(FlaskForm): # inherits from FlaskForm
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    remember= BooleanField('Remember Me')
    submit = SubmitField('Login')