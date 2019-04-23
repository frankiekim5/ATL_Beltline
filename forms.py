from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, IntegerField, DecimalField, BooleanField, DateField, TextAreaField, RadioField, SelectMultipleField
from wtforms.validators import DataRequired, Length, Email, EqualTo, NumberRange


class UserRegistrationForm(FlaskForm): # inherits from FlaskForm
    firstName = StringField('First Name', validators=[DataRequired()])
    lastName = StringField('Last Name', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Register')

class VisitorRegistrationForm(FlaskForm): # inherits from FlaskForm
    firstName = StringField('First Name', validators=[DataRequired()])
    lastName = StringField('Last Name', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Register')

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
    submit = SubmitField('Register')

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
    submit = SubmitField('Register')

class EmailRegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])

class EmployeeProfileForm(FlaskForm):
    firstName = StringField('First Name', validators=[DataRequired()])
    lastName = StringField('Last Name', validators=[DataRequired()])
    phone = IntegerField('Phone', validators=[DataRequired(), NumberRange(min=1000000000, max=9999999999, message="Phone number must be 10 digits.")])
    email = StringField('Emails', validators=[Email()])
    visitorAccount = BooleanField('Visitor Account')
    update = SubmitField('Update')
    addEmail = SubmitField('Add Email')

class LoginForm(FlaskForm): # inherits from FlaskForm
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    remember= BooleanField('Remember Me')
    submit = SubmitField('Login')

class TransitForm(FlaskForm): 
    transportType = SelectField('Transport Type', 
        choices = [('MARTA','MARTA'), ('Bus','Bus'),('Bike','Bike')], validators=[DataRequired()])
    route = StringField('Route', validators=[DataRequired()])
    price = DecimalField('Price', validators=[DataRequired(), NumberRange(min=0.01, max=None, message="Positive Price Only")])
    submit = SubmitField('Submit')

class SiteForm(FlaskForm):
    siteName = StringField('Name', validators=[DataRequired()])
    zipcode = StringField('Zipcode', validators=[DataRequired(), Length(min=5, max=5, message="Zipcode must be 5 digits.")])
    address = StringField('Address', validators=[DataRequired()])
    ### Access the Database to retrieve managers who haven't been assigned to a site yet ###
    # def managers(self):
    #     managers = SelectField('Manager', 
    #         choices = self.unassigned_managers, validators=[DataRequired()])
    #     return managers
    openEveryday = BooleanField('Open Everyday')
    submit = SubmitField('Submit')

