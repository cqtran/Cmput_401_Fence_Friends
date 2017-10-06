from flask import Flask, render_template

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
    # Access MySQL and authorize
    
    return render_template("home.html")

if __name__ == "__main__":
    app.run()