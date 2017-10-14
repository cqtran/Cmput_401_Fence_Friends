from flask import Flask, render_template, request
from flask_security import Security, login_required, \
     SQLAlchemySessionUserDatastore
from Python.db import dbSession, init_db
from Python.models import User, Role

# Import python files with functionality
import Python.accounts as Accounts
import Python.customers as Customers
import Python.projects as Projects

app = Flask(__name__) #, template_folder = "HTML", static_folder = "CSS")
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'super-secret'
app.config['SECURITY_PASSWORD_SALT'] = 'testing'
Bootstrap(app)


# Setup Flask-Security
userDatastore = SQLAlchemySessionUserDatastore(dbSession,
                                                User, Role)
security = Security(app, userDatastore)


test = 0

#@app.route("/")
#def main():
#    return render_template("login.html")

@app.route('/showSignUp')
def showSignUp():
    return render_template("signup.html")


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

@app.route('/login', methods=['GET', 'POST'])
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

#@app.route('/customers', methods=['GET', 'POST'])
@app.route('/')
@login_required
def customers():
    print("nigga we made it")
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
    return render_template("customer.html")

@app.route('/newcustomer', methods=['GET', 'POST'])
def newcustomer():
    return render_template("newcustomer.html")

@app.route('/editcustomer', methods=['GET', 'POST'])
def editcustomer():
    return render_template("editcustomer.html")

@app.route('/projects')
def projects():
    return render_template("projects.html")

@app.route('/newproject')
def newproject():
    return render_template("newproject.html")

if __name__ == "__main__":
    app.run(debug=True)