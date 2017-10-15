from flask import Flask, render_template, request
from flask_security import Security, login_required, \
     SQLAlchemySessionUserDatastore
from Python.db import dbSession, init_db
from Python.models import User, Role
from flask_mail import Mail
from flask_security.core import current_user

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
userDatastore.create_role(name = 'admin')

security = Security(app, userDatastore, confirm_register_form=ExtendedConfirmRegisterForm)


test = 0
# TODO: implement fresh login for password change

# Create a user to test with only run once
@app.before_first_request
def create_user():
    init_db()
    dbSession.commit()

@app.teardown_appcontext
def shutdown_session(exception=None):
    dbSession.remove()

#@app.route("/")
#def main():
#    return render_template("login.html")
'''
@app.route('/showSignUp')
def showSignUp():
    return render_template("signup.html")
'''
'''
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # Get form information
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirmPassword = request.form['confirmPassword']
        
        print("Username: " + username)
        print("email: " + email)
        print("password: " + password)
        print("confirmPassword: " + confirmPassword)
        
        if(password != confirmPassword):
            return render_template("signup.html", error = "Password and confirmed password do not match")
        
        success = Accounts.requestAccount(username, email, password)
        
        if success:
            return render_template("login.html", note = "Request sucessful")
        else:
            return render_template("signup.html", error = "An error has occurred. Try again later.")
    else:
        return render_template("signup.html")
'''

'''@app.route('/login', methods=['GET', 'POST'])
#@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        # Get form information
        username = request.form['username']
        password = request.form['password']
        print("Username: " + username)
        print("Password: " + password)

        # Authenticate the username/password
        success = Accounts.authenticate(username, password)
        
        if success:
            cmpy_ID = Accounts.getCompany(username)
           # customers(company=cmpy_ID)

            return render_template("customer.html", company = cmpy_ID)
        else:
            return render_template("login.html", error = "Invalid username or password")
    else:
        return render_template("login.html")
'''

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
    return render_template("customer.html", company=current_user.username)

@app.route('/users')
@login_required
def users():
    return render_template("users.html")

@app.route('/accountrequests')
@login_required
def accountrequests():
    return render_template("accountrequests.html")

@app.route('/newcustomer', methods=['GET', 'POST'])
@login_required
def newcustomer():
    return render_template("newcustomer.html")

@app.route('/editcustomer', methods=['GET', 'POST'])
@login_required
def editcustomer():
    return render_template("editcustomer.html")

@app.route('/projects')
@login_required
def projects():
    return render_template("projects.html")

@app.route('/newproject')
@login_required
def newproject():
    return render_template("newproject.html")

if __name__ == "__main__":
    app.run(debug=True)