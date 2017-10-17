from flask import Flask, render_template, request, redirect, url_for, session
from flask_security import Security, login_required, \
     SQLAlchemySessionUserDatastore
from Python.db import dbSession, init_db
from Python.models import User, Role, Company, Customer
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
app.config['SECRET_KEY'] = 'super-secret'
app.config['SECURITY_PASSWORD_SALT'] = 'testing'

app.config['SECURITY_REGISTERABLE'] = True
app.config['SECURITY_RECOVERABLE'] = True
# change to true after implemented
app.config['SECURITY_CONFIRMABLE'] = True
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

    newCompany = Company(company_name = "Fence", email = "e@e.c")
    #dbSession.add(newCompany)
    dbSession.commit()

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
        print(customers[0].first_name)
        print(customers[1].first_name)
        s = []
        for i in customers:
            s.append(i.first_name)

        return render_template("customer.html", company = current_user.company_name, listcust = json.dumps(s)) #change to companyname

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

    if request.method == 'POST':
        customerId = request.form['customer']
        customer = Customers.getCustomer(customerId)
        print(str(customer))

    return render_template("projects.html")

@app.route('/newproject')
@login_required
@roles_required('primary')
def newproject():
    return render_template("newproject.html")


# delete later, just for testing note
@app.route('/projectinfo', methods=['GET', 'POST'])
@login_required
@roles_required('primary')
def projectinfo():
    if request.method == 'POST':
        notes = request.form['note']

        # get project ID and display note
        return render_template("projectinfo.html", note = notes)

    else:
        return render_template("projectinfo.html")



if __name__ == "__main__":
    app.run(debug=True)