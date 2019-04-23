from flask import Flask, render_template, url_for, flash, redirect, session, request, jsonify
from flask_mysqldb import MySQL
from forms import UserRegistrationForm, LoginForm, VisitorRegistrationForm, EmployeeRegistrationForm, EmployeeVisitorRegistrationForm, TransitForm, EmailRegistrationForm, TransitForm, SiteForm, EventForm, ManageSiteForm, ManageTransitForm, ManageUser, ManageEvent, EditEvent, UserTakeTransit, TransitHistory, EmployeeProfileForm, ManageStaff, SiteReport, ViewSchedule, ExploreEvent, VisitorEventDetail, ExploreSite, TransitDetail, SiteDetail, VisitHistory
from passlib.hash import sha256_crypt
from random import randint
from datetime import datetime
import ast

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

        cur.execute("SELECT username FROM user")
        data = cur.fetchall()
        usernames = []
        for user in data: 
            usernames.append(user['username'])
        if username in usernames: 
            flash("Username already taken. Please give another username.", 'danger')
            return render_template('register_user.html', title='Register User', form=form)

        cur.execute("SELECT email FROM user_email")
        data = cur.fetchall()
        emails = []
        for e in data: 
            emails.append(e['email'])
        if email in emails: 
            flash("Email already taken. Please give another email.", 'danger')
            return render_template('register_user.html', title='Register User', form=form)

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

    filtered_users = []
    ## SORTING ## 
    if form.usernameUpSort.data:
        userList = request.form['user_name']
        userList = ast.literal_eval(userList)
        temp_users = []
        for user in userList:
            temp_users.append(user['username'])

        # Create cursor
        cur = mysql.connection.cursor()

        cur.execute("SELECT username, status, user_type FROM user ORDER BY username")
        results = cur.fetchall()
        for result in results:

            cur.execute("SELECT COUNT(*) FROM user_email WHERE username=%s", (result['username'],))
            email_count = cur.fetchone()
            result['email_count'] = email_count['COUNT(*)']
            if result['username'] in temp_users:
                filtered_users.append(result)
        

        # Commit to DB
        mysql.connection.commit()
        # Close connection
        cur.close()
        
        return render_template('manage_user.html', all_users=filtered_users, title="Manage User", legend="Manage User", form=form, emails=request.args.get('emails'), userType=request.args.get('userType'), username=request.args.get('username'))
    if form.usernameDownSort.data:
        userList = request.form['user_name']
        userList = ast.literal_eval(userList)
        temp_users = []
        for user in userList:
            temp_users.append(user['username'])

        # Create cursor
        cur = mysql.connection.cursor()

        cur.execute("SELECT username, status, user_type FROM user ORDER BY username DESC")
        results = cur.fetchall()
        for result in results:

            cur.execute("SELECT COUNT(*) FROM user_email WHERE username=%s", (result['username'],))
            email_count = cur.fetchone()['COUNT(*)']
            result['email_count'] = email_count
            if result['username'] in temp_users:
                filtered_users.append(result)
        

        # Commit to DB
        mysql.connection.commit()
        # Close connection
        cur.close()
        
        return render_template('manage_user.html', all_users=filtered_users, title="Manage User", legend="Manage User", form=form, emails=request.args.get('emails'), userType=request.args.get('userType'), username=request.args.get('username'))
    if form.emailUpSort.data:
        userList = request.form['user_name']
        userList = ast.literal_eval(userList)
        temp_users = []
        for user in userList:
            temp_users.append(user['username'])

        # Create cursor
        cur = mysql.connection.cursor()

        # cur.execute("SELECT username, status, user_type FROM user ORDER BY username")
        cur.execute("SELECT username, status, user_type FROM user ORDER BY username")
        results = cur.fetchall()
        for result in results:

            cur.execute("SELECT COUNT(*) FROM user_email WHERE username=%s", (result['username'],))
            email_count = cur.fetchone()
            result['email_count'] = email_count['COUNT(*)']
            if result['username'] in temp_users:
                filtered_users.append(result)
        

        # Commit to DB
        mysql.connection.commit()
        # Close connection
        cur.close()
        
        return render_template('manage_user.html', all_users=filtered_users, title="Manage User", legend="Manage User", form=form, emails=request.args.get('emails'), userType=request.args.get('userType'), username=request.args.get('username'))
    if form.typeUpSort.data:
        userList = request.form['user_name']
        userList = ast.literal_eval(userList)
        temp_users = []
        for user in userList:
            temp_users.append(user['username'])

        # Create cursor
        cur = mysql.connection.cursor()

        # cur.execute("SELECT username, status, user_type FROM user ORDER BY username")
        cur.execute("SELECT username, status, user_type FROM user ORDER BY user_type")
        results = cur.fetchall()
        for result in results:

            cur.execute("SELECT COUNT(*) FROM user_email WHERE username=%s", (result['username'],))
            email_count = cur.fetchone()
            result['email_count'] = email_count['COUNT(*)']
            if result['username'] in temp_users:
                filtered_users.append(result)
        

        # Commit to DB
        mysql.connection.commit()
        # Close connection
        cur.close()
        
        return render_template('manage_user.html', all_users=filtered_users, title="Manage User", legend="Manage User", form=form, emails=request.args.get('emails'), userType=request.args.get('userType'), username=request.args.get('username'))
    if form.typeDownSort.data:
        userList = request.form['user_name']
        userList = ast.literal_eval(userList)
        temp_users = []
        for user in userList:
            temp_users.append(user['username'])

        # Create cursor
        cur = mysql.connection.cursor()

        cur.execute("SELECT username, status, user_type FROM user ORDER BY user_type DESC")
        results = cur.fetchall()
        for result in results:

            cur.execute("SELECT COUNT(*) FROM user_email WHERE username=%s", (result['username'],))
            email_count = cur.fetchone()['COUNT(*)']
            result['email_count'] = email_count
            if result['username'] in temp_users:
                filtered_users.append(result)
        

        # Commit to DB
        mysql.connection.commit()
        # Close connection
        cur.close()
        
        return render_template('manage_user.html', all_users=filtered_users, title="Manage User", legend="Manage User", form=form, emails=request.args.get('emails'), userType=request.args.get('userType'), username=request.args.get('username'))
    if form.statusUpSort.data:
        userList = request.form['user_name']
        userList = ast.literal_eval(userList)
        temp_users = []
        for user in userList:
            temp_users.append(user['username'])

        # Create cursor
        cur = mysql.connection.cursor()

        # cur.execute("SELECT username, status, user_type FROM user ORDER BY username")
        cur.execute("SELECT username, status, user_type FROM user ORDER BY status")
        results = cur.fetchall()
        for result in results:

            cur.execute("SELECT COUNT(*) FROM user_email WHERE username=%s", (result['username'],))
            email_count = cur.fetchone()
            result['email_count'] = email_count['COUNT(*)']
            if result['username'] in temp_users:
                filtered_users.append(result)
        

        # Commit to DB
        mysql.connection.commit()
        # Close connection
        cur.close()
        
        return render_template('manage_user.html', all_users=filtered_users, title="Manage User", legend="Manage User", form=form, emails=request.args.get('emails'), userType=request.args.get('userType'), username=request.args.get('username'))
    if form.statusDownSort.data:
        userList = request.form['user_name']
        userList = ast.literal_eval(userList)
        temp_users = []
        for user in userList:
            temp_users.append(user['username'])

        # Create cursor
        cur = mysql.connection.cursor()

        cur.execute("SELECT username, status, user_type FROM user ORDER BY status DESC")
        results = cur.fetchall()
        for result in results:

            cur.execute("SELECT COUNT(*) FROM user_email WHERE username=%s", (result['username'],))
            email_count = cur.fetchone()['COUNT(*)']
            result['email_count'] = email_count
            if result['username'] in temp_users:
                filtered_users.append(result)
        

        # Commit to DB
        mysql.connection.commit()
        # Close connection
        cur.close()
        
        return render_template('manage_user.html', all_users=filtered_users, title="Manage User", legend="Manage User", form=form, emails=request.args.get('emails'), userType=request.args.get('userType'), username=request.args.get('username'))
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
                            elif status == 'declined' and user['user_type'] == 'Declined':
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

    filtered_sites = []
    if form.upSort.data:
        sitesList = request.form['site_name']
        sitesList = ast.literal_eval(sitesList)
        temp_sites = []
        for site in sitesList:
            temp_sites.append(site['site'])

        # Create cursor
        cur = mysql.connection.cursor()


        cur.execute("SELECT site_name, manager_username, open_everyday FROM site ORDER BY site_name")
        results = cur.fetchall()
        for result in results:
            if result['open_everyday'] == 1:
                result['open_everyday'] = 'Yes'
            else:
                result['open_everyday'] = "No"
            cur.execute("SELECT firstname, lastname FROM user WHERE username=%s", (result['manager_username'],))
            name = cur.fetchone()
            fullName = name['firstname'] + " " + name['lastname']
            result['manager'] = fullName
            if result['site_name'] in temp_sites:
                result['site'] = result['site_name']
                filtered_sites.append(result)
        

        # Commit to DB
        mysql.connection.commit()
        # Close connection
        cur.close()
        
        return render_template('manage_site.html', form=form, sites=sites, sitesList=filtered_sites, title='Manage Navigation', legend='Manage Site', emails=request.args.get('emails'), userType=request.args.get('userType'), username=request.args.get('username'))
    if form.downSort.data:
        sitesList = request.form['site_name']
        sitesList = ast.literal_eval(sitesList)
        temp_sites = []
        for site in sitesList:
            temp_sites.append(site['site'])

        # Create cursor
        cur = mysql.connection.cursor()


        cur.execute("SELECT site_name, manager_username, open_everyday FROM site ORDER BY site_name DESC")
        results = cur.fetchall()

        for result in results:
            if result['open_everyday'] == 1:
                result['open_everyday'] = 'Yes'
            else:
                result['open_everyday'] = "No"
            cur.execute("SELECT firstname, lastname FROM user WHERE username=%s", (result['manager_username'],))
            name = cur.fetchone()
            fullName = name['firstname'] + " " + name['lastname']
            result['manager'] = fullName
            if result['site_name'] in temp_sites:
                result['site'] = result['site_name']
                filtered_sites.append(result)
        

        # Commit to DB
        mysql.connection.commit()
        # Close connection
        cur.close()
        
        return render_template('manage_site.html', form=form, sites=sites, sitesList=filtered_sites, title='Manage Navigation', legend='Manage Site', emails=request.args.get('emails'), userType=request.args.get('userType'), username=request.args.get('username'))
    if form.managerUpSort.data:
        sitesList = request.form['site_name']
        sitesList = ast.literal_eval(sitesList)
        temp_managers = []
        for site in sitesList:
            temp_managers.append(site['manager'])
        # Create cursor
        cur = mysql.connection.cursor()


        cur.execute("SELECT site_name, manager_username, open_everyday FROM site ORDER BY manager_username ASC")
        results = cur.fetchall()

        for result in results:
            if result['open_everyday'] == 1:
                result['open_everyday'] = 'Yes'
            else:
                result['open_everyday'] = "No"
            cur.execute("SELECT firstname, lastname FROM user WHERE username=%s", (result['manager_username'],))
            name = cur.fetchone()
            fullName = name['firstname'] + " " + name['lastname']
            result['manager'] = fullName
            if result['manager'] in temp_managers:
                result['site'] = result['site_name']
                filtered_sites.append(result)
        

        # Commit to DB
        mysql.connection.commit()
        # Close connection
        cur.close()
        return render_template('manage_site.html', form=form, sites=sites, sitesList=filtered_sites, title='Manage Navigation', legend='Manage Site', emails=request.args.get('emails'), userType=request.args.get('userType'), username=request.args.get('username'))
    if form.managerDownSort.data:
        sitesList = request.form['site_name']
        sitesList = ast.literal_eval(sitesList)
        temp_managers = []
        for site in sitesList:
            temp_managers.append(site['manager'])
        # Create cursor
        cur = mysql.connection.cursor()


        cur.execute("SELECT site_name, manager_username, open_everyday FROM site ORDER BY manager_username DESC")
        results = cur.fetchall()

        for result in results:
            if result['open_everyday'] == 1:
                result['open_everyday'] = 'Yes'
            else:
                result['open_everyday'] = "No"
            cur.execute("SELECT firstname, lastname FROM user WHERE username=%s", (result['manager_username'],))
            name = cur.fetchone()
            fullName = name['firstname'] + " " + name['lastname']
            result['manager'] = fullName
            if result['manager'] in temp_managers:
                result['site'] = result['site_name']
                filtered_sites.append(result)
        

        # Commit to DB
        mysql.connection.commit()
        # Close connection
        cur.close()
        return render_template('manage_site.html', form=form, sites=sites, sitesList=filtered_sites, title='Manage Navigation', legend='Manage Site', emails=request.args.get('emails'), userType=request.args.get('userType'), username=request.args.get('username'))
    if form.openUpSort.data:
        sitesList = request.form['site_name']
        sitesList = ast.literal_eval(sitesList)
        temp_managers = []
        for site in sitesList:
            temp_managers.append(site['manager'])
        # Create cursor
        cur = mysql.connection.cursor()


        cur.execute("SELECT site_name, manager_username, open_everyday FROM site ORDER BY open_everyday ASC")
        results = cur.fetchall()

        for result in results:
            if result['open_everyday'] == 1:
                result['open_everyday'] = 'Yes'
            else:
                result['open_everyday'] = "No"
            cur.execute("SELECT firstname, lastname FROM user WHERE username=%s", (result['manager_username'],))
            name = cur.fetchone()
            fullName = name['firstname'] + " " + name['lastname']
            result['manager'] = fullName
            if result['manager'] in temp_managers:
                result['site'] = result['site_name']
                filtered_sites.append(result)
        

        # Commit to DB
        mysql.connection.commit()
        # Close connection
        cur.close()
        return render_template('manage_site.html', form=form, sites=sites, sitesList=filtered_sites, title='Manage Navigation', legend='Manage Site', emails=request.args.get('emails'), userType=request.args.get('userType'), username=request.args.get('username'))
    if form.openDownSort.data:
        sitesList = request.form['site_name']
        sitesList = ast.literal_eval(sitesList)
        temp_managers = []
        for site in sitesList:
            temp_managers.append(site['manager'])
        # Create cursor
        cur = mysql.connection.cursor()


        cur.execute("SELECT site_name, manager_username, open_everyday FROM site ORDER BY open_everyday DESC")
        results = cur.fetchall()

        for result in results:
            if result['open_everyday'] == 1:
                result['open_everyday'] = 'Yes'
            else:
                result['open_everyday'] = "No"
            cur.execute("SELECT firstname, lastname FROM user WHERE username=%s", (result['manager_username'],))
            name = cur.fetchone()
            fullName = name['firstname'] + " " + name['lastname']
            result['manager'] = fullName
            if result['manager'] in temp_managers:
                result['site'] = result['site_name']
                filtered_sites.append(result)
        

        # Commit to DB
        mysql.connection.commit()
        # Close connection
        cur.close()
        return render_template('manage_site.html', form=form, sites=sites, sitesList=filtered_sites, title='Manage Navigation', legend='Manage Site', emails=request.args.get('emails'), userType=request.args.get('userType'), username=request.args.get('username'))
    if form.validate_on_submit():
        if form.filter.data:
            site = request.form['sitesDrop']
            managers = request.form.get('managers')
            openEveryDay = form.openEveryDay.data
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
    return render_template('manage_site.html', form=form, sites=sites, sitesList=filtered_sites, title='Manage Navigation', legend='Manage Site', emails=request.args.get('emails'), userType=request.args.get('userType'), username=request.args.get('username'))


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

        if manager_username != manager_username: 
            cur.execute("UPDATE site SET manager_username=%s, zipcode=%s, address=%s, open_everyday=%s WHERE site_name=%s", (new_manager, zipcode, address, openEveryday, site_name))
        else: 
            cur.execute("UPDATE site SET zipcode=%s, address=%s, open_everyday=%s WHERE site_name=%s", (zipcode, address, openEveryday, site_name))
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

