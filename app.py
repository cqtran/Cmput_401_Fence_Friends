from flask import Flask, render_template, request, session, redirect, url_for
import os
# Import python files with functionality
import Python.accounts as Accounts
import Python.customers as Customers
import Python.projects as Projects

app = Flask(__name__) #, template_folder = "HTML", static_folder = "CSS")
app.secret_key = os.urandom(24) # used for sessions


@app.route("/")
def main():
    return render_template("login.html")

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
            session['companyid'] = cmpy_ID


            return redirect(url_for('customers'))#render_template("customer.html", company = cmpy_ID), redirect(url_for('customers'))
        else:
            return render_template("login.html", error = "Invalid username or password")
    else:
        return render_template("login.html")

@app.route('/customers', methods=['GET', 'POST'])
def customers():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        pn = request.form['pn']
        address = request.form['address']
        getcmpyid = session.get('companyid', None)

        success = Customers.addCustomer(name, email, pn, address, getcmpyid)

        list_customers = Customers.displayCustomers(getcmpyid)
        #print("This is company id")
        #print(getcmpyid)

        return render_template("customer.html", name = name, email = email, pn=pn,
                               address = address, listcust = list_customers)
    else:
        #print("This is company id")
        getcmpyid = session.get('companyid', None)
        #print(getcmpyid)
        list_customers = Customers.displayCustomers(getcmpyid)

        return render_template("customer.html", listcust = list_customers)

@app.route('/newcustomer', methods=['GET', 'POST'])
def newcustomer():
    return render_template("newcustomer.html")

@app.route('/editcustomer', methods=['GET', 'POST'])
def editcustomer():
    return render_template("editcustomer.html")

@app.route('/projects', methods=['GET', 'POST'])
def projects():

    if request.method == 'POST':
        customerId = request.form['customer']
        customer = Customers.getCustomer(customerId)
        print(customer)

    return render_template("projects.html")

@app.route('/newproject')
def newproject():
    return render_template("newproject.html")


# delete later, just for testing note
@app.route('/projectinfo', methods=['GET', 'POST'])
def projectinfo():
    if request.method == 'POST':
        notes = request.form['note']

        # get project ID and display note
        return render_template("projectinfo.html", note = notes)

    else:
        return render_template("projectinfo.html")



if __name__ == "__main__":
    app.run(debug=True)