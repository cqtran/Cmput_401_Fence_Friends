from flask import Flask, render_template, request

# Import python files with functionality
import Python.accounts as Accounts

app = Flask(__name__) #, template_folder = "HTML", static_folder = "CSS")

@app.route("/")
def main():
    return render_template("login.html")

@app.route('/showSignUp')
def showSignUp():
    return render_template("signup.html")


@app.route('/signup', methods=['POST'])
def signup():
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

@app.route('/login', methods=['GET', 'POST'])
#@app.route('/login', methods=['POST'])
def login():
    # Get form information
    username = request.form.get('username', "")
    password = request.form.get('password', "")
    print("Username: " + username)
    print("Password: " + password)

    # Authenticate the username/password
    success = Accounts.authenticate(username, password)
    
    if success:
        return render_template("customer.html")
    else:
        return render_template("login.html", error = "Invalid username or password")

@app.route('/customers', methods=['GET', 'POST'])
def customers():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        pn = request.form['pn']
        address = request.form['address']
        print(type(name))

        return render_template("customer.html", name = name, email = email, pn=pn, address = address)
    else:
        return render_template("customer.html")

@app.route('/newcustomer', methods=['GET', 'POST'])
def newcustomer():
    return render_template("newcustomer.html")

@app.route('/projects')
def projects():
    return render_template("projects.html")

if __name__ == "__main__":
    app.run(debug=True)