# Helper method to retrieve all events
def get_all_events(username):
    # Create cursor
    cur = mysql.connection.cursor()

    # Query event information from event table
    cur.execute("SELECT * FROM event WHERE site_name IN (SELECT site_name FROM site WHERE manager_username=%s)", (username,))
    events = cur.fetchall()

    # Retrieve needed information
    for event in events:
        event['duration'] = event['end_date'] - event['start_date']
        split = str(event['duration']).split()
        if split[0] != '0:00:00':
            duration = int(split[0]) + 1
        else:
            duration = 1    
        event['duration'] = duration
        cur.execute("SELECT COUNT(*) FROM assign_to WHERE event_name=%s and start_date=%s and site_name=%s", (event['event_name'], event['start_date'], event['site_name']))
        staff_count = cur.fetchone()
        staff_count = staff_count['COUNT(*)']
        event['staff_count'] = staff_count

    # Commit to DB
    mysql.connection.commit()

    # Close connection
    cur.close()
    return events

def event_visits_revenue(all_events):
    # Create cursor
    cur = mysql.connection.cursor()

    for event in all_events:
        # Retrieve total visits
        cur.execute("SELECT COUNT(*) FROM visit_event WHERE event_name=%s and start_date=%s and site_name=%s", (event['event_name'], event['start_date'], event['site_name']))
        visit_count = cur.fetchone()['COUNT(*)']
        
        # Retrieve price for the event
        cur.execute("SELECT price FROM event WHERE event_name=%s and start_date=%s and site_name=%s", (event['event_name'], event['start_date'], event['site_name']))
        price = cur.fetchone()['price']

        total_revenue = visit_count * price

        event['total_visits'] = visit_count
        event['total_revenue'] = total_revenue


    # Commit to DB
    mysql.connection.commit()

    # Close connection
    cur.close()
    return all_events

## SCREEN 25 
@app.route('/manage_event', methods=["GET", "POST"])
def manage_event():
    form = ManageEvent()
    username = request.args['username']
    all_events = get_all_events(username)
    all_events = event_visits_revenue(all_events)
    filtered_events = []

    if form.viewEdit.data:
        if 'event_name' not in request.form:
            flash('Please select an event to edit', 'danger')
        else:
            event_name = request.form['event_name']
            query = "start_date " + event_name 
            start_date = request.form[query]
            query2 = "site_name " + event_name
            site_name = request.form[query2]
            return redirect(url_for('edit_event', event_name=event_name, start_date=start_date, site_name=site_name, emails=request.args.get('emails'), userType=request.args.get('userType'), username=request.args.get('username')))
    elif form.filter.data:
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

        if minDurationRange == None:
            minDurationRange = 0
        if minVisitsRange == None:
            minVisitsRange = 0
        if minRevenueRange == None:
            minRevenueRange = 0
        if maxDurationRange == None:
            maxDurationRange = 100000000
        if maxVisitsRange == None:
            maxVisitsRange = 100000000
        if maxRevenueRange == None:
            maxRevenueRange = 100000000

        for event in all_events:
            if name == "":
                if descriptionKeyword == "":
                    if startDate == None and endDate == None:
                        filtered_events = all_events
                    elif startDate != None and endDate == None:
                        if event['start_date'] >= startDate:
                            filtered_events.append(event)
                    elif startDate == None and endDate != None:
                        if event['end_date'] <= endDate:
                            filtered_events.append(event)
                    else:
                        if event['start_date'] >= startDate and event['end_date'] <= endDate:
                            filtered_events.append(event)
                else:
                    if descriptionKeyword.lower() in event['description'].lower():
                        if startDate == None and endDate == None:
                            filtered_events.append(event)
                        elif startDate != None and endDate == None:
                            if event['start_date'] >= startDate:
                                filtered_events.append(event)
                        elif startDate == None and endDate != None:
                            if event['end_date'] <= endDate:
                                filtered_events.append(event)
                        else:
                            if event['start_date'] >= startDate and event['end_date'] <= endDate:
                                filtered_events.append(event)
            else:
                if name.lower() in event['event_name'].lower():
                    if descriptionKeyword == "":
                        if startDate == None and endDate == None:
                            filtered_events.append(event)
                        elif startDate != None and endDate == None:
                            if event['start_date'] >= startDate:
                                filtered_events.append(event)
                        elif startDate == None and endDate != None:
                            if event['end_date'] <= endDate:
                                filtered_events.append(event)
                        else:
                            if event['start_date'] >= startDate and event['end_date'] <= endDate:
                                filtered_events.append(event)
                    else:
                        if descriptionKeyword.lower() in event['description'].lower():
                            if startDate == None and endDate == None:
                                filtered_events.append(event)
                            elif startDate != None and endDate == None:
                                if event['start_date'] >= startDate:
                                    filtered_events.append(event)
                            elif startDate == None and endDate != None:
                                if event['end_date'] <= endDate:
                                    filtered_events.append(event)
                            else:
                                if event['start_date'] >= startDate and event['end_date'] <= endDate:
                                    filtered_events.append(event)

    return render_template('manage_event.html', events=filtered_events, title="Manage Event", legend="Manage Event", form=form, userType=request.args.get('userType'), username=request.args.get('username'))