class EventForm(FlaskForm): 
    name = StringField('Name', validators=[DataRequired()])
    price = DecimalField('Price', validators=[NumberRange(min=0.00, max=None, message="Positive Price Only")])
    capacity = IntegerField('Capacity', validators=[DataRequired(), NumberRange(min=1, max=None, message="Positive Capacity Only")])
    minStaff = IntegerField('Minimum Staff Required', validators=[DataRequired(), NumberRange(min=1, max=None, message="Positive Number Only")])
    startDate = DateField('Start Date', validators=[DataRequired()])
    endDate = DateField('End Date', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    updateStaff = SubmitField('Update Staff List')
    submit = SubmitField('Submit')

class ManageSiteForm(FlaskForm): 
    openEveryDay = SelectField('Open Everyday', choices = [('all','--All--'), ('yes', 'Yes'), ('no','No')], validators=[DataRequired()])
    filter = SubmitField('Filter')
    edit = SubmitField('Edit')
    delete = SubmitField('Delete')
    upSort = SubmitField('Up')
    downSort = SubmitField('Down')
    managerUpSort = SubmitField('Up')
    managerDownSort = SubmitField('Down')
    openUpSort = SubmitField('Up')
    openDownSort = SubmitField('Down')
    
class ManageTransitForm(FlaskForm): 
    transportType = SelectField('Transport', choices = [('all','--All--'),('MARTA','MARTA'), ('Bus','Bus'),('Bike','Bike')])
    route = StringField('Route')
    minPrice = DecimalField('Min Price')
    maxPrice = DecimalField('Max Price')
    filter = SubmitField('Filter')
    edit = SubmitField('Edit')
    delete = SubmitField('Delete')
    typeUpSort = SubmitField('Up')
    typeDownSort = SubmitField('Down')
    priceUpSort = SubmitField('Up')
    priceDownSort = SubmitField('Down')

class ManageUser(FlaskForm): 
    username = StringField('Username')
    usertype = SelectField('Type', choices = [('user','User'),('visitor','Visitor'),('staff','Staff'),('manager','Manager')], validators=[DataRequired()])
    status = SelectField('Status', choices = [('all','ALL'),('approved','Approved'),('pending','Pending'),('declined','Declined')])
    filter = SubmitField('Filter')
    approve = SubmitField('Approve')
    decline = SubmitField('Decline')
    usernameUpSort = SubmitField('Up')
    usernameDownSort = SubmitField('Down')
    emailUpSort = SubmitField('Up')
    emailDownSort = SubmitField('Down')
    typeUpSort = SubmitField('Up')
    typeDownSort = SubmitField('Down')
    statusUpSort = SubmitField('Up')
    statusDownSort = SubmitField('Down')

class ManageEvent(FlaskForm): 
    name = StringField('Name')
    descriptionKeyword = StringField('Description Keyword')
    startDate = DateField('Start Date')
    endDate = DateField('End Date')
    minDurationRange = IntegerField('Min Duration')
    maxDurationRange = IntegerField('Max Duration')
    minVisitsRange = IntegerField('Min Visits')
    maxVisitsRange = IntegerField('Max Visits')
    minRevenueRange = IntegerField('Min Revenue')
    maxRevenueRange = IntegerField('Max Revenue')
    filter = SubmitField('Filter')
    viewEdit = SubmitField('View/Edit')
    nameUpSort = SubmitField('Up')
    nameDownSort = SubmitField('Down')
    staffUpSort = SubmitField('Up')
    staffDownSort = SubmitField('Down')
    durationUpSort = SubmitField('Up')
    durationDownSort = SubmitField('Down')
    visitUpSort = SubmitField('Up')
    visitDownSort = SubmitField('Down')
    revenueUpSort = SubmitField('Up')
    revenueDownSort = SubmitField('Down')

class EditEvent(FlaskForm): 
    staffAssigned = SelectMultipleField('Staff Assigned', 
        choices = [('Timmy Wu', 'Timmy Wu'),("Danny Lee", "Danny Lee"),('Frankie Kim','Frankie Kim')])
    description = TextAreaField('Description', validators=[DataRequired()])
    minVisitsRange = IntegerField('Min Daily Visits')
    maxVisitsRange = IntegerField('Max Daily Visits')
    minRevenueRange = IntegerField('Min Daily Revenue')
    maxRevenueRange = IntegerField('Max Daily Revenue')
    filter = SubmitField('Filter')
    update = SubmitField('Update')
    dateUpSort = SubmitField('Up')
    dateDownSort = SubmitField('Down')
    visitUpSort = SubmitField('Up')
    visitDownSort = SubmitField('Down')
    revenueUpSort = SubmitField('Up')
    revenueDownSort = SubmitField('Down')

class UserTakeTransit(FlaskForm): 
    transportType = SelectField('Transport', choices = [('all','--All--'),('MARTA','MARTA'), ('Bus','Bus'),('Bike','Bike')],validators=[DataRequired()])
    minPrice = DecimalField('Min Price')
    maxPrice = DecimalField('Max Price')
    transitDate = DateField('Transit Date')
    logTransit = SubmitField('Log Transit')
    transportUpSort = SubmitField('Up')
    transportDownSort = SubmitField('Down')
    priceUpSort = SubmitField('Up')
    priceDownSort = SubmitField('Down')
    numConnectedUpSort = SubmitField('Up')
    numConnectedDownSort = SubmitField('Down')
    filter = SubmitField('Filter')

class TransitHistory(FlaskForm): 
    transportType = SelectField('Transport', choices = [('all','--All--'),('MARTA','MARTA'), ('Bus','Bus'),('Bike','Bike')],validators=[DataRequired()])
    route = StringField('Route')
    startDate = DateField('Start Date')
    endDate = DateField('End Date')
    filter = SubmitField('Filter')
    dateUpSort = SubmitField('Up')
    dateDownSort = SubmitField('Down')
    routeUpSort = SubmitField('Up')
    routeDownSort = SubmitField('Down')
    transportUpSort = SubmitField('Up')
    transportDownSort = SubmitField('Down')
    priceUpSort = SubmitField('Up')
    priceDownSort = SubmitField('Down')


class ManageStaff(FlaskForm): 
    firstName = StringField('First Name')
    lastName = StringField('Last Name')
    startDate = DateField('Start Date')
    endDate = DateField('End Date')
    filter = SubmitField('Filter')
    staffUpSort = SubmitField('Up')
    staffDownSort = SubmitField('Down')
    shiftUpSort = SubmitField('Up')
    shiftDownSort = SubmitField('Down')

class SiteReport(FlaskForm): 
    startDate = DateField('Start Date', validators=[DataRequired()])
    endDate = DateField('End Date', validators=[DataRequired()])
    minEventCount = IntegerField('Min Event Count')
    maxEventCount = IntegerField('Max Event Count')
    minStaffCount = IntegerField('Min Staff Count')
    maxStaffCount = IntegerField('Max Staff Count')
    minVisitsRange = IntegerField('Min Visits')
    maxVisitsRange = IntegerField('Max Visits')
    minRevenueRange = IntegerField('Min Revenue')
    maxRevenueRange = IntegerField('Max Revenue')
    filter = SubmitField("Filter")
    dailyDetail = SubmitField("Daily Detail")
    dateUpSort = SubmitField('Up')
    dateDownSort = SubmitField('Down')
    eventUpSort = SubmitField('Up')
    eventDownSort = SubmitField('Down')
    staffUpSort = SubmitField('Up')
    staffDownSort = SubmitField('Down')
    visitUpSort = SubmitField('Up')
    visitDownSort = SubmitField('Down')
    revenueUpSort = SubmitField('Up')
    revenueDownSort = SubmitField('Down')


class ViewSchedule(FlaskForm): 
    eventName = StringField("Event Name")
    descriptionKeyword = StringField("Description Keyword")
    startDate = DateField('Start Date')
    endDate = DateField('End Date')
    eventList = RadioField('Events', choices = [('Eastside Trail','Eastside Trail'),('Westside Trail','Westside Trail')])
    filter = SubmitField("Filter")
    viewEvent = SubmitField("View Event")
    eventUpSort = SubmitField('Up')
    eventDownSort = SubmitField('Down')
    startDateUpSort = SubmitField('Up')
    startDateDownSort = SubmitField('Down')
    endDateUpSort = SubmitField('Up')
    endDateDownSort = SubmitField('Down')
    siteUpSort = SubmitField('Up')
    siteDownSort = SubmitField('Down')
    staffUpSort = SubmitField('Up')
    staffDownSort = SubmitField('Down')


class ExploreEvent(FlaskForm): 
    eventName = StringField("Name")
    descriptionKeyword = StringField("Description Keyword")
    startDate = DateField('Start Date')
    endDate = DateField('End Date')
    minVisitsRange = IntegerField('Min Visits')
    maxVisitsRange = IntegerField('Max Visits')
    minPriceRange = IntegerField('Min Price')
    maxPriceRange = IntegerField('Max Price')
    includeVisited = BooleanField('Include Visited')
    includeSoldOutEvent = BooleanField('Include Sold Out Evet')
    filter = SubmitField('Filter')
    eventDetail = SubmitField('Event Detail')

    eventUpSort = SubmitField('Up')
    eventDownSort = SubmitField('Down')
    siteUpSort = SubmitField('Up')
    siteDownSort = SubmitField('Down')
    priceUpSort = SubmitField('Up')
    priceDownSort = SubmitField('Down')
    ticketUpSort = SubmitField('Up')
    ticketDownSort = SubmitField('Down')
    totalUpSort = SubmitField('Up')
    totalDownSort = SubmitField('Down')
    myVisitUpSort = SubmitField('Up')
    myVisitDownSort = SubmitField('Down')

class VisitorEventDetail(FlaskForm): 
    visitDate = DateField('Visit Date', validators=[DataRequired()])
    logVisit = SubmitField('Log Visit')

class ExploreSite(FlaskForm): 
    openEveryDay = SelectField('Open Everyday', choices = [('all','--All--'), ('yes', 'Yes'), ('no','No')])
    startDate = DateField('Start Date')
    endDate = DateField('End Date')
    minVisitsRange = IntegerField('Min Visits')
    maxVisitsRange = IntegerField('Max Visits')
    minEventCount = IntegerField('Min Event Count')
    maxEventCount = IntegerField('Max Event Count')
    includeVisited = BooleanField('Include Visited')
    filter = SubmitField('Filter')
    siteDetail = SubmitField('Site Detail')
    transitDetail = SubmitField('Transit Detail')
    siteUpSort = SubmitField('Up')
    siteDownSort = SubmitField('Down')
    eventUpSort = SubmitField('Up')
    eventDownSort = SubmitField('Down')
    totalUpSort = SubmitField('Up')
    totalDownSort = SubmitField('Down')
    myVisitUpSort = SubmitField('Up')
    myVisitDownSort = SubmitField('Down')

class TransitDetail(FlaskForm): 
    transportType = SelectField('Transport', choices = [('all','--All--'),('MARTA','MARTA'), ('Bus','Bus'),('Bike','Bike')],validators=[DataRequired()])
    routeList = RadioField('Routes', choices = [('816','816'),('102','102')], validators=[DataRequired()])
    transitDate = DateField('Transit Date')
    logTransit = SubmitField('Log Transit')
    filter = SubmitField('Filter')

    transportUpSort = SubmitField('Up')
    transportDownSort = SubmitField('Down')
    priceUpSort = SubmitField('Up')
    priceDownSort = SubmitField('Down')
    connectedSitesUpSort = SubmitField('Up')
    connectedSitesDownSort = SubmitField('Down')
    

class SiteDetail(FlaskForm): 
    visitDate = DateField('Visit Date', validators=[DataRequired()])
    logVisit = SubmitField('Log Visit')

class VisitHistory(FlaskForm): 
    event = StringField("Event")
    startDate = DateField('Start Date')
    endDate = DateField('End Date')
    filter = SubmitField('Filter')

    dateUpSort = SubmitField('Up')
    dateDownSort = SubmitField('Down')
    eventUpSort = SubmitField('Up')
    eventDownSort = SubmitField('Down')
    siteUpSort = SubmitField('Up')
    siteDownSort = SubmitField('Down')
    priceUpSort = SubmitField('Up')
    priceDownSort = SubmitField('Down')
    

class DailyDetail(FlaskForm): 
    eventUpSort = SubmitField('Up')
    eventDownSort = SubmitField('Down')
    staffUpSort = SubmitField('Up')
    staffDownSort = SubmitField('Down')
    visitUpSort = SubmitField('Up')
    visitDownSort = SubmitField('Down')
    revenueUpSort = SubmitField('Up')
    revenueDownSort = SubmitField('Down')