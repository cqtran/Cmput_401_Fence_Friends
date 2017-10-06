from flask import Flask, render_template, request

# Import python files with other functionality such as accessing the database
#import Python.db as DB

app = Flask(__name__, template_folder = "HTML", static_folder = "CSS")

@app.route("/")
def main():
    return render_template("login.html")

@app.route('/showSignUp')
def showSignUp():
    return render_template("signup.html")

@app.route('/login', methods=['POST'])
def login():
    # Get form information
    username = request.form['username']
    password = request.form['password']
    print("Username: " + username)
    print("Password: " + password)
    
    # Access MySQL and authorize
    
    #connection = DB.getConnection()
    #cursor = connection.cursor()
    
    #statement = "SELECT * FROM accounts WHERE Username = '" + username + "' AND Password = '" + password + "'"
    #numrows = cursor.query(statement)
    
    #cursor.close()
    #connection.close()
    
    return render_template("home.html")

    #if numrows == 1:
    #    return render_template("home.html")
    #else:
    #    return render_template("login.html")

if __name__ == "__main__":
    app.run()