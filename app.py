from flask import Flask, render_template, request, redirect, url_for, session
from flask_security import Security, login_required, \
     SQLAlchemySessionUserDatastore
from Python.db import dbSession, init_db, fieldExists
from Python.models import User, Role, Company, Customer, Project, Status
from flask_mail import Mail
from flask_security.core import current_user
from flask_security.signals import user_registered
from flask_security.decorators import roles_required

import os
# Import python files with functionality
import Python.accounts as Accounts
import Python.customers as Customers
import Python.projects as Projects

from Python.extendedRegisterForm import *

import json
from Python.jsonifyObjects import MyJSONEncoder
from flask.json import jsonify



app = Flask(__name__) #, template_folder = "HTML", static_folder = "CSS")
app.json_encoder = MyJSONEncoder
app.secret_key = os.urandom(24) # used for sessions


app.config['DEBUG'] = True
app.config['TESTING'] = True
app.config['SECRET_KEY'] = 'super-secret'
app.config['SECURITY_PASSWORD_SALT'] = 'testing'

app.config['SECURITY_REGISTERABLE'] = True
app.config['SECURITY_RECOVERABLE'] = True
# change to true after implemented
app.config['SECURITY_CONFIRMABLE'] = False
app.config['SECURITY_CHANGEABLE'] = True

app.config['SECURITY_MSG_INVALID_PASSWORD'] = ("Invalid username or password", "error")
app.config['SECURITY_MSG_USER_DOES_NOT_EXIST'] = ("Invalid username or password", "error")

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'cmput401fence@gmail.com'
app.config['MAIL_PASSWORD'] = 'fencing401'
app.config['SECURITY_EMAIL_SENDER'] = 'cmput401fence@gmail.com'

mail = Mail(app)

# Setup Flask-Security
userDatastore = SQLAlchemySessionUserDatastore(dbSession,
                                                User, Role)

dbSession.commit()

security = Security(app, userDatastore, confirm_register_form=ExtendedConfirmRegisterForm)


test = 0
# TODO: implement fresh login for password change

# Create a user to test with only run once
@app.before_first_request
def setup_db():
    init_db()
    userDatastore.find_or_create_role(name = 'admin')
    userDatastore.find_or_create_role(name = 'primary')
    userDatastore.find_or_create_role(name = 'secondary')

    if not fieldExists(dbSession, Company.company_name, "Fence"):
        newCompany = Company(company_name = "Fence", email = "e@e.c")
        dbSession.add(newCompany)

    dbSession.commit()


    # Test data
    if not fieldExists(dbSession, User.id, 1):
        newUser = User(id = 1, email = 'test@test.null', username = 'test', 
            password = 'password', company_name = 'Fence', active = 1)
        dbSession.add(newUser)
        userDatastore.add_role_to_user(newUser, 'primary')
        userDatastore.activate_user(newUser)
        dbSession.commit()

    if not fieldExists(dbSession, Customer.customer_id, 1):
        newCustomer = Customer(customer_id = 1, email = "null@null.null", first_name = "Andy",
                last_name = "John", cellphone = "1234567", company_name = "Fence")

    if not fieldExists(dbSession, Status.status_name, "Not Reached"):
        newStatus = Status(status_name = "Not Reached")
        dbSession.add(newStatus)
        dbSession.commit()

    if not fieldExists(dbSession, Project.project_id, 1):
        newProject = Project(project_id = 1, customer_id = 1, address = "1234",
                             start_date =  "2017-08-19")
        dbSession.add(newProject)
        dbSession.commit()




    # if not fieldExists(dbSession, roles_users.id, 1):
    #     newRoleUser = Roles_users(id = 1, user_id = 1, role_id = 2)
    #     dbSession.add(newRoleUser)
    #     dbSession.commit()


@app.teardown_appcontext
def shutdown_session(exception=None):
    dbSession.remove()

#deactivates new users
@user_registered.connect_via(app)
def user_registered_sighandler(app, user, confirm_token):
    #userDatastore.deactivate_user(user)
    userDatastore.add_role_to_user(user, 'primary')
    dbSession.commit()

#@app.route('/customers', methods=['GET', 'POST'])
@app.route('/')
@login_required
def customers():
    #user = dbSession.query(User).filter(User.id == current_user.id).one()

        #print("This is company id")
        #print(getcmpyid)

        #return render_template("customer.html", listcust = list_customers)

    #x = userDatastore.deactivate_user(current_user)
    #dbSession.commit()
    if current_user.has_role('admin'):
        users = dbSession.query(User).filter(User.active == True) # need to add filter role
        return render_template("users.html", company = "Admin", users = users)
    else:
        customers = dbSession.query(Customer).filter(Customer.company_name == current_user.company_name).all()
        s = []
        id = []
        for i in customers:
            s.append(i.first_name)
            id.append(i.customer_id)

        return render_template("customer.html", company = current_user.company_name, listcust = json.dumps(s), custid = json.dumps(id)) #change to companyname

@app.route('/users')
@login_required
@roles_required('admin')
def users():
    users = dbSession.query(User).filter(User.active == True).all()
    return render_template("users.html", company = "Admin", users = users)

@app.route('/accountrequests')
@login_required
@roles_required('admin')
def accountrequests():
    users = dbSession.query(User).filter(User.active == False).all()
    return render_template("accountrequests.html", company = "Admin", users = users)

@app.route('/newcustomer', methods=['GET', 'POST'])
@login_required
@roles_required('primary')
def newcustomer():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        pn = request.form['pn']
        address = request.form['address']

        success = Customers.addCustomer(name,email,pn,address,current_user.company_name)
        print(success)

        return redirect(url_for('customers'))


    else:
        return render_template("newcustomer.html")

@app.route('/editcustomer', methods=['GET', 'POST'])
@login_required
@roles_required('primary')
def editcustomer():
    return render_template("editcustomer.html")

@app.route('/projects')
@login_required
@roles_required('primary')
def projects():
    # Get the argument 'cust_id' if it is given
    customer_id = request.args.get('cust_id')
    
    # Start a query on Project
    projects= dbSession.query(Project)
    
    # If the current user is an admin, then allow them to look at all projects
    if current_user.has_role('admin'):
        pass
    # Otherwise, find projects in the same company as the logged in user
    else:
        projects = projects.filter(Customer.company_name == current_user.company_name)
    
    # If an customer id is given, then filter projects on the customer
    if customer_id is not None:
        projects = projects.filter(customer_id == Project.customer_id)
        print('\ncustomer_id: ' + customer_id)

    # Filter projects with matching customer_ids and execute query
    projects = projects.filter(Customer.customer_id == Project.customer_id).all()
    
    # Serialize results
    json_list=[i.serialize for i in projects]
    print('Projects found: ')
    print(json_list)
    print('\n')
    
    return render_template("projects.html", listproj = json.dumps(json_list))

@app.route('/newproject')
@login_required
@roles_required('primary')
def newproject():
    if request.method == 'POST':
        status = request.form['status']
        email = request.form['email']
        pn = request.form['pn']
        address = request.form['address']

        success = Customers.addCustomer(name,email,pn,address,current_user.company_name)
    return render_template("newproject.html")


# delete later, just for testing note
@app.route('/projectinfo')
@login_required
@roles_required('primary')
def projectinfo():
    project_id = request.args.get('proj_id')
    
    if customer_id is not None:
        project = dbSession.query(Project)
        project = project.filter(Project.project_id == project_id).one()
        return render_template("projectinfo.html", proj = json.dumps(project.serialize))
    return render_template("projectinfo.html")

if __name__ == "__main__":
    app.run(debug=True)