## SCREEN 26 
@app.route('/edit_event', methods=["GET", "POST"])
def edit_event(): 
    form = EditEvent()
    event_name = request.args['event_name']
    start_date = request.args['start_date']
    site_name = request.args['site_name']
    
    # Create cursor
    cur = mysql.connection.cursor()

    # Retrieve all of this event's information
    cur.execute("SELECT * FROM event WHERE event_name=%s and start_date=%s and site_name=%s", (event_name, start_date, site_name))
    event = cur.fetchone()

    # Commit to DB
    mysql.connection.commit()

    # Close connection
    cur.close()
    
    staff_list = []
    if request.method == 'GET':
        form.description.data = event['description']
    startDate = event['start_date']
    endDate = event['end_date']
    minStaff = event['min_staff_req']

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
    
    # Find availability of staff assigned to other events
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

    selected_staff = []
    # Select currently assigned staff
    cur.execute("SELECT staff_username FROM assign_to WHERE event_name=%s and start_date=%s and site_name=%s", (event['event_name'], event['start_date'], event['site_name']))
    event_staff = cur.fetchall()
    for staff in event_staff:
        # Retrieve first and last name of assigned staff members
        cur.execute("SELECT firstname, lastname from user WHERE username=%s", (staff['staff_username'],))
        name = cur.fetchone()                
        fullName = name['firstname'] + " " + name['lastname']
        selected_staff.append(fullName)
        staff_list.append(fullName)

    # if len(staff_list) < minStaff:
    #     flash('Not enough available staff members', 'danger')
    #     return redirect(url_for('manage_event', userType=request.args.get('userType'), username=request.args.get('username')))

    cur.execute("SELECT visit_event_date, count(*) as visits FROM visit_event WHERE event_name=%s GROUP BY visit_event_date", (event['event_name'],))
    dailyResults = cur.fetchall()
    cur.execute("SELECT price FROM event WHERE event_name=%s",(event['event_name'],))
    price = cur.fetchone()
    price = price['price']

    for day in dailyResults: 
        day['price'] = day['visits'] * price

    # Commit to DB
    mysql.connection.commit()

    # Close connection
    cur.close()

    if form.update.data:
        description = form.description.data
        minStaff = event['min_staff_req']
        assign_staff = request.form.getlist('assign_staff')

        # Check if len of staff is greater than min staff required
        if len(assign_staff) < minStaff:
            flash('Cannot assign number of staff under the Minimum Staff Required', 'danger')
            return render_template("edit_event.html", results = dailyResults, event=event, assigned_staff=selected_staff, staff_list=staff_list, title="Create Event", form=form, userType=request.args.get('userType'), username=request.args.get('username'))
        
        # Create cursor
        cur = mysql.connection.cursor()

        # Update event information
        cur.execute("UPDATE event SET description=%s WHERE event_name=%s and start_date=%s and site_name=%s", (description, event['event_name'], event['start_date'], event['site_name']))        

        # Update assign_to information for staff members
        cur.execute("SELECT staff_username FROM assign_to WHERE event_name=%s and start_date=%s and site_name=%s", (event['event_name'], event['start_date'], event['site_name']))
        event_staff = cur.fetchall()
        
        # Staff assigned to the event
        staff_names = []
        for staff in event_staff:
            # Retrieve first and last name of assigned staff members
            cur.execute("SELECT firstname, lastname from user WHERE username=%s", (staff['staff_username'],))
            name = cur.fetchone()
            fullName = name['firstname'] + " " + name['lastname']
            staff_names.append(fullName)

        # If a staff member in the event is not in the assign_to table, insert the member into the assign_to table
        for staff in assign_staff:
            staff_name = staff.split()
            firstname = staff_name[0]
            lastname = staff_name[1]
            if staff not in staff_names:
                cur.execute("SELECT username FROM user WHERE firstname=%s and lastname=%s", (firstname, lastname))
                staff_username = cur.fetchone()
                cur.execute("INSERT INTO assign_to(staff_username, event_name, start_date, site_name) VALUES(%s, %s, %s, %s)", (staff_username['username'], event['event_name'], event['start_date'], event['site_name']))
        # If a staff member is de-selected, remove the member from assign_to
        for staff in staff_names:
            staff_name = staff.split()
            firstname = staff_name[0]
            lastname = staff_name[1]
            if staff not in assign_staff:
                cur.execute("SELECT username FROM user WHERE firstname=%s and lastname=%s", (firstname, lastname))
                staff_username = cur.fetchone()
                cur.execute("DELETE FROM assign_to WHERE staff_username=%s and event_name=%s and start_date=%s and site_name=%s", (staff_username['username'], event['event_name'], event['start_date'], event['site_name']))

        # Commit to DB
        mysql.connection.commit()

        # Close connection
        cur.close()
        flash('Successfully Updated Event', 'success')
        # return render_template("edit_event.html", event=event, staff_list=staff_list, assigned_staff=selected_staff, title="Edit Event", legend ="Edit Event", form=form, userType=request.args.get('userType'), username=request.args.get('username'))
        return redirect(url_for('edit_event', results = dailyResults, event_name=event_name, start_date=start_date, site_name=site_name ,userType=request.args.get('userType'), username=request.args.get('username')))
        # return redir("edit_event.html", event=event, assigned_staff=selected_staff, staff_list=staff_list, title="Create Event", form=form, userType=request.args.get('userType'), username=request.args.get('username'))
    elif form.filter.data:
        # name = form.name.data 
        # price = form.price.data
        # capacity = form.capacity.data
        # minStaff = form.minStaff.data 
        # startDate = form.startDate.data
        # endDate = form.endDate.data 
        # staffAssigned = form.staffAssigned.data
        # description = form.description.data
        minVisitsRange = form.minVisitsRange.data 
        maxVisitsRange = form.maxVisitsRange.data 
        minRevenueRange = form.minRevenueRange.data 
        maxRevenueRange = form.maxRevenueRange.data
        newResults = []
        if minVisitsRange != None and maxVisitsRange != None and minRevenueRange == None and maxRevenueRange == None: 
            for item in dailyResults: 
                if item['visits'] >= int(minVisitsRange) and item['visits'] <= int(maxVisitsRange): 
                    newResults.append(item)
        elif minVisitsRange == None and maxVisitsRange == None and minRevenueRange != None and maxRevenueRange != None:  
            for item in dailyResults: 
                if item['price'] >= float(minRevenueRange) and item['price'] <= float(maxRevenueRange): 
                    newResults.append(item)
        elif minVisitsRange != None and maxVisitsRange == None and minRevenueRange == None and maxRevenueRange == None:  
            for item in dailyResults: 
                if item['price'] >= float(minRevenueRange): 
                    newResults.append(item)
        elif minVisitsRange == None and maxVisitsRange != None and minRevenueRange == None and maxRevenueRange == None:  
            for item in dailyResults: 
                if item['price'] <= float(maxRevenueRange): 
                    newResults.append(item)
        elif minVisitsRange == None and maxVisitsRange == None and minRevenueRange != None and maxRevenueRange == None:  
            for item in dailyResults: 
                if item['price'] >= float(minRevenueRange): 
                    newResults.append(item)
        elif minVisitsRange == None and maxVisitsRange == None and minRevenueRange == None and maxRevenueRange != None:  
            for item in dailyResults: 
                if item['price'] <= float(maxRevenueRange): 
                    newResults.append(item)
        elif minVisitsRange != None and maxVisitsRange != None and minRevenueRange != None and maxRevenueRange != None:  
            for item in dailyResults: 
                if item['price'] >= float(minRevenueRange) and item['price'] <= float(maxRevenueRange) and item['visits'] >= int(minVisitsRange) and item['visits'] <= int(maxVisitsRange): 
                    newResults.append(item)
        elif minVisitsRange == None and maxVisitsRange == None and minRevenueRange == None and maxRevenueRange == None:  
            for item in dailyResults: 
                newResults.append(item)
        
        form.minVisitsRange.data = minVisitsRange
        form.maxVisitsRange.data = maxVisitsRange
        form.minRevenueRange.data = minRevenueRange
        form.maxRevenueRange.data = maxRevenueRange

        return render_template("edit_event.html", results = newResults, event=event, staff_list=staff_list, assigned_staff=selected_staff, title="Edit Event", legend ="Edit Event", form=form, userType=request.args.get('userType'), username=request.args.get('username'))
    return render_template("edit_event.html", results = dailyResults, event=event, staff_list=staff_list, assigned_staff=selected_staff, title="Edit Event", legend ="Edit Event", form=form, userType=request.args.get('userType'), username=request.args.get('username'))

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
    username = request.args['username']
    staff = []

    # Create cursor
    cur = mysql.connection.cursor()

    # Find the site for the manager
    cur.execute("SELECT site_name FROM site WHERE manager_username=%s", (username,))
    site_name = cur.fetchone()['site_name']

    # Find the staff assigned to this site
    cur.execute("SELECT staff_username FROM assign_to WHERE site_name=%s", (site_name,))
    staff_usernames = cur.fetchall()
    
    staff_names = set()
    for staff in staff_usernames:
        cur.execute("SELECT firstname, lastname FROM user WHERE username=%s", (staff['staff_username'],))
        name = cur.fetchone()
        firstname = name['firstname']
        lastname = name['lastname']
        fullName = firstname + " " + lastname
        staff_names.add(fullName)
    # Find the number of events the staff member is assigned to
    all_staff = []
    for staff in staff_names:
        member = {}
        staff_name = staff.split()
        cur.execute("SELECT username FROM user WHERE firstname=%s and lastname=%s", (staff_name[0].strip(), staff_name[1].strip()))
        username = cur.fetchone()['username']
        cur.execute("SELECT COUNT(*) FROM assign_to WHERE staff_username=%s", (username,))
        event_count = cur.fetchone()['COUNT(*)']
        member['name'] = staff
        member['event_count'] = event_count
        all_staff.append(member)

    # Commit to DB
    mysql.connection.commit()

    # Close connection
    cur.close()
    return render_template("manage_staff.html", all_staff=all_staff, site_name=site_name, title="Manage Staff", legend="Manage Staff", form=form, userType=request.args.get('userType'), username=request.args.get('username'))

# Helper method to retrieve site_information
def site_derived(all_sites):
    sites_information = []
    for site in all_sites:
        info = {}
        info['site_name'] = site
        # Create cursor
        cur = mysql.connection.cursor()

        # Find the number of events hosted at each site
        cur.execute("SELECT COUNT(*) FROM event WHERE site_name=%s", (site,))
        event_count = cur.fetchone()['COUNT(*)']
        info['event_count'] = event_count

        sites_information.append(info)

    # Commit to DB
    mysql.connection.commit()

    # Close connection
    cur.close()
    return sites_information

## SCREEN 29 
@app.route('/site_report', methods=['GET', 'POST'])
def site_report(): 
    form = SiteReport()
    username = request.args['username']
    # Create cursor
    cur = mysql.connection.cursor()

    cur.execute("SELECT site_name from site WHERE manager_username=%s", (username,))
    site_name = cur.fetchone()['site_name']

    # Commit to DB
    mysql.connection.commit()

    # Close connection
    cur.close()
    # sites_info = site_derived(all_sites)
    # return str(sites_info)
    filtered = []
    if form.filter.data:
        startDate = form.startDate.data
        endDate = form.endDate.data
        difference = endDate - startDate
        split = str(difference).split()
        number_days = int(split[0]) + 1

        if startDate > endDate:
            flash("End Date cannot be before Start Date", 'danger')
            return render_template("site_report.html", title="Site Report", legend="Site Report", form=form, userType=request.args.get('userType'), username=request.args.get('username'))

        # Create cursor
        cur = mysql.connection.cursor()

        # Find the event count
        cur.execute("SELECT event_name, start_date, end_date FROM event WHERE site_name=%s", (site_name,))
        events = cur.fetchall()
        
        increment_date = startDate
        tableList = []
        for i in range(number_days):
            event_count = 0
            row = {}
            row['day'] = increment_date
            cur.execute("SELECT DATE_ADD(%s, INTERVAL 1 DAY) AS Tomorrow", (increment_date,))
            day = cur.fetchone()

            event_visits = 0
            total_revenue = 0
            staff_count = 0
            for event in events:
                if increment_date >= event['start_date'] and increment_date <= event['end_date']:
                    event_count += 1
                    # Find staff count
                    cur.execute("SELECT COUNT(*) FROM assign_to WHERE event_name=%s and start_date=%s and site_name=%s", (event['event_name'], event['start_date'], site_name))
                    staff_count = cur.fetchone()['COUNT(*)']

                    # Find total visits to that event
                    cur.execute("SELECT COUNT(*) FROM visit_event WHERE event_name=%s and start_date=%s and site_name=%s and visit_event_date=%s", (event['event_name'], event['start_date'], site_name, increment_date))
                    total_visits = cur.fetchone()
                    event_visits += total_visits['COUNT(*)']

                    # Find revenue from visits
                    cur.execute("SELECT price FROM event WHERE event_name=%s and start_date=%s and site_name=%s", (event['event_name'], event['start_date'], site_name))
                    price = cur.fetchone()['price']
                    total_revenue += int(price) * event_visits
            # Find total visits to site
            cur.execute("SELECT COUNT(*) FROM visit_site WHERE site_name=%s and visit_start_date=%s", (site_name, increment_date))
            site_visits = cur.fetchone()['COUNT(*)']
            total_visits = event_visits + site_visits
            row['event_count'] = event_count
            row['staff_count'] = staff_count
            row['total_visits'] = total_visits
            row['total_revenue'] = total_revenue

            increment_date = day['Tomorrow']
            increment_date = datetime.strptime(increment_date, '%Y-%m-%d')
            increment_date = increment_date.date()
            tableList.append(row)
        
        # Filter
        minEventCount = form.minEventCount.data
        maxEventCount = form.maxEventCount.data
        minStaffCount = form.minStaffCount.data
        maxStaffCount = form.maxStaffCount.data
        minVisitsRange = form.minVisitsRange.data
        maxVisitsRange = form.maxVisitsRange.data
        minRevenueRange = form.minRevenueRange.data
        maxRevenueRange = form.maxRevenueRange.data

        if minEventCount == None:
            minEventCount = 0
        if minStaffCount == None:
            minStaffCount = 0
        if minVisitsRange == None:
            minVisitsRange = 0
        if minRevenueRange == None:
            minRevenueRange = 0
        if maxEventCount == None:
            maxEventCount = 100000000
        if maxStaffCount == None:
            maxStaffCount = 100000000
        if maxVisitsRange == None:
            maxVisitsRange = 100000000
        if maxRevenueRange == None:
            maxRevenueRange = 100000000


        for site in tableList:
            # Check site's event count
            if site['event_count'] >= minEventCount and site['event_count'] <= maxEventCount:
                if site['staff_count'] >= minStaffCount and site['event_count'] <= maxStaffCount:
                    if site['total_visits'] >= minVisitsRange and site['total_visits'] <= maxVisitsRange:
                        if site['total_revenue'] >= minRevenueRange and site['total_revenue'] <= maxRevenueRange:
                            filtered.append(site)

        # Commit to DB
        mysql.connection.commit()

        # Close connection
        cur.close()
        
    elif form.dailyDetail.data:
        if 'date' not in request.form:
            flash('Please select a date to view details', 'danger')
        else:
            date = request.form['date']
            return redirect(url_for('daily_detail', date=date, userType=request.args.get('userType'), username=request.args.get('username')))
    return render_template("site_report.html", tableList=filtered, title="Site Report", legend="Site Report", form=form, userType=request.args.get('userType'), username=request.args.get('username'))

