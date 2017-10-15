from flask import Flask, render_template, request
from flask_security import Security, login_required, \
     SQLAlchemySessionUserDatastore
from Python.db import dbSession, init_db
from Python.models import User, Role
from flask_mail import Mail
from flask_security.core import current_user
from flask_security.signals import user_registered
from flask_security.decorators import roles_required

# Import python files with functionality
import Python.accounts as Accounts
import Python.customers as Customers
import Python.projects as Projects
from Python.extendedRegisterForm import *

app = Flask(__name__) #, template_folder = "HTML", static_folder = "CSS")

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
    '''if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        pn = request.form['pn']
        address = request.form['address']
        print(type(name))
        success = Customers.addCustomer(name, email, pn, address)
        test = 1
        list_customers = Customers.displayCustomers(test)
        print("This is test value")
        print(test)
        return render_template("customer.html", name = name, email = email, pn=pn,
                               address = address, listcust = list_customers)
    else:
        return render_template("customer.html")'''
    #x = userDatastore.deactivate_user(current_user)
    #dbSession.commit()
    if current_user.has_role('admin'):
        users = dbSession.query(User).filter(User.active == True).filter(User.role == 'primary')
        return render_template("users.html", company = "Admin", users = users)
    else:
        return render_template("customer.html", company = current_user.username) #change to companyname

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
@roles_required('primary', 'secondary')
def newcustomer():
    return render_template("newcustomer.html")

@app.route('/editcustomer', methods=['GET', 'POST'])
@login_required
@roles_required('primary', 'secondary')
def editcustomer():
    return render_template("editcustomer.html")

@app.route('/projects')
@login_required
@roles_required('primary', 'secondary')
def projects():
    return render_template("projects.html")

@app.route('/newproject')
@login_required
@roles_required('primary', 'secondary')
def newproject():
    return render_template("newproject.html")

if __name__ == "__main__":
    app.run(debug=True)