from flask import Flask, render_template, url_for, flash, redirect, session, request, jsonify
from flask_mysqldb import MySQL
from forms import UserRegistrationForm, LoginForm, VisitorRegistrationForm, EmployeeRegistrationForm, EmployeeVisitorRegistrationForm, TransitForm, EmailRegistrationForm, TransitForm, SiteForm, EventForm, ManageSiteForm, ManageTransitForm, ManageUser, ManageEvent, EditEvent, UserTakeTransit, TransitHistory, EmployeeProfileForm, ManageStaff, SiteReport, ViewSchedule, ExploreEvent, VisitorEventDetail, ExploreSite, TransitDetail, SiteDetail, VisitHistory
from passlib.hash import sha256_crypt
from random import randint

app = Flask(__name__)

# Config MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '@SanDiego26' ## Frankie1999! 
app.config['MYSQL_DB'] = 'atlbeltline'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
# Init MySQL
mysql = MySQL(app)

app.config['SECRET_KEY'] = '9a5abb1bd779b72b6a20aeb3cc1d9731'

@app.route('/')
def main():
    return render_template('index.html', emails=request.args.get('emails'), userType=request.args.get('userType'), username=request.args.get('username'))

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    form = EmailRegistrationForm()
    if request.method == 'POST':
        for email in session['emails']:
            if request.form[email] == email:
                session['emails'].remove(email)
                cur = mysql.connection.cursor()
                cur.execute("DELETE FROM user_email WHERE email=%s", (email,))
                mysql.connection.commit()
                cur.close()
        return render_template('profile.html', form=form, emails=request.args.get('emails'), userType=request.args.get('userType'), username=request.args.get('username'))
    else:
        return render_template('profile.html', form=form, emails=request.args.get('emails'), userType=request.args.get('userType'), username=request.args.get('username'))

# @app.route('/employee_profile', methods=['GET', 'POST'])
# def employee_profile():
#     form = EmployeeProfileForm()
#     return render_template('employee_profile.html', form=form, emails=request.args.get('emails'), userType=request.args.get('userType'), username=request.args.get('username'))

@app.route('/registerNav')
def registerNav():
    return render_template('register.html', title='Register Navigation')

@app.route('/register_user', methods=['GET', 'POST'])
def registerUser():
    form = UserRegistrationForm()
    if form.validate_on_submit() and request.method == 'POST':
        username = form.username.data
        firstname = form.firstName.data
        lastname = form.lastName.data
        status = 'Pending'
        password = sha256_crypt.hash(str(form.password.data))
        email = form.email.data

        # Create cursor
        cur = mysql.connection.cursor()

        # Execute query
        cur.execute("INSERT INTO user(username, firstname, lastname, status, password) VALUES(%s, %s, %s, %s, %s)", (username, firstname, lastname, status, password))
        cur.execute("INSERT INTO user_email(username, email) VALUES(%s, %s)", (username, email))

        # Commit to DB
        mysql.connection.commit()

        # Close connection
        cur.close()

        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('main'))
    return render_template('register_user.html', title='Register User', form=form)

@app.route('/register_visitor', methods=['GET', 'POST'])
def registerVisitor():
    form = VisitorRegistrationForm()
    if form.validate_on_submit() and request.method == 'POST':
        username = form.username.data
        firstname = form.firstName.data
        lastname = form.lastName.data
        status = 'Pending'
        password = sha256_crypt.hash(str(form.password.data))
        email = form.email.data

        # Create cursor
        cur = mysql.connection.cursor()

        # Execute query
        cur.execute("INSERT INTO user(username, firstname, lastname, status, password) VALUES(%s, %s, %s, %s, %s)", (username, firstname, lastname, status, password))
        cur.execute("INSERT INTO visitor(username) VALUES(%s)", (username,))
        cur.execute("INSERT INTO user_email(username, email) VALUES(%s, %s)", (username, email))

        # Commit to DB
        mysql.connection.commit()

        # Close connection
        cur.close()
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('main'))
    return render_template('register_visitor.html', title='Register Visitor', form=form)

@app.route('/register_employee', methods=['GET', 'POST'])
def registerEmployee():
    form = EmployeeRegistrationForm()
    if form.validate_on_submit() and request.method == 'POST':
        username = form.username.data
        firstname = form.firstName.data
        lastname = form.lastName.data
        status = 'Pending'
        password = sha256_crypt.hash(str(form.password.data))
        phone = form.phone.data
        address = form.address.data
        city = form.city.data
        state = form.state.data
        zipcode = form.zipcode.data
        userType = form.userType.data
        email = form.email.data

        # Create cursor
        cur = mysql.connection.cursor()

        # Execute query
        cur.execute("INSERT INTO user(username, firstname, lastname, status, password) VALUES(%s, %s, %s, %s, %s)", (username, firstname, lastname, status, password))
        cur.execute("INSERT INTO employee(username, employee_id, phone, address, city, state, zipcode) VALUES(%s, NULL, %s, %s, %s, %s, %s)", (username, phone, address, city, state, zipcode))
        cur.execute("INSERT INTO user_email(username, email) VALUES(%s, %s)", (username, email))
        if (userType == 'manager'):
            cur.execute("INSERT INTO manager(username) VALUES(%s)", (username,))
        elif (userType == 'staff'):
            cur.execute("INSERT INTO staff(username) VALUES(%s)", (username,))

        # Commit to DB
        mysql.connection.commit()

        # Close connection
        cur.close()
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('main'))
    return render_template('register_employee.html', title='Register Employee', form=form)

