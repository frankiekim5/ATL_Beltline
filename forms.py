from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, IntegerField, DecimalField, BooleanField, DateField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, NumberRange


class UserRegistrationForm(FlaskForm): # inherits from FlaskForm
    firstName = StringField('First Name', validators=[DataRequired()])
    lastName = StringField('Last Name', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Sign Up')

class VisitorRegistrationForm(FlaskForm): # inherits from FlaskForm
    firstName = StringField('First Name', validators=[DataRequired()])
    lastName = StringField('Last Name', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    email = StringField('Email', validators=[DataRequired(), Email()])
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
    phone = IntegerField('Phone', validators=[DataRequired(), NumberRange(min=1000000000, max=9999999999, message="Phone number must be 10 digits.")])
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
    zipcode = StringField('Zipcode', validators=[DataRequired(), Length(min=5, max=5, message="Zipcode must be 5 digits.")])
    email = StringField('Email', validators=[DataRequired(), Email()])
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
    phone = IntegerField('Phone', validators=[DataRequired(), NumberRange(min=1000000000, max=9999999999, message="Phone number must be 10 digits.")])
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
    zipcode = StringField('Zipcode', validators=[DataRequired(), Length(min=5, max=5, message="Zipcode must be 5 digits.")])
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Sign Up')

class LoginForm(FlaskForm): # inherits from FlaskForm
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    remember= BooleanField('Remember Me')
    submit = SubmitField('Login')

class TransitForm(FlaskForm): 
    transportType = SelectField('Transport Type', 
        choices = [('marta','MARTA'), ('bus','Bus'),('bike','Bike')], validators=[DataRequired()])
    route = StringField('Route', validators=[DataRequired()])
    price = DecimalField('Price', validators=[DataRequired(), NumberRange(min=0.01, max=None, message="Positive Price Only")])
    connectedSites = SelectField('Connected Sites', 
        choices = [('Atlanta Beltline Center', 'Atlanta Beltline Center')], validators=[DataRequired()])
    submit = SubmitField('Create')


class SiteForm(FlaskForm): 
    siteName = StringField('Name', validators=[DataRequired()])
    zipcode = IntegerField('Zipcode', validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired()])
    manager = SelectField('Manager', 
        choices = [('Frankie Kim', 'Frankie Kim')], validators=[DataRequired()])
    openEveryday = BooleanField('Open Everyday')
    submit = SubmitField('Submit')

class EventForm(FlaskForm): 
    name = StringField('Name', validators=[DataRequired()])
    price = DecimalField('Price', validators=[DataRequired()])
    capacity = IntegerField('Capacity', validators=[DataRequired()])
    minStaff = IntegerField('Minimum Staff Required', validators=[DataRequired()])
    startDate = DateField('Start Date', validators=[DataRequired()])
    endDate = DateField('End Date', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    assignStaff = SelectField('Assign Staff', validators=[DataRequired()], 
        choices = [('Timmy Wu', 'Timmy Wu')])
    submit = SubmitField('Submit')