## SCREEN 30 
@app.route('/daily_detail', methods=["GET", "POST"])
def daily_detail(): 
    username = request.args['username']
    date = request.args['date']
    increment_date = datetime.strptime(date, '%Y-%m-%d')
    increment_date = increment_date.date()

    cur = mysql.connection.cursor()

    cur.execute('SELECT event_name, start_date, end_date FROM event WHERE site_name = (SELECT site_name FROM site WHERE manager_username = %s)',(username,))
    events = cur.fetchall()

    filtered_daily = []
    for event in events:
        if increment_date >= event['start_date'] and increment_date <= event['end_date']:
            filtered_daily.append(event)
    
    dailyDetail = []
    for event in filtered_daily: 
        cur.execute("SELECT count(*) as num FROM visit_event WHERE event_name = %s and start_date = %s", (event['event_name'], event['start_date']))
        visits = cur.fetchone()
        visits = visits['num']
        event['visits'] = visits

        cur.execute("SELECT price FROM event WHERE event_name = %s and start_date = %s", (event['event_name'], event['start_date']))
        price = cur.fetchone()
        price = price['price'] 
        event['revenue'] = visits * price

        cur.execute("SELECT CONCAT(firstname, ' ', lastname) as fullname FROM user WHERE username in (SELECT staff_username FROM assign_to WHERE event_name = %s and start_date = %s) ORDER BY firstname ASC",(event['event_name'], event['start_date']))
        staff = cur.fetchall()
        staffList = [] 
        for s in staff: 
            staffList.append(s['fullname'])
        event['staffList'] = staffList
        dailyDetail.append(event)

    #return str(events)

    # Commit to DB
    mysql.connection.commit()

    # Close connection
    cur.close()

    return render_template("daily_detail.html", title="Daily Detail", legend="Daily Detail", events=dailyDetail, userType=request.args.get('userType'), username=request.args.get('username'))

## SCREEN 31
@app.route('/view_schedule', methods=["GET", "POST"])
def view_schedule(): 
    form = ViewSchedule()

    username = request.args['username']

    eventName = form.eventName.data 
    descriptionKeyword = form.descriptionKeyword.data 
    startDate = form.startDate.data 
    endDate = form.endDate.data

    results = []

    if form.filter.data:
        cur = mysql.connection.cursor()
        cur.execute("SELECT event_name, start_date, site_name FROM assign_to WHERE staff_username = %s", (username,))
        worksOn = cur.fetchall()

        eventsData = []
        for event in worksOn: 
            cur.execute("SELECT event_name, site_name, start_date, end_date, min_staff_req, description FROM event WHERE event_name = %s and start_date = %s and site_name = %s", (event['event_name'], event['start_date'], event['site_name']))
            data = cur.fetchone()
            eventsData.append(data)
        # Commit to DB
        mysql.connection.commit()

        # Close connection
        cur.close()

        for event in eventsData: 
            if eventName == '': 
                if descriptionKeyword == '': 
                    if startDate == None and endDate == None: ## EVERYTHING
                        results.append(event)
                    elif startDate != None and endDate != None: 
                        if event['start_date'] >= startDate and event['end_date'] <= endDate: 
                            results.append(event)
                    elif startDate != None and endDate == None: 
                        if event['start_date'] >= startDate: 
                            results.append(event)
                    elif startDate == None and endDate != None: 
                        if event['end_date'] <= endDate: 
                            results.append(event)
                else: 
                    if descriptionKeyword.lower() in event['description'].lower():
                        if startDate == None and endDate == None: 
                            results.append(event)
                        elif startDate != None and endDate != None: 
                            if event['start_date'] >= startDate and event['end_date'] <= endDate: 
                                results.append(event)
                        elif startDate != None and endDate == None: 
                            if event['start_date'] >= startDate: 
                                results.append(event)
                        elif startDate == None and endDate != None: 
                            if event['end_date'] <= endDate: 
                                results.append(event)
            else: # event_name is not empty 
                if eventName.lower() in event['event_name'].lower(): 
                    if descriptionKeyword == '': 
                        if startDate == None and endDate == None:
                            results.append(event)
                        elif startDate != None and endDate != None: 
                            if event['start_date'] >= startDate and event['end_date'] <= endDate: 
                                results.append(event)
                        elif startDate != None and endDate == None: 
                            if event['start_date'] >= startDate: 
                                results.append(event)
                        elif startDate == None and endDate != None: 
                            if event['end_date'] <= endDate: 
                                results.append(event)
                    elif descriptionKeyword.lower() in event['description'].lower():
                        if startDate == None and endDate == None: 
                            results.append(event)
                        elif startDate != None and endDate != None: 
                            if event['start_date'] >= startDate and event['end_date'] <= endDate: 
                                results.append(event)
                        elif startDate != None and endDate == None: 
                            if event['start_date'] >= startDate: 
                                results.append(event)
                        elif startDate == None and endDate != None: 
                            if event['end_date'] <= endDate: 
                                results.append(event)
               

        form.eventName.data = eventName 
        form.descriptionKeyword.data = descriptionKeyword
        form.startDate.data = startDate
        form.endDate.data = endDate

        return render_template("view_schedule.html", title="View Schedule", legend="View Schedule", results=results, form=form, userType=request.args.get('userType'), username=request.args.get('username'))
    if form.viewEvent.data:
        if 'event_name' not in request.form:
            flash('Must select an event to view', 'danger')
            form.eventName.data = eventName 
            form.descriptionKeyword.data = descriptionKeyword
            form.startDate.data = startDate
            form.endDate.data = endDate
            return render_template("view_schedule.html", title="View Schedule", legend="View Schedule", results=results, form=form, userType=request.args.get('userType'), username=request.args.get('username'))
        else: 
            event_name = request.form['event_name']
            query = "start_date " + event_name 
            start_date = request.form[query]
            query2 = "site_name " + event_name
            site_name = request.form[query2]
            return redirect(url_for('staff_event_detail', event_name=event_name, start_date=start_date, site_name=site_name, userType=request.args.get('userType'), username=request.args.get('username')))


    return render_template("view_schedule.html", title="View Schedule", legend="View Schedule", results=results, form=form, userType=request.args.get('userType'), username=request.args.get('username'))

## SCREEN 32 
@app.route('/staff_event_detail', methods=["GET", "POST"])
def staff_event_detail(): 
    

    username = request.args['username']
    event_name = request.args['event_name']
    start_date = request.args['start_date']
    site_name = request.args['site_name']

   
 
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM event WHERE event_name = %s and start_date = %s and site_name = %s", (event_name, start_date, site_name))
    event = cur.fetchone()
    
    cur.execute("SELECT CONCAT(firstname, ' ', lastname) as fullname FROM user WHERE username in (SELECT staff_username FROM assign_to WHERE event_name = %s and start_date = %s and site_name = %s) ORDER BY firstname ASC",(event_name, start_date, site_name))
    staff = cur.fetchall()
    staffList = [] 
    for s in staff: 
        staffList.append(s['fullname'])
    event['staffList'] = staffList

    event['duration'] = event['end_date'] - event['start_date']
    
    split = str(event['duration']).split()
    if split[0] != '0:00:00':
        duration = int(split[0]) + 1
    else:
        duration = 1
    event['duration'] = duration

    # Commit to DB  
    mysql.connection.commit()

    # Close connection
    cur.close()

    return render_template("staff_event_detail.html", title="Event Detail", legend="Event Detail", event=event, userType=request.args.get('userType'), username=request.args.get('username'))

# Helper method to calculate the total visits, tickets remaining, and my visits for the user
def get_event_derived(all_events, username):
    # Create cursor
    cur = mysql.connection.cursor()

    for event in all_events:
        # Calculate my visits for each event
        cur.execute("SELECT COUNT(*) FROM visit_event WHERE visitor_username=%s and event_name=%s and start_date=%s and site_name=%s", (username, event['event_name'], event['start_date'], event['site_name']))
        my_visits = cur.fetchone()['COUNT(*)']
        event['my_visits'] = my_visits

        # Calculate total visits for each event
        cur.execute("SELECT COUNT(*) FROM visit_event WHERE event_name=%s and start_date=%s and site_name=%s", (event['event_name'], event['start_date'], event['site_name']))
        total_visits = cur.fetchone()['COUNT(*)']
        event['total_visits'] = total_visits

        # Calculate tickets remaining for each event
        event['tickets_remaining'] = event['capacity'] - event['total_visits']

    # Commit to DB
    mysql.connection.commit()

    # Close connection
    cur.close()
    return all_events

## Helper to get all events
def get_events(username):
    # Create cursor
    cur = mysql.connection.cursor()

    # Query event information from event table
    cur.execute("SELECT * FROM event")
    events = cur.fetchall()

    # Retrieve needed information
    for event in events:
        event['duration'] = event['end_date'] - event['start_date']
        split = str(event['duration']).split()
        if split[0] != '0:00:00':
            duration = int(split[0]) + 1
        else:
            duration = 1    
        event['duration'] = duration
        cur.execute("SELECT COUNT(*) FROM assign_to WHERE event_name=%s and start_date=%s and site_name=%s", (event['event_name'], event['start_date'], event['site_name']))
        staff_count = cur.fetchone()
        staff_count = staff_count['COUNT(*)']
        event['staff_count'] = staff_count

        cur.execute("SELECT COUNT(*) FROM visit_event WHERE visitor_username=%s and event_name=%s", (username, event['event_name']))
        total_visits = cur.fetchone()['COUNT(*)']
        event['total_visits'] = total_visits

    # Commit to DB
    mysql.connection.commit()

    # Close connection
    cur.close()
    return events