@app.route('/register_employee_visitor', methods=['GET', 'POST'])
def registerEmployeeVisitor():
    form = EmployeeVisitorRegistrationForm()
    if form.validate_on_submit():
        username = form.username.data
        firstname = form.firstName.data
        lastname = form.lastName.data
        status = 'Pending'
        password = sha256_crypt.hash(str(form.password.data))
        phone = form.phone.data
        address = form.address.data
        city = form.city.data
        state = form.state.data
        zipcode = form.zipcode.data
        userType = form.userType.data
        email = form.email.data

        # Create cursor
        cur = mysql.connection.cursor()

        # Execute query
        cur.execute("INSERT INTO user(username, firstname, lastname, status, password) VALUES(%s, %s, %s, %s, %s)", (username, firstname, lastname, status, password))
        cur.execute("INSERT INTO visitor(username) VALUES(%s)", (username,))
        cur.execute("INSERT INTO employee(username, employee_id, phone, address, city, state, zipcode) VALUES(%s, NULL, %s, %s, %s, %s, %s)", (username, phone, address, city, state, zipcode))
        cur.execute("INSERT INTO user_email(username, email) VALUES(%s, %s)", (username, email))
        if (userType == 'manager'):
            cur.execute("INSERT INTO manager(username) VALUES(%s)", (username,))
        elif (userType == 'staff'):
            cur.execute("INSERT INTO staff(username) VALUES(%s)", (username,))

        # Commit to DB
        mysql.connection.commit()

        # Close connection
        cur.close()
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('main'))
    return render_template('register_employee_visitor.html', title='Register Employee-Visitor', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit and request.method == 'POST':
        email = form.email.data
        password_candidate = form.password.data
        
        cur = mysql.connection.cursor()
        # Get the user via username 
        # NOTE: If user enters an email not in user_email, return an error
        result = cur.execute("SELECT * FROM user_email WHERE email = %s", [email])
        # Login fails
        if result == 0:
            flash('Please enter a correct email address', 'danger')
            return redirect(url_for('login'))
        username = cur.fetchone()['username']
        cur.execute("SELECT * FROM user WHERE username=%s", [username])
        
        if result > 0:
            # Get stored password hash
            password = cur.fetchone()['password']
            # return '<h1>' + str(session) + '</h1>'

            # Compare passwords
            if sha256_crypt.verify(password_candidate, password):
                # Passwords matched
                session['logged_in'] = True
                session['username'] = username
                session['userType'] = 'User' # default to User. Will be changed below if the user is more than just a user

                # Retreive All emails associated with this user.
                cur.execute("SELECT * from user_email WHERE username=%s", [username])
                userEmail = cur.fetchall()
                allEmails = []
                for item in userEmail:
                    allEmails.append(item['email'])
                session['emails'] = allEmails
                # return '<h1>' + str(session['emails']) + '</h1>'
                
                # Check what the user type is #
                visitorResult = cur.execute("SELECT * FROM visitor WHERE username = %s", [username])
                employeeResult = cur.execute("SELECT * FROM employee WHERE username=%s", [username])
                managerResult = cur.execute("SELECT * FROM manager WHERE username=%s", [username])
                staffResult = cur.execute("SELECT * FROM staff WHERE username=%s", [username])
                adminResult = cur.execute("SELECT * FROM administrator WHERE username=%s", [username])
                # Check if user is a visitor / employee-visitor
                if visitorResult > 0:
                    # User is a visitor. Now check if user is also an employee
                    if employeeResult > 0:
                        # User is also an employee. Check what type of employee user is.
                        if managerResult > 0:
                            # User is a manager. Redirect to homepage with manager's functionalities
                            session['userType'] = 'Manager-Visitor'
                        elif staffResult > 0:
                            # User is a staff. Redirect to homepage with staff's functionalities
                            session['userType'] = 'Staff-Visitor'
                        elif adminResult > 0:
                            # User is an admin. Redirect to homepage with admin's functionalities
                            session['userType'] = 'Administrator-Visitor'
                        return redirect(url_for('main', emails=session['emails'], userType=session['userType'], username=session['username']))
                    else:
                        # User is only a visitor.
                        session['userType'] = 'Visitor'
                        return redirect(url_for('main', emails=session['emails'], userType=session['userType'], username=session['username']))
                # Check if user is only an employee
                if employeeResult > 0:
                    # User is also an employee. Check what type of employee user is.
                    if managerResult > 0:
                        # User is a manager. Redirect to homepage with manager's functionalities
                        session['userType'] = 'Manager'
                    elif staffResult > 0:
                        # User is a staff. Redirect to homepage with staff's functionalities
                        session['userType'] = 'Staff'
                    elif adminResult > 0:
                        # User is an admin. Redirect to homepage with admin's functionalities
                        session['userType'] = 'Administrator'
                    first = 'True'
                    return redirect(url_for('main', emails=session['emails'], userType=session['userType'], username=session['username']))
                
                flash('You have been logged in', 'success')
                return redirect(url_for('main', emails=session['emails'], userType=session['userType'], username=session['username']))
            else:
                flash('Invalid login', 'danger')
                return render_template('login.html', title='Login', form=form)
            cur.close()
        else:
            flash('Email not found', 'danger')
            return render_template('login.html', title='Login', form=form)
    # else:
    #     flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route('/logout')
def logout():
    session.clear()
    flash('You are now logged out', 'success')
    return redirect(url_for('login'))

def view_all_users():
    # Create cursor
    cur = mysql.connection.cursor()

    # Execute queries
    cur.execute("SELECT username, status FROM user")
    userStatus = cur.fetchall()
    
    all_users = []
    for user in userStatus:
        user['email_count'] = 0
        all_users.append(user)

    cur.execute("SELECT username FROM user_email")
    user_emails = cur.fetchall()
    
    for person in user_emails:
        username = person['username']
        for user in userStatus:
            if user['username'] == username:
                user['email_count'] += 1
    
    cur.execute("SELECT username FROM visitor")
    visitors = cur.fetchall()
    cur.execute("SELECT username FROM manager")
    managers = cur.fetchall()
    cur.execute("SELECT username FROM staff")
    staff = cur.fetchall()

    # Gather all visitors, managers, and staff from queries
    all_visitors = []
    for visitor in visitors:
        all_visitors.append(visitor['username'])
    all_managers = []
    for manager in managers:
        all_managers.append(manager['username'])
    all_staff = []
    for staff_member in staff:
        all_staff.append(staff_member['username'])

    # Check usertype of each user
    for user in all_users:
        username = user['username']
        # if username in all_visitors or (username in all_visitors and (username in all_managers or username in all_staff)):
        if username in all_visitors and (username not in all_managers and username not in all_staff):
            user['user_type'] = 'Visitor'
        # elif username in all_managers or (username in all_managers and username in all_visitors):
        elif username in all_managers and username not in all_visitors:
            user['user_type'] = 'Manager'
        # elif username in all_staff or (username in all_staff and username in all_visitors):
        elif username in all_staff and username not in all_visitors:
            user['user_type'] = 'Staff'
        elif username in all_visitors and (username in all_managers and username not in all_staff):
            user['user_type'] = 'Manager-Visitor'
        elif username in all_visitors and (username not in all_managers and username in all_staff):
            user['user_type'] = 'Staff-Visitor'
        else:
            user['user_type'] = 'User'

    # Commit to DB
    mysql.connection.commit()

    # Close connection
    cur.close()
    return all_users
    
# Helper method to retrieve all transits
# NOTE: Used again for manage_transit
def get_all_transits():
    # Create cursor
    cur = mysql.connection.cursor()

    # Execute queries
    cur.execute("SELECT * FROM transit")
    transits = cur.fetchall()

    # Calculate # connected sites
    for transit in transits:
        cur.execute("SELECT COUNT(*) FROM connect WHERE transit_type=%s and transit_route=%s", (transit['transit_type'], transit['transit_route']))
        num_connected = cur.fetchone()
        transit['connected_sites'] = num_connected['COUNT(*)']

    # Commit to DB
    mysql.connection.commit()

    # Close connection
    cur.close()
    return transits

# Retrieves all the sites
# NOTE: Used again for manage_transit
def get_all_sites():
    # Create cursor
    cur = mysql.connection.cursor()

    # Retrieve all of the sites
    cur.execute("SELECT site_name FROM site")
    sites = cur.fetchall()
    
    all_sites = []
    for site in sites:
        all_sites.append(site['site_name'])

    # Commit to DB
    mysql.connection.commit()

    # Close connection
    cur.close()
    return all_sites

## SCREEN 15 
@app.route('/take_transit', methods=['GET', 'POST'])
def take_transit():
    form = UserTakeTransit()
    all_transits = get_all_transits()
    all_sites = get_all_sites()
    filtered_transits = []
    username = request.args['username']

    if form.logTransit.data:
        if 'transit' not in request.form:
            flash('Please select a transit to take', 'danger')
        else:
            transit = request.form['transit']
            transit = transit.split()
            transit_route = transit[0]
            transit_type = transit[1]
            transit_date = form.transitDate.data
            
            # Check if user selected a date
            if transit_date == None:
                flash('Please select a date to enter', 'danger')
                return redirect(url_for('take_transit', userType=request.args.get('userType'), username=request.args.get('username')))

            # Enter into take_transit table the data
            # Create cursor
            cur = mysql.connection.cursor()

            # Check first if the attempted entry is a duplicate
            # NOTE: user can only take the same transit once per day
            cur.execute("SELECT * FROM take_transit")
            results = cur.fetchall()
            
            for result in results:
                if result['username'] == username and result['transit_type'] == transit_type and result['transit_route'] == transit_route and result['transit_date'] == transit_date:
                    flash('Cannot take the same transit more than once per day', 'danger')
                    return redirect(url_for('take_transit', userType=request.args.get('userType'), username=request.args.get('username')))


            cur.execute("INSERT INTO take_transit(username, transit_type, transit_route, transit_date) VALUES(%s, %s, %s, %s)", (username, transit_type, transit_route, transit_date))            

            # Commit to DB
            mysql.connection.commit()

            # Close connection
            cur.close()
            flash('Successfully Logged Transit', 'success')
            return redirect(url_for('take_transit', userType=request.args.get('userType'), username=username))
            
    if form.filter.data:
        transportType = form.transportType.data
        minPrice = form.minPrice.data
        maxPrice = form.maxPrice.data

        # Check if min price field was left blank. Default to 0
        if minPrice == None:
            minPrice = 0
        # Check if max price field was left blank. Default to large number
        if maxPrice == None:
            maxPrice = 100000000
        
        
        containSite = request.form.get('contain_site')
        if containSite == 'all' and transportType == 'all':
            for transit in all_transits:
                if transit['transit_price'] >= minPrice and transit['transit_price'] <= maxPrice:
                    filtered_transits.append(transit)
        elif containSite == 'all' and transportType != 'all':
            for transit in all_transits:
                if transit['transit_type'] == transportType and transit['transit_price'] >= minPrice and transit['transit_price'] <= maxPrice:
                    filtered_transits.append(transit)
        elif containSite != 'all' and transportType == 'all':
            # Create cursor
            cur = mysql.connection.cursor()

            # Query the transits that have this site.
            cur.execute("SELECT transit_type, transit_route FROM connect WHERE site_name=%s", (containSite,))
            transit_sites = cur.fetchall()

            needed_transits = []

            for transit in transit_sites:
                needed_transits.append(transit)

            for transit in all_transits:
                for comparison in needed_transits:
                    if transit['transit_type'] == comparison['transit_type'] and transit['transit_price'] >= minPrice and transit['transit_price'] <= maxPrice and transit not in filtered_transits:
                        filtered_transits.append(transit)            
                
            # Commit to DB
            mysql.connection.commit()

            # Close connection
            cur.close()
        else:
            # Create cursor
            cur = mysql.connection.cursor()

            # Query the transits that have this site.
            cur.execute("SELECT transit_type, transit_route FROM connect WHERE site_name=%s", (containSite,))
            transit_sites = cur.fetchall()

            needed_transits = []
            for transit in transit_sites:
                if transit['transit_type'] == transportType:
                    needed_transits.append(transit)
            for transit in all_transits:
                for comparison in needed_transits:
                    if transit['transit_type'] == comparison['transit_type'] and transit['transit_price'] >= minPrice and transit['transit_price'] <= maxPrice:
                        filtered_transits.append(transit) 
        return render_template('take_transit.html', sites=all_sites, transits=filtered_transits, title="Take Transit",legend="Take Transit",form=form, userType=request.args.get('userType'), username=username)
    return render_template('take_transit.html', sites=all_sites, transits=filtered_transits, title="Take Transit",legend="Take Transit",form=form, userType=request.args.get('userType'), username=username)

# Helper method to query transit history for user
def get_transit_history(username):
    # Create cursor
    cur = mysql.connection.cursor()

    # Retrieve information from take_transit
    cur.execute("SELECT transit_type, transit_route, transit_date FROM take_transit WHERE username=%s", (username,))
    transits = cur.fetchall()

    # Retrieve the transit price from transit
    transit_history = []
    for transit in transits:
        history_entry = {}
        cur.execute("SELECT transit_price FROM transit WHERE transit_type=%s and transit_route=%s", (transit['transit_type'], transit['transit_route']))
        transit_price = cur.fetchone()
        history_entry['transit_type'] = transit['transit_type']
        history_entry['transit_route'] = transit['transit_route']
        history_entry['transit_price'] = transit_price['transit_price']
        history_entry['transit_date'] = transit['transit_date']
        transit_history.append(history_entry)

    # Commit to DB
    mysql.connection.commit()

    # Close connection
    cur.close()
    return transit_history

## SCREEN 16 
@app.route('/transit_history', methods=['GET', 'POST'])
def transit_history(): 
    form = TransitHistory()
    username = request.args['username']
    transit_history = get_transit_history(username)
    all_sites = get_all_sites()

    if form.filter.data:
        transportType = form.transportType.data
        route = form.route.data
        startDate = form.startDate.data
        endDate = form.endDate.data
        
        filtered_transits = []
        containSite = request.form.get('contain_site')
        if containSite == 'all' and transportType == 'all':
            if route == "":
                for transit in transit_history:
                    if startDate == None and endDate != None:
                        if transit['transit_date'] <= endDate:
                            filtered_transits.append(transit)
                    elif startDate != None and endDate == None:
                        if transit['transit_date'] >= startDate:
                            filtered_transits.append(transit)
                    elif startDate != None and endDate != None:
                        if transit['transit_date'] >= startDate and transit['transit_date'] <= endDate:
                            filtered_transits.append(transit)
                    else:
                        filtered_transits.append(transit)
            else:
                for transit in transit_history:
                    if transit['transit_route'] == route:
                        if startDate == None and endDate != None:
                            if transit['transit_date'] <= endDate:
                                filtered_transits.append(transit)
                        elif startDate != None and endDate == None:
                            if transit['transit_date'] >= startDate:
                                filtered_transits.append(transit)
                        elif startDate != None and endDate != None:
                            if transit['transit_date'] >= startDate and transit['transit_date'] <= endDate:
                                filtered_transits.append(transit)
                        else:
                            filtered_transits.append(transit)
        elif containSite == 'all' and transportType != 'all':
            if route == "":
                for transit in transit_history:
                    if transit['transit_type'] == transportType:
                        if startDate == None and endDate != None:
                            if transit['transit_date'] <= endDate:
                                filtered_transits.append(transit)
                        elif startDate != None and endDate == None:
                            if transit['transit_date'] >= startDate:
                                filtered_transits.append(transit)
                        elif startDate != None and endDate != None:
                            if transit['transit_date'] >= startDate and transit['transit_date'] <= endDate:
                                filtered_transits.append(transit)
                        else:
                            filtered_transits.append(transit)
            else:
                for transit in transit_history:
                    if transit['transit_type'] == transportType and transit['transit_route'] == route:
                        if startDate == None and endDate != None:
                            if transit['transit_date'] <= endDate:
                                filtered_transits.append(transit)
                        elif startDate != None and endDate == None:
                            if transit['transit_date'] >= startDate:
                                filtered_transits.append(transit)
                        elif startDate != None and endDate != None:
                            if transit['transit_date'] >= startDate and transit['transit_date'] <= endDate:
                                filtered_transits.append(transit)
                        else:
                            filtered_transits.append(transit)
        elif containSite != 'all' and transportType == 'all':
            # Create cursor
            cur = mysql.connection.cursor()

            # Query the transits that have this site.
            cur.execute("SELECT transit_type, transit_route FROM connect WHERE site_name=%s", (containSite,))
            transit_sites = cur.fetchall()

            needed_transits = []
            if route == "":
                for transit in transit_sites:
                    needed_transits.append(transit)
            else:
                for transit in transit_sites:
                    if transit['transit_route'] == route:
                        needed_transits.append(transit)
            for transit in transit_history:
                for comparison in needed_transits:
                    if transit['transit_route'] == comparison['transit_route'] and transit['transit_type'] == comparison['transit_type']:
                        if startDate == None and endDate != None:
                            if transit['transit_date'] <= endDate:
                                filtered_transits.append(transit)
                        elif startDate != None and endDate == None:
                            if transit['transit_date'] >= startDate:
                                filtered_transits.append(transit)
                        elif startDate != None and endDate != None:
                            if transit['transit_date'] >= startDate and transit['transit_date'] <= endDate:
                                filtered_transits.append(transit)
                        else:
                            filtered_transits.append(transit)   
                
            # Commit to DB
            mysql.connection.commit()

            # Close connection
            cur.close()
        else:
            # Create cursor
            cur = mysql.connection.cursor()

            # Query the transits that have this site.
            cur.execute("SELECT transit_type, transit_route FROM connect WHERE site_name=%s", (containSite,))
            transit_sites = cur.fetchall()

            needed_transits = []
            if route == "":
                for transit in transit_sites:
                    if transit['transit_type'] == transportType:
                        needed_transits.append(transit)
            else:
                for transit in transit_sites:
                    if transit['transit_route'] == route and transit['transit_type'] == transportType:
                        needed_transits.append(transit)
            for transit in transit_history:
                for comparison in needed_transits:
                    if transit['transit_route'] == comparison['transit_route'] and transit['transit_type'] == comparison['transit_type']:
                        if startDate == None and endDate != None:
                            if transit['transit_date'] <= endDate:
                                filtered_transits.append(transit)
                        elif startDate != None and endDate == None:
                            if transit['transit_date'] >= startDate:
                                filtered_transits.append(transit)
                        else:
                            filtered_transits.append(transit)
            # Commit to DB
            mysql.connection.commit()

            # Close connection
            cur.close()
                
        return render_template('transit_history.html', form=form, sites=all_sites, transits=filtered_transits, title='Transit History', legend='Transit History', emails=request.args.get('emails'), userType=request.args.get('userType'), username=request.args.get('username'))

    return render_template('transit_history.html', sites=all_sites, transits=[], title="Transit History",legend="Transit History",form=form, userType=request.args.get('userType'), username=username)

# Helper method to deal with email modifications
@app.route('/remove_email/<email>', methods=['GET', 'POST'])
def remove_email(email):
    username = request.args['username']
    # Create cursor
    cur = mysql.connection.cursor()

    # Check if user is trying to remove his or her only email
    cur.execute("SELECT COUNT(*) FROM user_email WHERE username=%s", (username,))
    emails = cur.fetchone()

    email_count = emails['COUNT(*)']
    if email_count == 1:
        flash('You must have at least one email', 'danger')
        return redirect(url_for('manage_profile', userType=request.args.get('userType'), username=username))

    # Remove the email from the user_emails table
    cur.execute("DELETE FROM user_email WHERE email=%s", (email,))

    # Commit to DB
    mysql.connection.commit()

    # Close connection
    cur.close()
    return redirect(url_for('manage_profile', userType=request.args.get('userType'), username=username))

## SCREEN 17 
@app.route('/manage_profile', methods=['GET','POST'])
def manage_profile():
    form = EmployeeProfileForm()
    profile = {}
    username = request.args['username']
    userType = request.args['userType']
    emails = []

    # Create cursor
    cur = mysql.connection.cursor()

    # Add email to user_email table
    if form.validate_on_submit():
        if form.addEmail.data:
            email = form.email.data

            # Insert the email into the table
            cur.execute("INSERT INTO user_email(username, email) VALUES(%s, %s)", (username, email))
            # Commit to DB
            mysql.connection.commit()

            # Close connection
            cur.close()

        return redirect(url_for('manage_profile', userType=request.args.get('userType'), username=request.args.get('username')))

    elif form.update.data:
        firstname = form.firstName.data
        lastname = form.lastName.data
        phone = form.phone.data

        # Update firstname and lastname
        cur.execute("UPDATE user SET firstname=%s, lastname=%s WHERE username=%s", (firstname, lastname, username))

        # Update phone number
        cur.execute("UPDATE employee SET phone=%s WHERE username=%s", (phone, username))

        # Commit to DB
        mysql.connection.commit()

        # Close connection
        cur.close()

        return redirect(url_for('manage_profile', userType=request.args.get('userType'), username=request.args.get('username')))

    # Retrieve all information for the employee and store in profile

    # Retrieve first name and last name for employee
    cur.execute("SELECT firstname, lastname FROM user WHERE username=%s", (username,))
    name = cur.fetchone()

    profile['firstname'] = name['firstname']
    profile['lastname'] = name['lastname']

    # Retrieve site name if employee is a manager
    if userType == 'Manager' or userType == 'Manager-Visitor':
        cur.execute("SELECT site_name FROM site WHERE manager_username=%s", (username,))
        site_name = cur.fetchone()
        if site_name == None:
            profile['site_name'] = "None"
        else:
            profile['site_name'] = site_name['site_name']
    else:
        profile['site_name'] = "None"
    
    # Retrieve Employee ID, set to None if account is not approved
    cur.execute("SELECT employee_id, phone, address, city, state, zipcode FROM employee WHERE username=%s", (username,))
    employee_info = cur.fetchone()
    if employee_info['employee_id'] == None:
        profile['employee_id'] = "None"
    else:
        profile['employee_id'] = employee_info['employee_id']
    profile['phone'] = employee_info['phone']
    profile['address'] = employee_info['address'] + ", " + employee_info['city'] + ", " + employee_info['state'] + ", " + employee_info['zipcode']
    
    form.firstName.data = profile['firstname']
    form.lastName.data = profile['lastname']
    form.phone.data = profile['phone']
    

    # Retrieve all emails from the user_email table
    cur.execute("SELECT email FROM user_email WHERE username=%s", (username,))
    user_emails = cur.fetchall()
    
    # Condense all user's emails into a list
    
    for email in user_emails:
        emails.append(email['email'])

    # Commit to DB
    mysql.connection.commit()

    # Close connection
    cur.close()
    return render_template("employee_profile.html", profile=profile, title="Manage Profile", legend="Manage Profile", form=form, emails=emails, userType=request.args.get('userType'), username=username)

## SCREEN 18 
@app.route('/manage_user', methods=['GET', 'POST'])
def manage_user(): 
    form = ManageUser()
    all_users = view_all_users()
    if form.validate_on_submit():
        if form.filter.data:
            username = form.username.data
            usertype = form.usertype.data 
            status = form.status.data
            filtered_users = []
            if username == "":
                if usertype == 'user':
                    for user in all_users:
                        if status == 'all':
                            if user['user_type'] == 'User':
                                filtered_users.append(user)
                        elif status == 'approved':
                            if user['user_type'] == 'User' and user['status'] == 'Approved':
                                filtered_users.append(user)
                        elif status == 'pending':
                            if user['user_type'] == 'User' and user['status'] == 'Pending':
                                filtered_users.append(user)
                        else:
                            if user['user_type'] == 'User' and user['status'] == 'Declined':
                                filtered_users.append(user)
                    return render_template('manage_user.html', all_users=filtered_users, title="Manage User", legend="Manage User", form=form, emails=request.args.get('emails'), userType=request.args.get('userType'), username=request.args.get('username'))
                elif usertype == 'visitor':
                    for user in all_users:
                        if status == 'all':
                            if user['user_type'] == 'Visitor' or user['user_type'] == 'Staff-Visitor' or user['user_type'] == 'Manager-Visitor':
                                if user['user_type'] == 'Manager-Visitor':
                                    user['user_type'] = 'Manager'
                                elif user['user_type'] == 'Staff-Visitor':
                                    user['user_type'] = 'Staff'
                                filtered_users.append(user)
                        elif status == 'approved':
                            if user['user_type'] == 'Visitor' or user['user_type'] == 'Staff-Visitor' or user['user_type'] == 'Manager-Visitor' and user['status'] == 'Approved':
                                if user['user_type'] == 'Manager-Visitor':
                                    user['user_type'] = 'Manager'
                                elif user['user_type'] == 'Staff-Visitor':
                                    user['user_type'] = 'Staff'
                                filtered_users.append(user)
                        elif status == 'pending':
                            if user['user_type'] == 'Visitor' or user['user_type'] == 'Staff-Visitor' or user['user_type'] == 'Manager-Visitor' and user['status'] == 'Pending':
                                if user['user_type'] == 'Manager-Visitor':
                                    user['user_type'] = 'Manager'
                                elif user['user_type'] == 'Staff-Visitor':
                                    user['user_type'] = 'Staff'
                                filtered_users.append(user)
                        else:
                            if user['user_type'] == 'Visitor' or user['user_type'] == 'Staff-Visitor' or user['user_type'] == 'Manager-Visitor' and user['status'] == 'Declined':
                                if user['user_type'] == 'Manager-Visitor':
                                    user['user_type'] = 'Manager'
                                elif user['user_type'] == 'Staff-Visitor':
                                    user['user_type'] = 'Staff'
                                filtered_users.append(user)
                    return render_template('manage_user.html', all_users=filtered_users, title="Manage User", legend="Manage User", form=form, emails=request.args.get('emails'), userType=request.args.get('userType'), username=request.args.get('username'))
                elif usertype == 'staff':
                    for user in all_users:
                        if status == 'all':
                            if user['user_type'] == 'Staff' or user['user_type'] == 'Staff-Visitor':
                                if user['user_type'] == 'Staff-Visitor':
                                    user['user_type'] = 'Staff'
                                filtered_users.append(user)
                        elif status == 'approved':
                            if user['user_type'] == 'Staff' or user['user_type'] == 'Staff-Visitor' and user['status'] == 'Approved':
                                if user['user_type'] == 'Staff-Visitor':
                                    user['user_type'] = 'Staff'
                                filtered_users.append(user)
                        elif status == 'pending':
                            if user['user_type'] == 'Staff' or user['user_type'] == 'Staff-Visitor' and user['status'] == 'Pending':
                                if user['user_type'] == 'Staff-Visitor':
                                    user['user_type'] = 'Staff'
                                filtered_users.append(user)
                        else:
                            if user['user_type'] == 'Staff' or user['user_type'] == 'Staff-Visitor' and user['status'] == 'Declined':
                                if user['user_type'] == 'Staff-Visitor':
                                    user['user_type'] = 'Staff'
                                filtered_users.append(user)
                    return render_template('manage_user.html', all_users=filtered_users, title="Manage User", legend="Manage User", form=form, emails=request.args.get('emails'), userType=request.args.get('userType'), username=request.args.get('username'))                    
                else:
                    for user in all_users:
                        if status == 'all':
                            if user['user_type'] == 'Manager' or user['user_type'] == 'Manager-Visitor':
                                if user['user_type'] == 'Manager-Visitor':
                                    user['user_type'] = 'Manager'
                                filtered_users.append(user)
                        elif status == 'approved':
                            if user['user_type'] == 'Manager' or user['user_type'] == 'Manager-Visitor' and user['status'] == 'Approved':
                                if user['user_type'] == 'Manager-Visitor':
                                    user['user_type'] = 'Manager'
                                filtered_users.append(user)
                        elif status == 'pending':
                            if user['user_type'] == 'Manager' or user['user_type'] == 'Manager-Visitor' and user['status'] == 'Pending':
                                if user['user_type'] == 'Manager-Visitor':
                                    user['user_type'] = 'Manager'
                                filtered_users.append(user)
                        else:
                            if user['user_type'] == 'Manager' or user['user_type'] == 'Manager-Visitor' and user['status'] == 'Declined':
                                if user['user_type'] == 'Manager-Visitor':
                                    user['user_type'] = 'Manager'
                                filtered_users.append(user)
                    return render_template('manage_user.html', all_users=filtered_users, title="Manage User", legend="Manage User", form=form, emails=request.args.get('emails'), userType=request.args.get('userType'), username=request.args.get('username'))                    
            else:
                # username field has been filled
                for user in all_users:
                    if user['username'] == username:
                        if user['user_type'] == 'Manager-Visitor':
                            user['user_type'] = 'Manager'
                        elif user['user_type'] == 'Staff-Visitor':
                            user['user_type'] = 'Staff'
                        # Check if username matches all filter criteria
                        if usertype == user['user_type'].lower():
                            if status == 'all':
                                filtered_users.append(user)
                            elif status == 'pending' and user['user_type'] == 'Pending':
                                filtered_users.append(user)
                            elif status == 'approved' and user['user_type'] == 'Approved':
                                filtered_users.append(user)
                            elif status == 'declind' and user['user_type'] == 'Declined':
                                filtered_users.append(user)
                return render_template('manage_user.html', all_users=filtered_users, title="Manage User", legend="Manage User", form=form, emails=request.args.get('emails'), userType=request.args.get('userType'), username=request.args.get('username'))                    
        elif form.approve.data:
            selected_user = request.form['user']
            for user in all_users:
                if user['username'] == selected_user:
                    # Create cursor
                    cur = mysql.connection.cursor()
                    if user['status'] == 'Pending' or user['status'] == 'Declined':
                        # Set the user's status to Approved in the database
                        cur.execute("UPDATE user SET status='Approved' WHERE username=%s", (selected_user,))

                        if user['user_type'] == 'Manager' or user['user_type'] == 'Manager-Visitor' or user['user_type'] == 'Staff' or user['user_type'] == 'Staff-Visitor':
                            emp_id = randint(100000000, 999999999)
                            cur.execute("UPDATE employee SET employee_id=%s WHERE username=%s", (emp_id, selected_user))

                        # Commit to DB
                        mysql.connection.commit()

                        # Close connection
                        cur.close()
            return redirect(url_for('manage_user', emails=request.args.get('emails'), userType=request.args.get('userType'), username=request.args.get('username')))
        elif form.decline.data:
            selected_user = request.form['user']
            for user in all_users:
                if user['username'] == selected_user:
                    # Create cursor
                    cur = mysql.connection.cursor()
                    if user['status'] == 'Pending':
                        cur.execute("UPDATE user SET status='Declined' WHERE username=%s", (selected_user,))

                        # Commit to DB
                        mysql.connection.commit()

                        # Close connection
                        cur.close()
                    elif user['status'] == 'Approved':
                        flash('Cannot decline an approved user', 'danger')
            return redirect(url_for('manage_user', emails=request.args.get('emails'), userType=request.args.get('userType'), username=request.args.get('username')))
    for user in all_users:
        if user['user_type'] == 'Manager-Visitor':
            user['user_type'] = 'Manager'
        elif user['user_type'] == 'Staff-Visitor':
            user['user_type'] = 'Staff'
    return render_template('manage_user.html', all_users=all_users, title="Manage User", legend="Manage User", form=form, emails=request.args.get('emails'), userType=request.args.get('userType'), username=request.args.get('username'))

def view_managers_for_sites():
        # Create cursor
        cur = mysql.connection.cursor()

        # Query retrieves first and last names for unassigned managers
        cur.execute("SELECT firstname, lastname FROM user WHERE username in (SELECT username FROM manager WHERE username not in (SELECT manager_username FROM site))")
        results = cur.fetchall()

        managers = []
        for manager in results:
            fullName = manager['firstname'] + " " + manager['lastname']
            managers.append(fullName)

        # Commit to DB
        mysql.connection.commit()

        # Close connection
        cur.close()
        return managers

def managers_assigned_and_sites():
    
        # Create cursor
        cur = mysql.connection.cursor()
        
        # Query retrieves the sites by site_name
        cur.execute("SELECT site_name, manager_username, open_everyday from site")
        results2 = cur.fetchall()

        sites = []
        for site in results2:
            # sites.append(site['site_name'])
            each_site = {}
            each_site['site'] = site['site_name']
            each_site['manager'] = site['manager_username']
            if site['open_everyday'] == 1:
                each_site['open_everyday'] = 'Yes'
            else:
                each_site['open_everyday'] = 'No'
            sites.append(each_site)
        
        for site in sites:
            cur.execute("SELECT firstname, lastname FROM user WHERE username in (SELECT username FROM manager WHERE username in (SELECT manager_username FROM site WHERE site_name=%s))", [site['site']])
            result = cur.fetchone()
            fullName = result['firstname'] + " " + result['lastname']
            site['manager'] = fullName

        # cur.execute("SELECT firstname, lastname FROM user WHERE username in (SELECT username FROM manager WHERE username in (SELECT manager_username FROM site WHERE site_name=%s))", [site['site_name']])
        # Commit to DB
        mysql.connection.commit()

        # Close connection
        cur.close()
        return sites

@app.route('/manage_site', methods=['GET', 'POST'])
def manage_site():
    form = ManageSiteForm()
    sites = managers_assigned_and_sites()
    if form.validate_on_submit():
        if form.filter.data:
            site = request.form['sitesDrop']
            managers = request.form.get('managers')
            openEveryDay = form.openEveryDay.data
            filtered_sites = []
            # Filter based on site and manager being 'All'
            if site == 'all' and managers == 'all':
                if openEveryDay == 'yes':
                    for site in sites:
                        if site['open_everyday'] == 'Yes':
                            filtered_sites.append(site)
                elif openEveryDay == 'no':
                    for site in sites:
                        if site['open_everyday'] == 'No':
                            filtered_sites.append(site)
                else:
                    filtered_sites = sites
                return render_template('manage_site.html', form=form, sites=sites, sitesList=filtered_sites, title='Manage Navigation', legend='Manage Site', emails=request.args.get('emails'), userType=request.args.get('userType'), username=request.args.get('username'))
            elif site != 'all' and managers == 'all':
                if openEveryDay == 'yes':
                    for each_site in sites:
                        if site == each_site['site'] and each_site['open_everyday'] == 'Yes':
                            filtered_sites.append(each_site)
                            return render_template('manage_site.html', form=form, sites=sites, sitesList=filtered_sites, title='Manage Navigation', legend='Manage Site', emails=request.args.get('emails'), userType=request.args.get('userType'), username=request.args.get('username'))
                    return render_template('manage_site.html', form=form, sites=sites, sitesList=filtered_sites, title='Manage Navigation', legend='Manage Site', emails=request.args.get('emails'), userType=request.args.get('userType'), username=request.args.get('username'))
                elif openEveryDay == 'no':
                    for each_site in sites:
                        if site == each_site['site'] and each_site['open_everyday'] == 'No':
                            filtered_sites.append(each_site)
                            return render_template('manage_site.html', form=form, sites=sites, sitesList=filtered_sites, title='Manage Navigation', legend='Manage Site', emails=request.args.get('emails'), userType=request.args.get('userType'), username=request.args.get('username'))
                    return render_template('manage_site.html', form=form, sites=sites, sitesList=filtered_sites, title='Manage Navigation', legend='Manage Site', emails=request.args.get('emails'), userType=request.args.get('userType'), username=request.args.get('username'))
                else:
                    for each_site in sites:
                        if site == each_site['site']:
                            filtered_sites.append(each_site)
                            return render_template('manage_site.html', form=form, sites=sites, sitesList=filtered_sites, title='Manage Navigation', legend='Manage Site', emails=request.args.get('emails'), userType=request.args.get('userType'), username=request.args.get('username'))
            elif managers != 'all' and site == 'all':
                if openEveryDay == 'yes':
                    for each_site in sites:
                        if managers == each_site['manager'] and each_site['open_everyday'] == 'Yes':
                            filtered_sites.append(each_site)
                            return render_template('manage_site.html', form=form, sites=sites, sitesList=filtered_sites, title='Manage Navigation', legend='Manage Site', emails=request.args.get('emails'), userType=request.args.get('userType'), username=request.args.get('username'))
                    return render_template('manage_site.html', form=form, sites=sites, sitesList=filtered_sites, title='Manage Navigation', legend='Manage Site', emails=request.args.get('emails'), userType=request.args.get('userType'), username=request.args.get('username'))
                elif openEveryDay == 'no':
                    for each_site in sites:
                        if managers == each_site['manager'] and each_site['open_everyday'] == 'No':
                            filtered_sites.append(each_site)
                            return render_template('manage_site.html', form=form, sites=sites, sitesList=filtered_sites, title='Manage Navigation', legend='Manage Site', emails=request.args.get('emails'), userType=request.args.get('userType'), username=request.args.get('username'))
                    return render_template('manage_site.html', form=form, sites=sites, sitesList=filtered_sites, title='Manage Navigation', legend='Manage Site', emails=request.args.get('emails'), userType=request.args.get('userType'), username=request.args.get('username'))
                else:
                    for each_site in sites:
                        if managers == each_site['manager']:
                            filtered_sites.append(each_site)
                            return render_template('manage_site.html', form=form, sites=sites, sitesList=filtered_sites, title='Manage Navigation', legend='Manage Site', emails=request.args.get('emails'), userType=request.args.get('userType'), username=request.args.get('username'))
            else:
                if openEveryDay == 'yes':
                    for each_site in sites:
                        if managers == each_site['manager'] and site == each_site['site'] and each_site['open_everyday'] == 'Yes':
                            filtered_sites.append(each_site)
                            return render_template('manage_site.html', form=form, sites=sites, sitesList=filtered_sites, title='Manage Navigation', legend='Manage Site', emails=request.args.get('emails'), userType=request.args.get('userType'), username=request.args.get('username'))
                    return render_template('manage_site.html', form=form, sites=sites, sitesList=filtered_sites, title='Manage Navigation', legend='Manage Site', emails=request.args.get('emails'), userType=request.args.get('userType'), username=request.args.get('username'))
                elif openEveryDay == 'no':
                    for each_site in sites:
                        if managers == each_site['manager'] and site == each_site['site'] and each_site['open_everyday'] == 'No':
                            filtered_sites.append(each_site)
                            return render_template('manage_site.html', form=form, sites=sites, sitesList=filtered_sites, title='Manage Navigation', legend='Manage Site', emails=request.args.get('emails'), userType=request.args.get('userType'), username=request.args.get('username'))
                    return render_template('manage_site.html', form=form, sites=sites, sitesList=filtered_sites, title='Manage Navigation', legend='Manage Site', emails=request.args.get('emails'), userType=request.args.get('userType'), username=request.args.get('username'))
                else:
                    for each_site in sites:
                        if managers == each_site['manager'] and site == each_site['site']:
                            filtered_sites.append(each_site)
                            return render_template('manage_site.html', form=form, sites=sites, sitesList=filtered_sites, title='Manage Navigation', legend='Manage Site', emails=request.args.get('emails'), userType=request.args.get('userType'), username=request.args.get('username'))
                    return render_template('manage_site.html', form=form, sites=sites, sitesList=filtered_sites, title='Manage Navigation', legend='Manage Site', emails=request.args.get('emails'), userType=request.args.get('userType'), username=request.args.get('username'))
        elif form.edit.data:
            if 'site' not in request.form:
                flash('Please select a site to edit', 'danger')
            else:
                site_name = request.form['site']
                return redirect(url_for('edit_site', site_name=site_name, emails=request.args.get('emails'), userType=request.args.get('userType'), username=request.args.get('username')))
        elif form.delete.data:
            if 'site' not in request.form:
                flash('Please select a site to delete', 'danger')
            else:
                site_name = request.form['site']
                # Delete the site from the database
                # Create cursor
                cur = mysql.connection.cursor()

                # Execute query
                cur.execute("DELETE FROM site WHERE site_name=%s", (site_name,))
                # Commit to DB
                mysql.connection.commit()

                # Close connection
                cur.close()
                flash('Successfully Deleted Site', 'success')
                return redirect(url_for('manage_site', emails=request.args.get('emails'), userType=request.args.get('userType'), username=request.args.get('username')))
    return render_template('manage_site.html', form=form, sites=sites, sitesList=sites, title='Manage Navigation', legend='Manage Site', emails=request.args.get('emails'), userType=request.args.get('userType'), username=request.args.get('username'))


## SCREEN 21 
@app.route('/create_site', methods=['GET', 'POST'])
def create_site(): 
    form = SiteForm()
    managers = view_managers_for_sites()
    if form.validate_on_submit() and request.method == 'POST': 
        siteName = form.siteName.data
        zipcode = form.zipcode.data
        address = form.address.data 
        manager = request.form.get('unassigned_managers')
        openEveryday = form.openEveryday.data

        # Create cursor
        cur = mysql.connection.cursor()

        # Execute queries
        # Get manager's username
        manager = manager.split()
        cur.execute("SELECT username FROM user WHERE firstname=%s and lastname=%s", [manager[0], manager[1]])
        manager_username = cur.fetchone()
        # Set manager's assigned to site value to True (1)
        cur.execute("INSERT INTO site(site_name, manager_username, zipcode, address, open_everyday) VALUES(%s, %s, %s, %s, %s)", (siteName, manager_username['username'], zipcode, address, openEveryday))

        # Commit to DB
        mysql.connection.commit()

        # Close connection
        cur.close()
        flash('Successfully Created Site', 'success')
        return redirect(url_for('manage_site', emails=request.args.get('emails'), userType=request.args.get('userType'), username=request.args.get('username')))
    return render_template("create_site.html", title='Create Site', form=form, legend='Create Site', unassigned_managers=managers, emails=request.args.get('emails'), userType=request.args.get('userType'), username=request.args.get('username'))

## SCREEN 20 
@app.route('/edit_site/<site_name>', methods=['GET', 'POST'])
def edit_site(site_name):
    ## can query from the database to get the specific SiteName as PK
    ## site = query using curr
    form = SiteForm()
    if form.validate_on_submit() and request.method == 'POST':
        ## here is where the site.name etc. should be in order to update 
        siteName = form.siteName.data
        zipcode = form.zipcode.data
        address = form.address.data
        manager = request.form.get('unassigned_managers')
        openEveryday = form.openEveryday.data

        # Create cursor
        cur = mysql.connection.cursor()

        # Execute queries
        manager = manager.split()
        cur.execute("SELECT username FROM user WHERE firstname=%s and lastname=%s", [manager[0], manager[1]])
        manager_username = cur.fetchone()
        # Check if manager has stayed the same or is an unassigned manager
        cur.execute("SELECT username FROM manager WHERE username NOT IN (SELECT manager_username FROM site)")
        unassigned_managers = cur.fetchall()
        
        new_manager = ""
        for manager in unassigned_managers:
            if manager_username == manager['username']:
                new_manager = manager_username
            else:
                new_manager = manager_username['username']
        
        cur.execute("UPDATE site SET site_name=%s, manager_username=%s, zipcode=%s, address=%s, open_everyday=%s WHERE site_name=%s", (siteName, new_manager, zipcode, address, openEveryday, site_name))
        # Commit to DB
        mysql.connection.commit()

        # Close connection
        cur.close()
        return redirect(url_for('manage_site', emails=request.args.get('emails'), userType=request.args.get('userType'), username=request.args.get('username')))
    elif request.method == 'GET':
        # Create cursor
        cur = mysql.connection.cursor()

        # Query the information for the site
        cur.execute("SELECT site_name, manager_username, zipcode, address, open_everyday FROM site WHERE site_name=%s", [site_name])
        site = cur.fetchone()
        if site['open_everyday'] == 1:
            site['open_everyday'] = True
        else:
            site['open_everyday'] = False
        
        
        cur.execute("SELECT firstname, lastname FROM user WHERE username in (SELECT username FROM manager WHERE username in (SELECT manager_username FROM site WHERE site_name=%s))", [site_name])
        manager_name = cur.fetchone()
        site['manager_name'] = manager_name['firstname'] + " " + manager_name['lastname']

        cur.execute("SELECT firstname, lastname FROM user WHERE username in (SELECT username FROM manager WHERE username not in (SELECT manager_username FROM site))")
        result = cur.fetchall()

        managers = []
        for manager in result:
            fullName = manager['firstname'] + " " + manager['lastname']
            managers.append(fullName)

        managers.insert(0, site['manager_name'])

        # Commit to DB
        mysql.connection.commit()

        # Close connection
        cur.close()
        
        # Put the information from the site into the Edit Site screen
        form.siteName.data = site['site_name']
        form.zipcode.data = site['zipcode']
        form.address.data = site['address']
        form.openEveryday.data = site['open_everyday']

        return render_template("create_site.html", title="Edit Site", unassigned_managers=managers, form=form, legend="Edit Site",  emails=request.args.get('emails'), userType=request.args.get('userType'), username=request.args.get('username'))

## SCREEN 22 
@app.route('/manage_transit', methods=['GET', 'POST'])
def manage_transit():
    form = ManageTransitForm()
    all_transits = get_all_transits()
    all_sites = get_all_sites()
    if form.edit.data:
        if 'transit' not in request.form:
            flash('Please select a transit to edit', 'danger')
        else:
            transit = request.form['transit']
            return redirect(url_for('edit_transit', transit=transit, emails=request.args.get('emails'), userType=request.args.get('userType'), username=request.args.get('username')))
    elif form.delete.data:
        if 'transit' not in request.form:
            flash('Please select a transit to delete', 'danger')
        else:
            transit = request.form['transit']
            transit = transit.split()
            transit_route = transit[0]
            transit_type = transit[1]

            # Create cursor
            cur = mysql.connection.cursor()

            # Delete transit from transit table
            cur.execute("DELETE FROM transit WHERE transit_route=%s and transit_type=%s", (transit_route, transit_type))
            
            # Commit to DB
            mysql.connection.commit()

            # Close connection
            cur.close()
            flash('Successfully Deleted Transit', 'success')
            return redirect(url_for('manage_transit', userType=request.args.get('userType'), username=request.args.get('username')))
    elif form.filter.data:
        transportType = form.transportType.data
        route = form.route.data
        minPrice = form.minPrice.data
        maxPrice = form.maxPrice.data

        # Check if min price field was left blank. Default to 0
        if minPrice == None:
            minPrice = 0
        # Check if max price field was left blank. Default to large number
        if maxPrice == None:
            maxPrice = 100000000
        
        filtered_transits = []
        containSite = request.form.get('contain_site')
        if containSite == 'all' and transportType == 'all':
            if route == "":
                for transit in all_transits:
                    if transit['transit_price'] >= minPrice and transit['transit_price'] <= maxPrice:
                        filtered_transits.append(transit)
            else:
                for transit in all_transits:
                    if transit['transit_route'] == route and transit['transit_price'] >= minPrice and transit['transit_price'] <= maxPrice:
                        filtered_transits.append(transit)
        elif containSite == 'all' and transportType != 'all':
            if route == "":
                for transit in all_transits:
                    if transit['transit_type'] == transportType and transit['transit_price'] >= minPrice and transit['transit_price'] <= maxPrice:
                        filtered_transits.append(transit)
            else:
                for transit in all_transits:
                    if transit['transit_type'] == transportType and transit['transit_route'] == route and transit['transit_price'] >= minPrice and transit['transit_price'] <= maxPrice:
                        filtered_transits.append(transit)
        elif containSite != 'all' and transportType == 'all':
            # Create cursor
            cur = mysql.connection.cursor()

            # Query the transits that have this site.
            cur.execute("SELECT transit_type, transit_route FROM connect WHERE site_name=%s", (containSite,))
            transit_sites = cur.fetchall()

            needed_transits = []
            if route == "":
                for transit in transit_sites:
                    needed_transits.append(transit)
            else:
                for transit in transit_sites:
                    if transit['transit_route'] == route:
                        needed_transits.append(transit)
            for transit in all_transits:
                for comparison in needed_transits:
                    if transit['transit_route'] == comparison['transit_route'] and transit['transit_type'] == comparison['transit_type'] and transit['transit_price'] >= minPrice and transit['transit_price'] <= maxPrice:
                        filtered_transits.append(transit)            
                
            # Commit to DB
            mysql.connection.commit()

            # Close connection
            cur.close()
        else:
            # Create cursor
            cur = mysql.connection.cursor()

            # Query the transits that have this site.
            cur.execute("SELECT transit_type, transit_route FROM connect WHERE site_name=%s", (containSite,))
            transit_sites = cur.fetchall()

            needed_transits = []
            if route == "":
                for transit in transit_sites:
                    if transit['transit_type'] == transportType:
                        needed_transits.append(transit)
            else:
                for transit in transit_sites:
                    if transit['transit_route'] == route and transit['transit_type'] == transportType:
                        needed_transits.append(transit)
            for transit in all_transits:
                for comparison in needed_transits:
                    if transit['transit_route'] == comparison['transit_route'] and transit['transit_type'] == comparison['transit_type'] and transit['transit_price'] >= minPrice and transit['transit_price'] <= maxPrice:
                        filtered_transits.append(transit)                
            # Commit to DB
            mysql.connection.commit()

            # Close connection
            cur.close()
                
        return render_template('manage_transit.html', form=form, sites=all_sites, transits=filtered_transits, title='Manage Transit', legend='Manage Transit', emails=request.args.get('emails'), userType=request.args.get('userType'), username=request.args.get('username'))
    return render_template('manage_transit.html', sites=all_sites, transits=None, legend="Manage Transit", form=form, title='Manage Transit', emails=request.args.get('emails'), userType=request.args.get('userType'), username=request.args.get('username'))


## SCREEN 24
@app.route('/create_transit', methods=['GET','POST'])
def create_transit():
    form = TransitForm()
    all_sites = get_all_sites()
    if form.validate_on_submit() and request.method == 'POST': 
        transportType = form.transportType.data
        route = form.route.data 
        price = form.price.data
        connectedSites = request.form.getlist('all_sites')

        if len(connectedSites) < 2:
            flash("Please select at least 2 sites", 'danger')
            # return redirect(url_for('create_transit', emails=request.args.get('emails'), userType=request.args.get('userType'), username=request.args.get('username')))
            return render_template("create_transit.html", all_sites=all_sites, title='Create Transit', form=form, legend='Create Transit', emails=request.args.get('emails'), userType=request.args.get('userType'), username=request.args.get('username'))

         # Create cursor
        cur = mysql.connection.cursor()

        # Execute query
        cur.execute("INSERT INTO transit(transit_type, transit_route, transit_price) VALUES(%s, %s, %s)", (transportType, route, price))
        for site in connectedSites:
            cur.execute("INSERT INTO connect(site_name, transit_type, transit_route) VALUES(%s, %s, %s)", (site, transportType, route))

        # Commit to DB
        mysql.connection.commit()

        # Close connection
        cur.close()
        flash('Successfully Created Transit', 'success')
        return redirect(url_for('manage_transit', emails=request.args.get('emails'), userType=request.args.get('userType'), username=request.args.get('username')))
    return render_template("create_transit.html", all_sites=all_sites, title='Create Transit', form=form, legend='Create Transit', emails=request.args.get('emails'), userType=request.args.get('userType'), username=request.args.get('username'))

## SCREEN 23
@app.route('/edit_transit/<transit>', methods=['GET', 'POST'])
def edit_transit(transit):
    form = TransitForm()
    transit = transit.split()
    all_sites = get_all_sites()
    transit_route = transit[0]
    transit_type = transit[1]
    ## MUST WRITE QUERIES HERE
    if form.validate_on_submit() and request.method == 'POST':
        transportType = form.transportType.data 
        route = form.route.data 
        price = form.price.data
        connectedSites = request.form.getlist('all_sites')

        if len(connectedSites) < 2:
            flash("Please select at least 2 sites", 'danger')
            return render_template("create_transit.html", all_sites=all_sites, all_connected=connectedSites, title='Edit Transit', form=form, legend='Edit Transit', emails=request.args.get('emails'), userType=request.args.get('userType'), username=request.args.get('username'))

        # Create cursor
        cur = mysql.connection.cursor()

        # Execute queries
        # Store new connected sites within connect

        # cur.execute("UPDATE connect SET transit_type=%s and transit_route=%s WHERE site_name=%s and transit_type=%s and transit_route=%s", (transportType, route, site, transit_type, transit_route))
        cur.execute("SELECT site_name FROM connect WHERE transit_type=%s and transit_route=%s", (transit_type, transit_route))
        route_sites = cur.fetchall()

        # Putting all route_sites into a list by site_name
        route_site_names = []
        for site in route_sites:
            route_site_names.append(site['site_name'])

        # If a site in the newly connected sites list is not in the connect table, insert it into the connect table
        for site in connectedSites:
            if site not in route_site_names:
                cur.execute("INSERT INTO connect(transit_type, transit_route, site_name) VALUES(%s, %s, %s)", (transit_type, transit_route, site))
        # If a site is de-selected, remove it from connect
        for site in route_site_names:
            if site not in connectedSites:
                cur.execute("DELETE FROM connect WHERE site_name=%s and transit_type=%s and transit_route=%s", (site, transit_type, transit_route))
        # Store updated values into transit
        cur.execute("UPDATE transit SET transit_type=%s, transit_route=%s, transit_price=%s WHERE transit_type=%s and transit_route=%s", (transportType, route, price, transit_type, transit_route))

        # Commit to DB
        mysql.connection.commit()

        # Close connection
        cur.close()
        return redirect(url_for('manage_transit', emails=request.args.get('emails'), userType=request.args.get('userType'), username=request.args.get('username')))
    elif request.method == 'GET':
        # Create cursor
        cur = mysql.connection.cursor()

        cur.execute("SELECT transit_price FROM transit WHERE transit_route=%s and transit_type=%s", (transit_route, transit_type))
        t_price = cur.fetchone()
        transit_price = t_price['transit_price']

        # Retrieve all of the sites
        cur.execute("SELECT site_name FROM site")
        all_sites = cur.fetchall()
        # Retrieve sites the transit connects to
        cur.execute("SELECT site_name FROM connect WHERE transit_type=%s and transit_route=%s", (transit_type, transit_route))
        connected_sites = cur.fetchall()

        # Condense all_sites into a list with just the site_names
        all_sites_list = []
        for site in all_sites:
            all_sites_list.append(site['site_name'])
        
        # Condense connected_sites into a list
        all_connected = []
        for site in connected_sites:
            all_connected.append(site['site_name'])

        # Put the information from the transit onto the Edit Screen
        form.transportType.data = transit_type
        form.route.data = transit_route
        form.price.data = transit_price

        # Commit to DB
        mysql.connection.commit()

        # Close connection
        cur.close()
        return render_template("create_transit.html", all_sites=all_sites_list, all_connected=all_connected, title='Edit Transit', form=form, legend='Edit Transit', emails=request.args.get('emails'), userType=request.args.get('userType'), username=request.args.get('username')) 

## SCREEN 25 
@app.route('/manage_event', methods=["GET", "POST"])
def manage_event():
    form = ManageEvent()
    if form.validate_on_submit(): 
        name = form.name.data
        descriptionKeyword = form.descriptionKeyword.data
        startDate = form.startDate.data 
        endDate = form.endDate.data 
        minDurationRange = form.minDurationRange.data 
        maxDurationRange = form.maxDurationRange.data 
        minVisitsRange = form.minVisitsRange.data 
        maxVisitsRange = form.maxVisitsRange.data 
        minRevenueRange = form.minRevenueRange.data 
        maxRevenueRange = form.maxRevenueRange.data
    return render_template('manage_event.html', title="Manage Event", legend="Manage Event", form=form, userType=request.args.get('userType'), username=request.args.get('username'))

## SCREEN 26 
@app.route('/edit_event', methods=["GET", "POST"])
def edit_event(): 
    form = EditEvent()
    if form.validate_on_submit(): 
        name = form.name.data 
        price = form.price.data
        capacity = form.capacity.data
        minStaff = form.minStaff.data 
        startDate = form.startDate.data
        endDate = form.endDate.data 
        staffAssigned = form.staffAssigned.data
        description = form.description.data
        minVisitsRange = form.minVisitsRange.data 
        maxVisitsRange = form.maxVisitsRange.data 
        minRevenueRange = form.minRevenueRange.data 
        maxRevenueRange = form.maxRevenueRange.data
    return render_template("edit_event.html", title="Edit Event", legend ="Edit Event", form=form)

# Helper method to retrieve all available staff by first and last name


## SCREEN 27 
@app.route('/create_event', methods=['GET', 'POST'])
def create_event(): 
    form = EventForm()
    username = request.args['username']
    
    # Create cursor
    cur = mysql.connection.cursor()

    # Check if manager currently manages a site
    result = cur.execute("SELECT site_name FROM site WHERE manager_username=%s", (username,))
    if result == 0:
        flash("Manager cannot create an event because he or she doesn't manage a site", 'danger')
        return redirect(url_for('manage_event', userType=request.args.get('userType'), username=username))
    site_name = cur.fetchone()
    site_name = site_name['site_name']

    # Commit to DB
    mysql.connection.commit()

    # Close connection
    cur.close()
    staff_list = []
    if form.validate_on_submit():
        # Checks for if manager updates staff list
        if form.updateStaff.data:
            startDate = form.startDate.data
            endDate = form.endDate.data
            if endDate < startDate:
                flash('End Date cannot be before the Start Date', 'danger')
                return render_template("create_event.html", staff_list=staff_list, title="Create Event", form=form, userType=request.args.get('userType'), username=request.args.get('username'))
            minStaff = form.minStaff.data

            # Create cursor
            cur = mysql.connection.cursor()

            # Staff available
            cur.execute("SELECT username FROM staff WHERE username NOT IN (SELECT staff_username FROM assign_to)")
            unassigned_staff = cur.fetchall()
            
            temp_staff = []
            for staff in unassigned_staff:
                temp_staff.append(staff['username'])
            
            # Retrieve first and last name of unassigned staff members
            for staff in temp_staff:
                cur.execute("SELECT firstname, lastname from user WHERE username=%s", (staff,))
                name = cur.fetchone()                
                fullName = name['firstname'] + " " + name['lastname']
                staff_list.append(fullName)                            

            # Find staff assigned
            cur.execute("SELECT * FROM assign_to")
            staff_assigned = cur.fetchall()
            
            assigned_staff = []
            possible_duplicates = []
            for staff in staff_assigned:
                member = {}
                # Retrieve first and last name of assigned staff members
                cur.execute("SELECT firstname, lastname from user WHERE username=%s", (staff['staff_username'],))
                name = cur.fetchone()                
                fullName = name['firstname'] + " " + name['lastname']
                member['name'] = fullName
                member['start_date'] = staff['start_date']
                # Find the end date of the event the staff is assigned to
                cur.execute("SELECT end_date FROM event WHERE event_name=%s and start_date=%s and site_name=%s", (staff['event_name'], staff['start_date'], staff['site_name']))
                end_date = cur.fetchone()
                member['end_date'] = end_date['end_date']
                if fullName not in possible_duplicates:
                    assigned_staff.append(member)
                possible_duplicates.append(fullName)
            
            # See if staff members in assigned_staff are available for this new event
            for assigned in assigned_staff:
                if startDate > assigned['end_date'] or endDate < assigned['start_date']:
                    staff_list.append(assigned['name'])

            if len(staff_list) < minStaff:
                flash('Not enough available staff members', 'danger')
                return redirect(url_for('manage_event', userType=request.args.get('userType'), username=request.args.get('username')))

            # Commit to DB
            mysql.connection.commit()

            # Close connection
            cur.close()
            return render_template("create_event.html", staff_list=staff_list, title="Create Event", form=form, userType=request.args.get('userType'), username=request.args.get('username'))
        elif form.submit.data:
            name = form.name.data
            price = form.price.data
            capacity = form.capacity.data
            minStaff = form.minStaff.data
            startDate = form.startDate.data
            endDate = form.endDate.data
            description = form.description.data
            assign_staff = request.form.getlist('assign_staff')

            # Check if len of staff is greater than min staff required
            if len(assign_staff) < minStaff:
                flash('Cannot assign number of staff under the Minimum Staff Required', 'danger')
                return render_template("create_event.html", staff_list=staff_list, title="Create Event", form=form, userType=request.args.get('userType'), username=request.args.get('username'))
            
            # Create cursor
            cur = mysql.connection.cursor()

            # Check if event overlaps with another event
            cur.execute("SELECT site_name, start_date, end_date FROM event")
            possible_overlaps = cur.fetchall()
            
            for possible in possible_overlaps:
                if possible['site_name'] == site_name:
                    if startDate >= possible['start_date'] and startDate <= possible['end_date'] or endDate >= possible['start_date'] and endDate <= possible['end_date']:
                        flash('Cannot schedule an event that overlaps with another at the same site', 'danger')
                        return render_template("create_event.html", staff_list=staff_list, title="Create Event", form=form, userType=request.args.get('userType'), username=request.args.get('username'))

            # Enter information for the new event
            cur.execute("INSERT INTO event(event_name, start_date, site_name, min_staff_req, description, capacity, price, end_date) VALUES(%s, %s, %s, %s, %s, %s, %s, %s)", (name, startDate, site_name, minStaff, description, capacity, price, endDate))

            # Enter information for assign_to
            for staff in assign_staff:
                staff_name = staff.split()
                firstname = staff_name[0]
                lastname = staff_name[1]
                cur.execute("SELECT username FROM user WHERE firstname=%s and lastname=%s", (firstname, lastname))
                username = cur.fetchone()
                username = username['username']
                cur.execute("INSERT INTO assign_to(staff_username, event_name, start_date, site_name) VALUES(%s, %s, %s, %s)", (username, name, startDate, site_name))
                         
            # Commit to DB
            mysql.connection.commit()

            # Close connection
            cur.close()
            flash('Successfully Created Event', 'success')
            return redirect(url_for('manage_event', userType=request.args.get('userType'), username=request.args.get('username')))
    return render_template("create_event.html", staff_list=staff_list, title="Create Event", form=form, userType=request.args.get('userType'), username=request.args.get('username'))

## SCREEN 28 
@app.route('/manage_staff', methods=['GET', 'POST'])
def manage_staff(): 
    form = ManageStaff()
    staff = [("Peter Han", 3), ("Timmy Wu", 2)]
    return render_template("manage_staff.html", title="Manage Staff", legend="Manage Staff", form=form, staff=staff)

## SCREEN 29 
@app.route('/site_report', methods=['GET', 'POST'])
def site_report(): 
    form = SiteReport()
    return render_template("site_report.html", title="Site Report", legend="Site Report", form=form)

## SCREEN 30 
@app.route('/daily_detail', methods=["GET", "POST"])
def daily_detail(): 
    return render_template("daily_detail.html", title="Daily Detail", legend="Daily Detail")

## SCREEN 31
@app.route('/view_schedule', methods=["GET", "POST"])
def view_schedule(): 
    form = ViewSchedule()
    return render_template("view_schedule.html", title="View Schedule", legend="View Schedule", form=form)

## SCREEN 32 
@app.route('/staff_event_detail', methods=["GET", "POST"])
def staff_event_detail(): 
    event = {
            "eventName": "Walking Tour",
            "site": "Inman Park",
            "startDate": "2019-02-02",
            "endDate": "2019-02-02",
            "durationDays":1, 
            "staffAssigned": "Peter Han",
            "capacity":20, 
            "price":0,
            "description":"walking tour with Peter Han - very dangerous"
            }
    return render_template("staff_event_detail.html", title="Event Detail", legend="Event Detail", event=event)

## SCREEN 33 
@app.route('/explore_event', methods=['GET','POST'])
def explore_event(): 
    form = ExploreEvent()
    return render_template("explore_event.html", title="Explore Event", legend="Explore Event", form=form)

## SCREEN 34 
@app.route('/visitor_event_detail', methods=["GET","POST"])
def visitor_event_detail(): 
    form = VisitorEventDetail()
    event = {
            "eventName": "Walking Tour",
            "site": "Inman Park",
            "startDate": "2019-02-02",
            "endDate": "2019-02-02",
            "staffAssigned": "Peter Han", 
            "price":0,
            "ticketsRemaining":0,
            "description":"walking tour with Peter Han - very dangerous"
            }
    return render_template("visitor_event_detail.html", title="Event Detail", legend="Event Detail", form=form, event=event)

## SCREEN 35 
@app.route('/explore_site', methods=["GET", "POST"])
def explore_site(): 
    form = ExploreSite()
    return render_template("explore_site.html", title="Explore Site", legend="Explore Site", form = form)

## SCREEN 36 
@app.route('/transit_detail', methods=["GET","POST"])
def transit_detail(): 
    form = TransitDetail()
    return render_template("transit_detail.html", title="Transit Detail", legend="Transit Detail", form=form)

## SCREEN 37 
@app.route('/site_detail', methods=["GET","POST"])
def site_detail(): 
    form = SiteDetail() 
    return render_template("site_detail.html", title="Site Detail", legend="Site Detail", form=form)

## SCREEN 38 
@app.route('/visit_history', methods=['GET','POST'])
def visit_history(): 
    form = VisitHistory()
    return render_template("visit_history.html", title="Visit History", legend="Visit History", form=form)

if __name__ == '__main__':
    app.run(debug=True)