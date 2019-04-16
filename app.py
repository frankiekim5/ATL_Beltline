from flask import Flask, render_template, url_for, flash, redirect, session, request, jsonify
from flask_mysqldb import MySQL
from forms import UserRegistrationForm, LoginForm, VisitorRegistrationForm, EmployeeRegistrationForm, EmployeeVisitorRegistrationForm, TransitForm, EmailRegistrationForm, TransitForm, SiteForm, EventForm, ManageSiteForm
from passlib.hash import sha256_crypt

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
        cur.execute("INSERT INTO employee(username, phone, address, city, state, zipcode) VALUES(%s, %s, %s, %s, %s, %s)", (username, phone, address, city, state, zipcode))
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
        cur.execute("INSERT INTO employee(username, phone, address, city, state, zipcode) VALUES(%s, %s, %s, %s, %s, %s)", (username, phone, address, city, state, zipcode))
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

<<<<<<< HEAD
@app.route('/transit_nav')
def transit_nav():
    return render_template('transit_navigation.html', title='Transit Navigation', emails=request.args.get('emails'), userType=request.args.get('userType'), username=request.args.get('username'))



=======
@app.route('/manage_transit')
def manage_transit():
    return render_template('manage_transit.html', title='Manage Transit', emails=request.args.get('emails'), userType=request.args.get('userType'), username=request.args.get('username'))
>>>>>>> e2b31c2c1fc1a410fecd69e89c1bcc121265a9bd
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

@app.route('/manage_site', methods=['GET', 'POST'])
def manage_site():
    form = ManageSiteForm()
    if form.validate_on_submit(): 
        site = form.site.data 
        manager = form.manager.data 
        openEveryDay = form.openEveryDay.data 
        siteList = form.siteList.data 
    return render_template('manage_site.html', form=form, title='Manage Navigation', legend='Manage Site', emails=request.args.get('emails'), userType=request.args.get('userType'), username=request.args.get('username'))

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
        return redirect(url_for('site_nav', emails=request.args.get('emails'), userType=request.args.get('userType'), username=request.args.get('username')))
    return render_template("create_site.html", title='Create Site', form=form, legend='Create Site', unassigned_managers=managers, emails=request.args.get('emails'), userType=request.args.get('userType'), username=request.args.get('username'))

#
@app.route('/edit_site', methods=['GET', 'POST'])
def edit_site(): 
    ## can query from the database to get the specific SiteName as PK
    ## site = query using curr
    form = SiteForm()
    if form.validate_on_submit(): 
        ## here is where the site.name etc. should be in order to update 
        siteName = form.siteName.data
        zipcode = form.zipcode.data
        address = form.address.data 
        manager = form.manager.data 
        openEveryday = form.openEveryday.data
    return render_template("create_site.html", title="Edit Site", form=form, legend="Edit Site",  emails=request.args.get('emails'), userType=request.args.get('userType'), username=request.args.get('username'))

## SCREEN 27 
@app.route('/create_event', methods=['GET', 'POST'])
def create_event(): 
    form = EventForm()  
    if form.validate_on_submit(): 
        name = form.name.data  
        price = form.price.data 
        capacity = form.capacity.data
        minStaff = form.minStaff.data 
        startDate = form.startDate.data
        endDate = form.endDate.data 
        description = form.description.data
        assignStaff = form.assignStaff.data
       

    return render_template("create_event.html", title="Create Event", form=form)

if __name__ == '__main__':
    app.run(debug=True)