## SCREEN 33 
@app.route('/explore_event', methods=['GET','POST'])
def explore_event(): 
    form = ExploreEvent()
    username = request.args['username']
    all_events = get_events(username)
    all_events = get_event_derived(all_events, username)
    all_sites = get_all_sites()
    # return str(event_derived)
    filtered_events = []

    if form.eventDetail.data:
        if 'event_name' not in request.form:
            flash('Please select an event to view details', 'danger')
        else:
            event_name = request.form['event_name']
            query = "start_date " + event_name 
            start_date = request.form[query]
            query2 = "site_name " + event_name
            site_name = request.form[query2]

            # Find tickets remaining for this event
            tickets_remaining = 0
            for event in all_events:
                if event['event_name'] == event_name and str(event['start_date']) == start_date and event['site_name'] == site_name:
                    tickets_remaining = event['tickets_remaining']

            return redirect(url_for('visitor_event_detail', tickets_remaining=tickets_remaining, event_name=event_name, start_date=start_date, site_name=site_name, emails=request.args.get('emails'), userType=request.args.get('userType'), username=request.args.get('username')))
    if form.filter.data:
        eventName = form.eventName.data
        descriptionKeyword = form.descriptionKeyword.data
        startDate = form.startDate.data
        endDate = form.endDate.data
        siteName = request.form.get('sitesDrop')
        minVisitsRange = form.minVisitsRange.data
        maxVisitsRange = form.maxVisitsRange.data
        minPriceRange = form.minPriceRange.data
        maxPriceRange = form.maxPriceRange.data
        includeVisited = form.includeVisited.data
        includeSoldOutEvent = form.includeSoldOutEvent.data

        if minVisitsRange == None:
            minVisitsRange = 0
        if minPriceRange == None:
            minRevenueRange = 0
        if maxVisitsRange == None:
            maxVisitsRange = 100000000
        if maxPriceRange == None:
            maxPriceRange = 100000000

        for event in all_events:
            if eventName == "":
                if descriptionKeyword == "":
                    if siteName == "all":
                        if startDate == None and endDate == None:
                            if event['total_visits'] >= minVisitsRange and event['total_visits'] <= maxVisitsRange:
                                if includeVisited == False and includeSoldOutEvent == False:
                                    filtered_events = all_events
                                elif includeVisited == True and includeSoldOutEvent == False:
                                    if event['my_visits'] > 0:
                                        filtered_events.append(event)
                                elif includeVisited == False and includeSoldOutEvent == True:
                                    if event['tickets_remaining'] == 0:
                                        filtered_events.append(event)
                                else:
                                    if event['my_visits'] > 0 and event['tickets_remaining'] == 0:
                                        filtered_events.append(event)
                        elif startDate != None and endDate == None:
                            if event['start_date'] >= startDate:
                                if event['total_visits'] >= minVisitsRange and event['total_visits'] <= maxVisitsRange:
                                    if includeVisited == False and includeSoldOutEvent == False:
                                        filtered_events.append(event)
                                    elif includeVisited == True and includeSoldOutEvent == False:
                                        if event['my_visits'] > 0:
                                            filtered_events.append(event)
                                    elif includeVisited == False and includeSoldOutEvent == True:
                                        if event['tickets_remaining'] == 0:
                                            filtered_events.append(event)
                                    else:
                                        if event['my_visits'] > 0 and event['tickets_remaining'] == 0:
                                            filtered_events.append(event)
                        elif startDate == None and endDate != None:
                            if event['end_date'] <= endDate:
                                if event['total_visits'] >= minVisitsRange and event['total_visits'] <= maxVisitsRange:
                                    if includeVisited == False and includeSoldOutEvent == False:
                                        filtered_events.append(event)
                                    elif includeVisited == True and includeSoldOutEvent == False:
                                        if event['my_visits'] > 0:
                                            filtered_events.append(event)
                                    elif includeVisited == False and includeSoldOutEvent == True:
                                        if event['tickets_remaining'] == 0:
                                            filtered_events.append(event)
                                    else:
                                        if event['my_visits'] > 0 and event['tickets_remaining'] == 0:
                                            filtered_events.append(event)
                        else:
                            if event['end_date'] <= endDate and event['start_date'] >= startDate:
                                if event['total_visits'] >= minVisitsRange and event['total_visits'] <= maxVisitsRange:
                                    if includeVisited == False and includeSoldOutEvent == False:
                                        filtered_events.append(event)
                                    elif includeVisited == True and includeSoldOutEvent == False:
                                        if event['my_visits'] > 0:
                                            filtered_events.append(event)
                                    elif includeVisited == False and includeSoldOutEvent == True:
                                        if event['tickets_remaining'] == 0:
                                            filtered_events.append(event)
                                    else:
                                        if event['my_visits'] > 0 and event['tickets_remaining'] == 0:
                                            filtered_events.append(event)
                    else:
                        if siteName.lower() in event['site_name'].lower():
                            if startDate == None and endDate == None:
                                if event['total_visits'] >= minVisitsRange and event['total_visits'] <= maxVisitsRange:
                                    if includeVisited == False and includeSoldOutEvent == False:
                                        filtered_events.append(event)
                                    elif includeVisited == True and includeSoldOutEvent == False:
                                        if event['my_visits'] > 0:
                                            filtered_events.append(event)
                                    elif includeVisited == False and includeSoldOutEvent == True:
                                        if event['tickets_remaining'] == 0:
                                            filtered_events.append(event)
                                    else:
                                        if event['my_visits'] > 0 and event['tickets_remaining'] == 0:
                                            filtered_events.append(event)
                                elif startDate != None and endDate == None:
                                    if event['start_date'] >= startDate:
                                        if event['total_visits'] >= minVisitsRange and event['total_visits'] <= maxVisitsRange:
                                            if includeVisited == False and includeSoldOutEvent == False:
                                                filtered_events.append(event)
                                            elif includeVisited == True and includeSoldOutEvent == False:
                                                if event['my_visits'] > 0:
                                                    filtered_events.append(event)
                                            elif includeVisited == False and includeSoldOutEvent == True:
                                                if event['tickets_remaining'] == 0:
                                                    filtered_events.append(event)
                                            else:
                                                if event['my_visits'] > 0 and event['tickets_remaining'] == 0:
                                                    filtered_events.append(event)
                                elif startDate == None and endDate != None:
                                    if event['end_date'] <= endDate:
                                        if event['total_visits'] >= minVisitsRange and event['total_visits'] <= maxVisitsRange:
                                            if includeVisited == False and includeSoldOutEvent == False:
                                                filtered_events.append(event)
                                            elif includeVisited == True and includeSoldOutEvent == False:
                                                if event['my_visits'] > 0:
                                                    filtered_events.append(event)
                                            elif includeVisited == False and includeSoldOutEvent == True:
                                                if event['tickets_remaining'] == 0:
                                                    filtered_events.append(event)
                                            else:
                                                if event['my_visits'] > 0 and event['tickets_remaining'] == 0:
                                                    filtered_events.append(event)
                                else:
                                    if event['end_date'] <= endDate and event['start_date'] >= startDate:
                                        if event['total_visits'] >= minVisitsRange and event['total_visits'] <= maxVisitsRange:
                                            if includeVisited == False and includeSoldOutEvent == False:
                                                filtered_events.append(event)
                                            elif includeVisited == True and includeSoldOutEvent == False:
                                                if event['my_visits'] > 0:
                                                    filtered_events.append(event)
                                            elif includeVisited == False and includeSoldOutEvent == True:
                                                if event['tickets_remaining'] == 0:
                                                    filtered_events.append(event)
                                            else:
                                                if event['my_visits'] > 0 and event['tickets_remaining'] == 0:
                                                    filtered_events.append(event)
                else:
                    if descriptionKeyword.lower() in event['description'].lower():
                        if siteName == "all":
                            if startDate == None and endDate == None:
                                if event['total_visits'] >= minVisitsRange and event['total_visits'] <= maxVisitsRange:
                                    if includeVisited == False and includeSoldOutEvent == False:
                                        filtered_events = all_events
                                    elif includeVisited == True and includeSoldOutEvent == False:
                                        if event['my_visits'] > 0:
                                            filtered_events.append(event)
                                    elif includeVisited == False and includeSoldOutEvent == True:
                                        if event['tickets_remaining'] == 0:
                                            filtered_events.append(event)
                                    else:
                                        if event['my_visits'] > 0 and event['tickets_remaining'] == 0:
                                            filtered_events.append(event)
                            elif startDate != None and endDate == None:
                                if event['start_date'] >= startDate:
                                    if event['total_visits'] >= minVisitsRange and event['total_visits'] <= maxVisitsRange:
                                        if includeVisited == False and includeSoldOutEvent == False:
                                            filtered_events.append(event)
                                        elif includeVisited == True and includeSoldOutEvent == False:
                                            if event['my_visits'] > 0:
                                                filtered_events.append(event)
                                        elif includeVisited == False and includeSoldOutEvent == True:
                                            if event['tickets_remaining'] == 0:
                                                filtered_events.append(event)
                                        else:
                                            if event['my_visits'] > 0 and event['tickets_remaining'] == 0:
                                                filtered_events.append(event)
                            elif startDate == None and endDate != None:
                                if event['end_date'] <= endDate:
                                    if event['total_visits'] >= minVisitsRange and event['total_visits'] <= maxVisitsRange:
                                        if includeVisited == False and includeSoldOutEvent == False:
                                            filtered_events.append(event)
                                        elif includeVisited == True and includeSoldOutEvent == False:
                                            if event['my_visits'] > 0:
                                                filtered_events.append(event)
                                        elif includeVisited == False and includeSoldOutEvent == True:
                                            if event['tickets_remaining'] == 0:
                                                filtered_events.append(event)
                                        else:
                                            if event['my_visits'] > 0 and event['tickets_remaining'] == 0:
                                                filtered_events.append(event)
                            else:
                                if event['end_date'] <= endDate and event['start_date'] >= startDate:
                                    if event['total_visits'] >= minVisitsRange and event['total_visits'] <= maxVisitsRange:
                                        if includeVisited == False and includeSoldOutEvent == False:
                                            filtered_events.append(event)
                                        elif includeVisited == True and includeSoldOutEvent == False:
                                            if event['my_visits'] > 0:
                                                filtered_events.append(event)
                                        elif includeVisited == False and includeSoldOutEvent == True:
                                            if event['tickets_remaining'] == 0:
                                                filtered_events.append(event)
                                        else:
                                            if event['my_visits'] > 0 and event['tickets_remaining'] == 0:
                                                filtered_events.append(event)
                        else:
                            if siteName.lower() in event['site_name'].lower():
                                if startDate == None and endDate == None:
                                    if event['total_visits'] >= minVisitsRange and event['total_visits'] <= maxVisitsRange:
                                        if includeVisited == False and includeSoldOutEvent == False:
                                            filtered_events.append(event)
                                        elif includeVisited == True and includeSoldOutEvent == False:
                                            if event['my_visits'] > 0:
                                                filtered_events.append(event)
                                        elif includeVisited == False and includeSoldOutEvent == True:
                                            if event['tickets_remaining'] == 0:
                                                filtered_events.append(event)
                                        else:
                                            if event['my_visits'] > 0 and event['tickets_remaining'] == 0:
                                                filtered_events.append(event)
                                    elif startDate != None and endDate == None:
                                        if event['start_date'] >= startDate:
                                            if event['total_visits'] >= minVisitsRange and event['total_visits'] <= maxVisitsRange:
                                                if includeVisited == False and includeSoldOutEvent == False:
                                                    filtered_events.append(event)
                                                elif includeVisited == True and includeSoldOutEvent == False:
                                                    if event['my_visits'] > 0:
                                                        filtered_events.append(event)
                                                elif includeVisited == False and includeSoldOutEvent == True:
                                                    if event['tickets_remaining'] == 0:
                                                        filtered_events.append(event)
                                                else:
                                                    if event['my_visits'] > 0 and event['tickets_remaining'] == 0:
                                                        filtered_events.append(event)
                                    elif startDate == None and endDate != None:
                                        if event['end_date'] <= endDate:
                                            if event['total_visits'] >= minVisitsRange and event['total_visits'] <= maxVisitsRange:
                                                if includeVisited == False and includeSoldOutEvent == False:
                                                    filtered_events.append(event)
                                                elif includeVisited == True and includeSoldOutEvent == False:
                                                    if event['my_visits'] > 0:
                                                        filtered_events.append(event)
                                                elif includeVisited == False and includeSoldOutEvent == True:
                                                    if event['tickets_remaining'] == 0:
                                                        filtered_events.append(event)
                                                else:
                                                    if event['my_visits'] > 0 and event['tickets_remaining'] == 0:
                                                        filtered_events.append(event)
                                    else:
                                        if event['end_date'] <= endDate and event['start_date'] >= startDate:
                                            if event['total_visits'] >= minVisitsRange and event['total_visits'] <= maxVisitsRange:
                                                if includeVisited == False and includeSoldOutEvent == False:
                                                    filtered_events.append(event)
                                                elif includeVisited == True and includeSoldOutEvent == False:
                                                    if event['my_visits'] > 0:
                                                        filtered_events.append(event)
                                                elif includeVisited == False and includeSoldOutEvent == True:
                                                    if event['tickets_remaining'] == 0:
                                                        filtered_events.append(event)
                                                else:
                                                    if event['my_visits'] > 0 and event['tickets_remaining'] == 0:
                                                        filtered_events.append(event)
            else:
                if descriptionKeyword == "":
                    if siteName == "all":
                        if startDate == None and endDate == None:
                            if event['total_visits'] >= minVisitsRange and event['total_visits'] <= maxVisitsRange:
                                if includeVisited == False and includeSoldOutEvent == False:
                                    filtered_events = all_events
                                elif includeVisited == True and includeSoldOutEvent == False:
                                    if event['my_visits'] > 0:
                                        filtered_events.append(event)
                                elif includeVisited == False and includeSoldOutEvent == True:
                                    if event['tickets_remaining'] == 0:
                                        filtered_events.append(event)
                                else:
                                    if event['my_visits'] > 0 and event['tickets_remaining'] == 0:
                                        filtered_events.append(event)
                        elif startDate != None and endDate == None:
                            if event['start_date'] >= startDate:
                                if event['total_visits'] >= minVisitsRange and event['total_visits'] <= maxVisitsRange:
                                    if includeVisited == False and includeSoldOutEvent == False:
                                        filtered_events.append(event)
                                    elif includeVisited == True and includeSoldOutEvent == False:
                                        if event['my_visits'] > 0:
                                            filtered_events.append(event)
                                    elif includeVisited == False and includeSoldOutEvent == True:
                                        if event['tickets_remaining'] == 0:
                                            filtered_events.append(event)
                                    else:
                                        if event['my_visits'] > 0 and event['tickets_remaining'] == 0:
                                            filtered_events.append(event)
                        elif startDate == None and endDate != None:
                            if event['end_date'] <= endDate:
                                if event['total_visits'] >= minVisitsRange and event['total_visits'] <= maxVisitsRange:
                                    if includeVisited == False and includeSoldOutEvent == False:
                                        filtered_events.append(event)
                                    elif includeVisited == True and includeSoldOutEvent == False:
                                        if event['my_visits'] > 0:
                                            filtered_events.append(event)
                                    elif includeVisited == False and includeSoldOutEvent == True:
                                        if event['tickets_remaining'] == 0:
                                            filtered_events.append(event)
                                    else:
                                        if event['my_visits'] > 0 and event['tickets_remaining'] == 0:
                                            filtered_events.append(event)
                        else:
                            if event['end_date'] <= endDate and event['start_date'] >= startDate:
                                if event['total_visits'] >= minVisitsRange and event['total_visits'] <= maxVisitsRange:
                                    if includeVisited == False and includeSoldOutEvent == False:
                                        filtered_events.append(event)
                                    elif includeVisited == True and includeSoldOutEvent == False:
                                        if event['my_visits'] > 0:
                                            filtered_events.append(event)
                                    elif includeVisited == False and includeSoldOutEvent == True:
                                        if event['tickets_remaining'] == 0:
                                            filtered_events.append(event)
                                    else:
                                        if event['my_visits'] > 0 and event['tickets_remaining'] == 0:
                                            filtered_events.append(event)
                    else:
                        if siteName.lower() in event['site_name'].lower():
                            if startDate == None and endDate == None:
                                if event['total_visits'] >= minVisitsRange and event['total_visits'] <= maxVisitsRange:
                                    if includeVisited == False and includeSoldOutEvent == False:
                                        filtered_events.append(event)
                                    elif includeVisited == True and includeSoldOutEvent == False:
                                        if event['my_visits'] > 0:
                                            filtered_events.append(event)
                                    elif includeVisited == False and includeSoldOutEvent == True:
                                        if event['tickets_remaining'] == 0:
                                            filtered_events.append(event)
                                    else:
                                        if event['my_visits'] > 0 and event['tickets_remaining'] == 0:
                                            filtered_events.append(event)
                                elif startDate != None and endDate == None:
                                    if event['start_date'] >= startDate:
                                        if event['total_visits'] >= minVisitsRange and event['total_visits'] <= maxVisitsRange:
                                            if includeVisited == False and includeSoldOutEvent == False:
                                                filtered_events.append(event)
                                            elif includeVisited == True and includeSoldOutEvent == False:
                                                if event['my_visits'] > 0:
                                                    filtered_events.append(event)
                                            elif includeVisited == False and includeSoldOutEvent == True:
                                                if event['tickets_remaining'] == 0:
                                                    filtered_events.append(event)
                                            else:
                                                if event['my_visits'] > 0 and event['tickets_remaining'] == 0:
                                                    filtered_events.append(event)
                                elif startDate == None and endDate != None:
                                    if event['end_date'] <= endDate:
                                        if event['total_visits'] >= minVisitsRange and event['total_visits'] <= maxVisitsRange:
                                            if includeVisited == False and includeSoldOutEvent == False:
                                                filtered_events.append(event)
                                            elif includeVisited == True and includeSoldOutEvent == False:
                                                if event['my_visits'] > 0:
                                                    filtered_events.append(event)
                                            elif includeVisited == False and includeSoldOutEvent == True:
                                                if event['tickets_remaining'] == 0:
                                                    filtered_events.append(event)
                                            else:
                                                if event['my_visits'] > 0 and event['tickets_remaining'] == 0:
                                                    filtered_events.append(event)
                                else:
                                    if event['end_date'] <= endDate and event['start_date'] >= startDate:
                                        if event['total_visits'] >= minVisitsRange and event['total_visits'] <= maxVisitsRange:
                                            if includeVisited == False and includeSoldOutEvent == False:
                                                filtered_events.append(event)
                                            elif includeVisited == True and includeSoldOutEvent == False:
                                                if event['my_visits'] > 0:
                                                    filtered_events.append(event)
                                            elif includeVisited == False and includeSoldOutEvent == True:
                                                if event['tickets_remaining'] == 0:
                                                    filtered_events.append(event)
                                            else:
                                                if event['my_visits'] > 0 and event['tickets_remaining'] == 0:
                                                    filtered_events.append(event)
                else:
                    if descriptionKeyword.lower() in event['description'].lower():
                        if siteName == "all":
                            if startDate == None and endDate == None:
                                if event['total_visits'] >= minVisitsRange and event['total_visits'] <= maxVisitsRange:
                                    if includeVisited == False and includeSoldOutEvent == False:
                                        filtered_events = all_events
                                    elif includeVisited == True and includeSoldOutEvent == False:
                                        if event['my_visits'] > 0:
                                            filtered_events.append(event)
                                    elif includeVisited == False and includeSoldOutEvent == True:
                                        if event['tickets_remaining'] == 0:
                                            filtered_events.append(event)
                                    else:
                                        if event['my_visits'] > 0 and event['tickets_remaining'] == 0:
                                            filtered_events.append(event)
                            elif startDate != None and endDate == None:
                                if event['start_date'] >= startDate:
                                    if event['total_visits'] >= minVisitsRange and event['total_visits'] <= maxVisitsRange:
                                        if includeVisited == False and includeSoldOutEvent == False:
                                            filtered_events.append(event)
                                        elif includeVisited == True and includeSoldOutEvent == False:
                                            if event['my_visits'] > 0:
                                                filtered_events.append(event)
                                        elif includeVisited == False and includeSoldOutEvent == True:
                                            if event['tickets_remaining'] == 0:
                                                filtered_events.append(event)
                                        else:
                                            if event['my_visits'] > 0 and event['tickets_remaining'] == 0:
                                                filtered_events.append(event)
                            elif startDate == None and endDate != None:
                                if event['end_date'] <= endDate:
                                    if event['total_visits'] >= minVisitsRange and event['total_visits'] <= maxVisitsRange:
                                        if includeVisited == False and includeSoldOutEvent == False:
                                            filtered_events.append(event)
                                        elif includeVisited == True and includeSoldOutEvent == False:
                                            if event['my_visits'] > 0:
                                                filtered_events.append(event)
                                        elif includeVisited == False and includeSoldOutEvent == True:
                                            if event['tickets_remaining'] == 0:
                                                filtered_events.append(event)
                                        else:
                                            if event['my_visits'] > 0 and event['tickets_remaining'] == 0:
                                                filtered_events.append(event)
                            else:
                                if event['end_date'] <= endDate and event['start_date'] >= startDate:
                                    if event['total_visits'] >= minVisitsRange and event['total_visits'] <= maxVisitsRange:
                                        if includeVisited == False and includeSoldOutEvent == False:
                                            filtered_events.append(event)
                                        elif includeVisited == True and includeSoldOutEvent == False:
                                            if event['my_visits'] > 0:
                                                filtered_events.append(event)
                                        elif includeVisited == False and includeSoldOutEvent == True:
                                            if event['tickets_remaining'] == 0:
                                                filtered_events.append(event)
                                        else:
                                            if event['my_visits'] > 0 and event['tickets_remaining'] == 0:
                                                filtered_events.append(event)
                        else:
                            if siteName.lower() in event['site_name'].lower():
                                if startDate == None and endDate == None:
                                    if event['total_visits'] >= minVisitsRange and event['total_visits'] <= maxVisitsRange:
                                        if includeVisited == False and includeSoldOutEvent == False:
                                            filtered_events.append(event)
                                        elif includeVisited == True and includeSoldOutEvent == False:
                                            if event['my_visits'] > 0:
                                                filtered_events.append(event)
                                        elif includeVisited == False and includeSoldOutEvent == True:
                                            if event['tickets_remaining'] == 0:
                                                filtered_events.append(event)
                                        else:
                                            if event['my_visits'] > 0 and event['tickets_remaining'] == 0:
                                                filtered_events.append(event)
                                    elif startDate != None and endDate == None:
                                        if event['start_date'] >= startDate:
                                            if event['total_visits'] >= minVisitsRange and event['total_visits'] <= maxVisitsRange:
                                                if includeVisited == False and includeSoldOutEvent == False:
                                                    filtered_events.append(event)
                                                elif includeVisited == True and includeSoldOutEvent == False:
                                                    if event['my_visits'] > 0:
                                                        filtered_events.append(event)
                                                elif includeVisited == False and includeSoldOutEvent == True:
                                                    if event['tickets_remaining'] == 0:
                                                        filtered_events.append(event)
                                                else:
                                                    if event['my_visits'] > 0 and event['tickets_remaining'] == 0:
                                                        filtered_events.append(event)
                                    elif startDate == None and endDate != None:
                                        if event['end_date'] <= endDate:
                                            if event['total_visits'] >= minVisitsRange and event['total_visits'] <= maxVisitsRange:
                                                if includeVisited == False and includeSoldOutEvent == False:
                                                    filtered_events.append(event)
                                                elif includeVisited == True and includeSoldOutEvent == False:
                                                    if event['my_visits'] > 0:
                                                        filtered_events.append(event)
                                                elif includeVisited == False and includeSoldOutEvent == True:
                                                    if event['tickets_remaining'] == 0:
                                                        filtered_events.append(event)
                                                else:
                                                    if event['my_visits'] > 0 and event['tickets_remaining'] == 0:
                                                        filtered_events.append(event)
                                    else:
                                        if event['end_date'] <= endDate and event['start_date'] >= startDate:
                                            if event['total_visits'] >= minVisitsRange and event['total_visits'] <= maxVisitsRange:
                                                if includeVisited == False and includeSoldOutEvent == False:
                                                    filtered_events.append(event)
                                                elif includeVisited == True and includeSoldOutEvent == False:
                                                    if event['my_visits'] > 0:
                                                        filtered_events.append(event)
                                                elif includeVisited == False and includeSoldOutEvent == True:
                                                    if event['tickets_remaining'] == 0:
                                                        filtered_events.append(event)
                                                else:
                                                    if event['my_visits'] > 0 and event['tickets_remaining'] == 0:
                                                        filtered_events.append(event)                

    return render_template("explore_event.html", sites=all_sites, events=filtered_events, title="Explore Event", legend="Explore Event", form=form, userType=request.args.get('userType'), username=request.args.get('username'))

