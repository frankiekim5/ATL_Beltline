from flask import Flask, render_template, url_for, flash, redirect, session, request, jsonify
from flask_mysqldb import MySQL
from forms import UserRegistrationForm, LoginForm, VisitorRegistrationForm, EmployeeRegistrationForm, EmployeeVisitorRegistrationForm, TransitForm, EmailRegistrationForm, TransitForm, SiteForm, EventForm, ManageSiteForm, ManageTransitForm, ManageUser, ManageEvent, EditEvent, UserTakeTransit, TransitHistory, EmployeeProfileForm
from passlib.hash import sha256_crypt
from random import randint

app = Flask(__name__)

# Config MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Frankie1999!'
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

@app.route('/employee_profile', methods=['GET', 'POST'])
def employee_profile():
    form = EmployeeProfileForm()
    return render_template('employee_profile.html', form=form, emails=request.args.get('emails'), userType=request.args.get('userType'), username=request.args.get('username'))

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
        result = cur.execute("SELECT * FROM user_email WHERE email = %s", [email])
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
    
## SCREEN 15 
@app.route('/take_transit', methods=['GET', 'POST'])
def take_transit(): 
    form = UserTakeTransit()
    return render_template('take_transit.html', title="Take Transit",legend="Take Transit",form=form)

## SCREEN 16 
@app.route('/transit_history', methods=['GET', 'POST'])
def transit_history(): 
    form = TransitHistory()
    return render_template('transit_history.html', title="Transit History",legend="Transit History",form=form)
 
## SCREEN 17 
@app.route('/manage_profile', methods=['GET','POST'])
def manage_profile(): 
    form = EmployeeProfileForm()
    ## email QUERY
    emails = ["timmywu@email.com", "timmylovesfrankie@gmail.com","timmy.wu@bobalover.com"]
    return render_template("employee_profile.html", title="Manage Profile", legend="Manage Profile", form=form, emails = emails)

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
            

## SCREEN 22 
@app.route('/manage_transit')
def manage_transit():
    form = ManageTransitForm()
    return render_template('manage_transit.html', legend="Manage Transit", form=form, title='Manage Transit', emails=request.args.get('emails'), userType=request.args.get('userType'), username=request.args.get('username'))

## SCREEN 24
@app.route('/create_transit', methods=['GET','POST'])
def create_transit():
    form = TransitForm()
    if form.validate_on_submit() and request.method == 'POST': 
        transportType = form.transportType.data 
        route = form.route.data 
        price = form.price.data
        connectedSites = form.connectedSites.data

         # Create cursor
        cur = mysql.connection.cursor()

        # Execute query
        cur.execute("INSERT INTO transit(transit_type, transit_route, transit_price) VALUES(%s, %s, %s)", (transportType, route, price))

        # Commit to DB
        mysql.connection.commit()

        # Close connection
        cur.close()
        return redirect(url_for('transit_nav', emails=request.args.get('emails'), userType=request.args.get('userType'), username=request.args.get('username')))
    return render_template("create_transit.html", title='Create Transit', form=form, legend='Create Transit', emails=request.args.get('emails'), userType=request.args.get('userType'), username=request.args.get('username'))

## SCREEN 23
@app.route('/edit_transit', methods=['GET', 'POST'])
def edit_transit(): 
    form = TransitForm()
    ## MUST WRITE QUERIES HERE 
    if form.validate_on_submit(): 
        transportType = form.transportType.data 
        route = form.route.data 
        price = form.price.data
        connectedSites = form.connectedSites.data
    return render_template("create_transit.html", title='Edit Transit', form=form, legend='Edit Transit', emails=request.args.get('emails'), userType=request.args.get('userType'), username=request.args.get('username')) 

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
    return render_template('manage_event.html', title="Manage Event", legend="Manage Event", form=form)

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

## SCREEN 27 
@app.route('/create_event', methods=['GET', 'POST'])
def create_event(): 
    form = EventForm()  
    if form.validate_on_submit(): 
        minStaff = form.minStaff.data 
        description = form.description.data
        assignStaff = form.assignStaff.data
    return render_template("create_event.html", title="Create Event", form=form)

if __name__ == '__main__':
    app.run(debug=True)