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

@app.route('/login', methods=['GET', 'POST'])
def login():
    # Get form information
    username = request.form.get('username', "")
    password = request.form.get('password', "")
    print("Username: " + username)
    print("Password: " + password)

    # Authenticate the username/password
    authorized = Accounts.authenticate(username, password)
    
    if authorized:
        return render_template("home.html")
    else:
        return render_template("login.html")



@app.route('/customers')
def customers():
    return render_template("customer.html")

@app.route('/projects')
def projects():
    return render_template("projects.html")

if __name__ == "__main__":
    app.run(debug=True)