## SCREEN 34 
@app.route('/visitor_event_detail', methods=["GET","POST"])
def visitor_event_detail(): 
    form = VisitorEventDetail()
    event_name = request.args['event_name']
    start_date = request.args['start_date']
    site_name = request.args['site_name']
    username = request.args['username']
    tickets_remaining = request.args['tickets_remaining']

    # Create cursor
    cur = mysql.connection.cursor()

    # Retrieve event information
    cur.execute("SELECT * FROM event WHERE event_name=%s and start_date=%s and site_name=%s", (event_name, start_date, site_name))
    event = cur.fetchone()

    # Commit to DB
    mysql.connection.commit()

    # Close connection
    cur.close()

    if form.logVisit.data:
        visitDate = form.visitDate.data
        if visitDate < event['start_date'] or visitDate > event['end_date']:
            flash('Please select a date in which the event is held', 'danger')
            return render_template("visitor_event_detail.html", title="Event Detail", legend="Event Detail", form=form, event=event, tickets_remaining=tickets_remaining, userType=request.args.get('userType'), username=request.args.get('username'))

        if tickets_remaining == '0':
            flash('This event has sold out', 'danger')
            return render_template("visitor_event_detail.html", title="Event Detail", legend="Event Detail", form=form, event=event, tickets_remaining=tickets_remaining, userType=request.args.get('userType'), username=request.args.get('username'))

        # Create cursor
        cur = mysql.connection.cursor()

        # Check for duplicate entry
        cur.execute("SELECT COUNT(*) FROM visit_event WHERE visitor_username=%s and event_name=%s and start_date=%s and site_name=%s and visit_event_date=%s", (username, event_name, event['start_date'], site_name, visitDate))
        possible_duplicate = cur.fetchone()['COUNT(*)']
        if possible_duplicate > 0:
            flash('Cannot log visit to the same event on the same date', 'danger')
            return render_template("visitor_event_detail.html", title="Event Detail", legend="Event Detail", form=form, event=event, tickets_remaining=tickets_remaining, userType=request.args.get('userType'), username=request.args.get('username'))

        # Insert information into visit_event table
        cur.execute("INSERT INTO visit_event(visitor_username, event_name, start_date, site_name, visit_event_date) VALUES(%s, %s, %s, %s, %s)", (username, event_name, event['start_date'], site_name, visitDate))

        # Commit to DB
        mysql.connection.commit()

        # Close connection
        cur.close()
        flash('Successfully Logged Visit to Event', 'success')
        return redirect(url_for('explore_event', userType=request.args.get('userType'), username=request.args.get('username')))
    return render_template("visitor_event_detail.html", title="Event Detail", legend="Event Detail", form=form, event=event, tickets_remaining=tickets_remaining, userType=request.args.get('userType'), username=request.args.get('username'))

## SCREEN 35 
@app.route('/explore_site', methods=["GET", "POST"])
def explore_site(): 
    form = ExploreSite()

    username = request.args['username']

    all_sites = get_all_sites()
    all_sites = site_derived(all_sites)

    cur = mysql.connection.cursor()

    for site in all_sites: 
        cur.execute("SELECT open_everyday FROM site WHERE site_name = %s", (site['site_name'],))
        open_everyday = cur.fetchone()
        if open_everyday['open_everyday'] == 1: 
            open_everyday = 'yes'
        else: 
            open_everyday = 'no'
        site['open_everyday'] = open_everyday
        cur.execute("SELECT count(*) as num FROM visit_site WHERE site_name = %s", (site['site_name'],))
        total_visits = cur.fetchone()
        site['total_visits'] = total_visits['num']
        cur.execute("SELECT count(*) as num FROM visit_site WHERE site_name = %s and visitor_username = %s", (site['site_name'], username,))
        my_visits = cur.fetchone()
        site['my_visits'] = my_visits['num']
        cur.execute("SELECT visit_start_date FROM visit_site WHERE site_name = %s", (site['site_name'],))
        td = cur.fetchall()
        total_dates = [] 
        for date in td: 
            total_dates.append(date['visit_start_date'])
        site['total_dates'] = total_dates
        cur.execute("SELECT visit_start_date FROM visit_site WHERE site_name = %s and visitor_username = %s", (site['site_name'], username,))
        md = cur.fetchall()
        my_dates = [] 
        for date in md: 
            my_dates.append(date['visit_start_date'])
        site['my_dates'] = my_dates

    # Commit to DB
    mysql.connection.commit()
    # Close connection
    cur.close()

    sites = []


    openEveryDay = form.openEveryDay.data
    startDate = form.startDate.data 
    endDate = form.endDate.data 
    minVisitsRange = form.minVisitsRange.data 
    maxVisitsRange = form.maxVisitsRange.data 
    minEventCount = form.minEventCount.data 
    maxEventCount = form.maxEventCount.data 
    includeVisited = form.includeVisited.data

    if form.filter.data: 
        site_name = request.form.get('sitesDrop')
        for site in all_sites: 
            if includeVisited == False:
                if site['my_visits'] == 0: 
                    if site_name == 'all': 
                        if site['open_everyday'] == openEveryDay: 
                            if minEventCount != None and maxEventCount!= None: 
                                if site['event_count'] >= minEventCount and site['event_count'] <= maxEventCount:
                                    sites.append(site)
                            elif minEventCount != None and maxEventCount == None: 
                                if site['event_count'] >= minEventCount: 
                                    sites.append(site)
                            elif minEventCount == None and maxEventCount != None: 
                                if site['event_count'] <= maxEventCount: 
                                    sites.append(site)
                            else: 
                                sites.append(site)
                        elif openEveryDay == 'all': 
                            if minEventCount != None and maxEventCount!= None: 
                                if site['event_count'] >= minEventCount and site['event_count'] <= maxEventCount:
                                    sites.append(site)
                            elif minEventCount != None and maxEventCount == None: 
                                if site['event_count'] >= minEventCount: 
                                    sites.append(site)
                            elif minEventCount == None and maxEventCount != None: 
                                if site['event_count'] <= maxEventCount: 
                                    sites.append(site)
                            else: 
                                sites.append(site)
                    else: 
                        if site['site_name'] == site_name: 
                            if site['open_everyday'] == openEveryDay: 
                                if minEventCount != None and maxEventCount!= None: 
                                    if site['event_count'] >= minEventCount and site['event_count'] <= maxEventCount:
                                        sites.append(site)
                                elif minEventCount != None and maxEventCount == None: 
                                    if site['event_count'] >= minEventCount: 
                                        sites.append(site)
                                elif minEventCount == None and maxEventCount != None: 
                                    if site['event_count'] <= maxEventCount: 
                                        sites.append(site)
                                else: 
                                    sites.append(site)
                            elif openEveryDay == 'all': 
                                if minEventCount != None and maxEventCount!= None: 
                                    if site['event_count'] >= minEventCount and site['event_count'] <= maxEventCount:
                                        sites.append(site)
                                elif minEventCount != None and maxEventCount == None: 
                                    if site['event_count'] >= minEventCount: 
                                        sites.append(site)
                                elif minEventCount == None and maxEventCount != None: 
                                    if site['event_count'] <= maxEventCount: 
                                        sites.append(site)
                                else: 
                                    sites.append(site)
            else: 
                if site_name == 'all': 
                    if site['open_everyday'] == openEveryDay: 
                        if minEventCount != None and maxEventCount!= None: 
                            if site['event_count'] >= minEventCount and site['event_count'] <= maxEventCount:
                                sites.append(site)
                        elif minEventCount != None and maxEventCount == None: 
                            if site['event_count'] >= minEventCount: 
                                sites.append(site)
                        elif minEventCount == None and maxEventCount != None: 
                            if site['event_count'] <= maxEventCount: 
                                sites.append(site)
                        else: 
                            sites.append(site)
                    elif openEveryDay == 'all': 
                        if minEventCount != None and maxEventCount!= None: 
                            if site['event_count'] >= minEventCount and site['event_count'] <= maxEventCount:
                                sites.append(site)
                        elif minEventCount != None and maxEventCount == None: 
                            if site['event_count'] >= minEventCount: 
                                sites.append(site)
                        elif minEventCount == None and maxEventCount != None: 
                            if site['event_count'] <= maxEventCount: 
                                sites.append(site)
                        else: 
                            sites.append(site)
                else: 
                    if site['site_name'] == site_name: 
                        if site['open_everyday'] == openEveryDay: 
                            if minEventCount != None and maxEventCount!= None: 
                                if site['event_count'] >= minEventCount and site['event_count'] <= maxEventCount:
                                    sites.append(site)
                            elif minEventCount != None and maxEventCount == None: 
                                if site['event_count'] >= minEventCount: 
                                    sites.append(site)
                            elif minEventCount == None and maxEventCount != None: 
                                if site['event_count'] <= maxEventCount: 
                                    sites.append(site)
                            else: 
                                sites.append(site)
                        elif openEveryDay == 'all': 
                            if minEventCount != None and maxEventCount!= None: 
                                if site['event_count'] >= minEventCount and site['event_count'] <= maxEventCount:
                                    sites.append(site)
                            elif minEventCount != None and maxEventCount == None: 
                                if site['event_count'] >= minEventCount: 
                                    sites.append(site)
                            elif minEventCount == None and maxEventCount != None: 
                                if site['event_count'] <= maxEventCount: 
                                    sites.append(site)
                            else: 
                                sites.append(site)
                

    form.openEveryDay.data = openEveryDay
    form.startDate.data = startDate
    form.endDate.data = endDate
    form.minVisitsRange.data = minVisitsRange
    form.maxVisitsRange.data = maxVisitsRange 
    form.minEventCount.data = minEventCount 
    form.maxEventCount.data = maxEventCount
    form.includeVisited.data = includeVisited

    if form.siteDetail.data:
        if 'site_name' not in request.form:
            flash('Please select an site to view details', 'danger')
        else:
            site_name = request.form['site_name']
            return redirect(url_for('site_detail', site_name=site_name, userType=request.args.get('userType'), username=request.args.get('username')))
    elif form.transitDetail.data:
        if 'site_name' not in request.form:
            flash('Please select a site to view transit details', 'danger')
        else:
            site_name = request.form['site_name']
            return redirect(url_for('transit_detail', site_name=site_name, userType=request.args.get('userType'), username=request.args.get('username')))
    return render_template("explore_site.html", all_sites = all_sites, sites=sites, title="Explore Site", legend="Explore Site", form = form, userType=request.args.get('userType'), username=request.args.get('username'))

# Helper method to retrieve transits for site
def transits_for_site(site_name):
    # Create cursor
    cur = mysql.connection.cursor()

    # Retrieve transits for this site
    cur.execute("SELECT transit_type, transit_route FROM connect WHERE site_name=%s", (site_name,))
    transits = cur.fetchall()

    # Find the price of the transit
    for transit in transits:
        cur.execute("SELECT transit_price FROM transit WHERE transit_type=%s and transit_route=%s", (transit['transit_type'], transit['transit_route']))
        transit['transit_price'] = cur.fetchone()['transit_price']

        # Find # connected sites for transit
        cur.execute("SELECT COUNT(*) FROM connect WHERE transit_type=%s and transit_route=%s", (transit['transit_type'], transit['transit_route']))
        transit['connected_sites'] = cur.fetchone()['COUNT(*)']

    # Commit to DB
    mysql.connection.commit()

    # Close connection
    cur.close()
    return transits

## SCREEN 36 
@app.route('/transit_detail', methods=["GET","POST"])
def transit_detail(): 
    form = TransitDetail()
    username = request.args['username']
    site_name = request.args['site_name']
    all_transits = transits_for_site(site_name)
    filtered_transits = []

    if form.filter.data:
        transportType = form.transportType.data
        if transportType == 'all':
            filtered_transits = all_transits
        else:
            for transit in all_transits:
                if transit['transit_type'] == transportType:
                    filtered_transits.append(transit)
    elif form.logTransit.data:
        if 'transit' not in request.form:
            flash('Please select a transit to log a date for', 'danger')
            return render_template("transit_detail.html", site_name=site_name, transits=filtered_transits, title="Transit Detail", legend="Transit Detail", form=form, userType=request.args.get('userType'), username=request.args.get('username'))
        else:
            transit = request.form['transit']
        transit = transit.split()
        transit_route = transit[0]
        transit_type = transit[1]
        transitDate = form.transitDate.data
        if transitDate == None:
            flash('Please select a valid date to log transit', 'danger')
            return render_template("transit_detail.html", site_name=site_name, transits=filtered_transits, title="Transit Detail", legend="Transit Detail", form=form, userType=request.args.get('userType'), username=request.args.get('username'))

        # Create cursor
        cur = mysql.connection.cursor()
    
        # Check first if the attempted entry is a duplicate
        # NOTE: user can only take the same transit once per day
        cur.execute("SELECT * FROM take_transit")
        results = cur.fetchall()
        
        for result in results:
            if result['username'] == username and result['transit_type'] == transit_type and result['transit_route'] == transit_route and result['transit_date'] == transitDate:
                flash('Cannot take the same transit more than once per day', 'danger')
                return render_template("transit_detail.html", site_name=site_name, transits=filtered_transits, title="Transit Detail", legend="Transit Detail", form=form, userType=request.args.get('userType'), username=request.args.get('username'))

        # insert information into take_transit table
        cur.execute("INSERT INTO take_transit(username, transit_type, transit_route, transit_date) VALUES(%s, %s, %s, %s)", (username, transit_type, transit_route, transitDate))
        
        # Commit to DB
        mysql.connection.commit()

        # Close connection
        cur.close()
        flash('Successfully logged transit', 'success')
        return redirect(url_for('explore_site', userType=request.args.get('userType'), username=request.args.get('username')))
    return render_template("transit_detail.html", site_name=site_name, transits=filtered_transits, title="Transit Detail", legend="Transit Detail", form=form, userType=request.args.get('userType'), username=request.args.get('username'))

## SCREEN 37 
@app.route('/site_detail', methods=["GET","POST"])
def site_detail(): 
    username = request.args['username']
    form = SiteDetail()
    site_name = request.args['site_name']
    # Create cursor
    cur = mysql.connection.cursor()

    # Query information for the site
    cur.execute("SELECT open_everyday, address, zipcode FROM site WHERE site_name=%s", (site_name,))
    site_information = cur.fetchone()

    if site_information['open_everyday'] == 0:
        site_information['open_everyday'] = 'No'
    else:
        site_information['open_everyday'] = 'Yes'

    # Commit to DB
    mysql.connection.commit()

    # Close connection
    cur.close()

    if form.logVisit.data:
        visitDate = form.visitDate.data

        # Create cursor
        cur = mysql.connection.cursor()

        # Check for duplicate entry
        cur.execute("SELECT COUNT(*) FROM visit_site WHERE visitor_username=%s and site_name=%s and visit_start_date=%s", (username, site_name, visitDate))
        possible_duplicate = cur.fetchone()['COUNT(*)']
        if possible_duplicate > 0:
            flash('Cannot log visit to the same site on the same date', 'danger')
            return redirect(url_for('site_detail', site_name=site_name, userType=request.args.get('userType'), username=request.args.get('username')))

        # Insert information into visit_event table
        cur.execute("INSERT INTO visit_site(visitor_username, site_name, visit_start_date) VALUES(%s, %s, %s)", (username, site_name, visitDate))

        # Commit to DB
        mysql.connection.commit()

        # Close connection
        cur.close()
        flash('Successfully Logged Visit to Site', 'success')
        return redirect(url_for('explore_site', userType=request.args.get('userType'), username=request.args.get('username')))
    return render_template("site_detail.html", site_name=site_name, site_information=site_information, title="Site Detail", legend="Site Detail", form=form, userType=request.args.get('userType'), username=request.args.get('username'))

# Helper method to retrieve the visit sites and visit events for user
def get_visits(username):
    # Create cursor
    cur = mysql.connection.cursor()

    # Retrieve visit events
    cur.execute("SELECT event_name, start_date, site_name, visit_event_date FROM visit_event WHERE visitor_username=%s", (username,))
    events = cur.fetchall()

    # Retrieve price or each event
    for event in events:
        cur.execute("SELECT price FROM event WHERE event_name=%s and start_date=%s and site_name=%s", (event['event_name'], event['start_date'], event['site_name']))
        event['price'] = cur.fetchone()['price']

    # Retrieve visit sites
    cur.execute("SELECT site_name, visit_start_date FROM visit_site WHERE visitor_username=%s", (username,))
    sites = cur.fetchall()

    # Commit to DB
    mysql.connection.commit()

    # Close connection
    cur.close()
    visits = {'events': events, 'sites':sites}
    return visits

## SCREEN 38 
@app.route('/visit_history', methods=['GET','POST'])
def visit_history(): 
    username = request.args['username']
    form = VisitHistory()
    all_sites = get_all_sites()
    visits = get_visits(username)
    events = visits['events']
    sites = visits['sites']

    filtered_events = []
    filtered_sites = []
    if form.filter.data:
        event_name = form.event.data
        startDate = form.startDate.data
        endDate = form.endDate.data        
        site = request.form.get('contain_site')

        if endDate != None and startDate != None and endDate < startDate:
            flash('End Date cannot be before Start Date', 'danger')
            return render_template("visit_history.html", sites=all_sites, events=filtered_events, sitesList=filtered_sites, title="Visit History", legend="Visit History", form=form, userType=request.args.get('userType'), username=request.args.get('username'))
        
        if site == 'all':
            if event_name == "":
                if startDate == None and endDate == None:
                    filtered_events = events
                    filtered_sites = sites
                elif startDate != None and endDate == None:
                    for event in events:
                        if event['visit_event_date'] >= startDate:
                            filtered_events.append(event)
                    for site in sites:
                        if site['visit_start_date'] >= startDate:
                            filtered_sites.append(site)
                elif startDate == None and endDate != None:
                    for event in events:
                        if event['visit_event_date'] <= endDate:
                            filtered_events.append(event)
                    for site in sites:
                        if site['visit_start_date'] <= endDate:
                            filtered_sites.append(site)
                else:
                    for event in events:
                        if event['visit_event_date'] >= startDate and event['visit_event_date'] <= endDate:
                            filtered_events.append(event)
                    for site in sites:
                        if site['visit_start_date'] >= startDate and site['visit_start_date'] <= endDate:
                            filtered_sites.append(site)
            else:
                for event in events:
                    if event['event_name'] == event_name:
                        if startDate == None and endDate == None:
                            filtered_events.append(event)
                        elif startDate != None and endDate == None:
                            if event['visit_event_date'] >= startDate:
                                filtered_events.append(event)
                        elif startDate == None and endDate != None:
                            if event['visit_event_date'] <= endDate:
                                filtered_events.append(event)
                        else:
                            if event['visit_event_date'] >= startDate and event['visit_event_date'] <= endDate:
                                filtered_events.append(event)
        else:
            for each_site in sites:
                if each_site['site_name'] == site:
                    if startDate == None and endDate == None:
                        filtered_sites.append(each_site)
                    elif startDate != None and endDate == None:
                        if each_site['visit_start_date'] >= startDate:
                            filtered_sites.append(each_site)
                    elif startDate == None and endDate != None:
                        if each_site['visit_start_date'] <= endDate:
                            filtered_sites.append(site)
                    else:
                        if each_site['visit_start_date'] >= startDate and each_site['visit_start_date'] <= endDate:
                            filtered_sites.append(site)     
                    filtered_sites.append(each_site)
            if event_name == "":
                for event in events:
                    if startDate == None and endDate == None:
                        filtered_events.append(event)
                    elif startDate != None and endDate == None:
                        if event['visit_event_date'] >= startDate:
                            filtered_events.append(event)
                    elif startDate == None and endDate != None:
                        if event['visit_event_date'] <= endDate:
                            filtered_events.append(event)
                    else:
                        if event['visit_event_date'] >= startDate and event['visit_event_date'] <= endDate:
                            filtered_events.append(event)                          
            else:
                for event in events:
                    if event['event_name'] == event_name:
                        if startDate == None and endDate == None:
                            filtered_events.append(event)
                        elif startDate != None and endDate == None:
                            if event['visit_event_date'] >= startDate:
                                filtered_events.append(event)
                        elif startDate == None and endDate != None:
                            if event['visit_event_date'] <= endDate:
                                filtered_events.append(event)
                        else:
                            if event['visit_event_date'] >= startDate and event['visit_event_date'] <= endDate:
                                filtered_events.append(event)

    return render_template("visit_history.html", sites=all_sites, events=filtered_events, sitesList=filtered_sites, title="Visit History", legend="Visit History", form=form, userType=request.args.get('userType'), username=request.args.get('username'))

if __name__ == '__main__':
    app.run(debug=True)