from flask import Flask, Blueprint, render_template, request, redirect, \
    url_for, session
from flask_security import Security, login_required, \
     SQLAlchemySessionUserDatastore
from database.db import dbSession, init_db, fieldExists
from database.models import User, Role, Company, Customer, Project, Status, Picture, Layout, Appearance
from flask_mail import Mail
from api.email.Email import SENDER_EMAIL, Email
from api.email.Messages import Messages
from diagram.DiagramParser import DiagramParser
from flask_security.core import current_user
from flask_security.signals import user_registered
from flask_security.decorators import roles_required
from api.decorators import async

from priceCalculation.QuoteCalculation import QuoteCalculation
import priceCalculation.priceCalculation as PriceCalculation

import os, traceback
# Import python files with functionality
import api.users as Users
import api.customers as Customers
import api.projects as Projects
import api.pictures as Pictures
import api.statuses as Statuses
import api.layouts as Layouts
import api.appearances as Appearances
import api.quotes as Quotes
import api.materials as Materials
import api.estimates as Estimates
import api.accounting as Accounting
#import api.errors as Errors
from api.forms.extendedRegisterForm import *

import json
from api.jsonifyObjects import MyJSONEncoder
from flask.json import jsonify

import argparse

""" 
    app.py is used for running the fence friends + cavalry fence application
    to run the website locally 
    run: 'app.py' in the terminal with 'python3 app.py'
    database will initialize on entering the website
    If at anytime there is an error go into mysql and use the following commands
    
    drop database testData;
    create database testData;
    use testData;
    run python3 app.py
    enter website
"""



app = Flask(__name__) #, template_folder = "HTML", static_folder = "CSS")
app.register_blueprint(Customers.customerBlueprint)
app.register_blueprint(Projects.projectBlueprint)
app.register_blueprint(Pictures.pictureBlueprint)
app.register_blueprint(Statuses.statusBlueprint)
app.register_blueprint(Users.userBlueprint)
app.register_blueprint(Layouts.layoutBlueprint)
app.register_blueprint(Appearances.appearanceBlueprint)
app.register_blueprint(Quotes.quoteBlueprint)
#app.register_blueprint(Errors.errorBlueprint)
app.register_blueprint(Materials.materialBlueprint)
app.register_blueprint(Estimates.estimateBlueprint)
app.register_blueprint(Accounting.accountingBlueprint)
app.json_encoder = MyJSONEncoder
#app.secret_key = os.urandom(24) # used for sessions

app.config['DEBUG'] = True
app.config['TESTING'] = False
app.config['SECRET_KEY'] = 'super-secret'
app.config['SECURITY_PASSWORD_SALT'] = 'testing'

app.config['SECURITY_REGISTERABLE'] = True
app.config['SECURITY_RECOVERABLE'] = True
# change to true after implemented
app.config['SECURITY_CONFIRMABLE'] = False
app.config['SECURITY_CHANGEABLE'] = True
app.config['SECURITY_FLASH_MESSAGES'] = False

app.config['SECURITY_MSG_INVALID_PASSWORD'] = ("Invalid username or password", "error")
app.config['SECURITY_MSG_USER_DOES_NOT_EXIST'] = ("Invalid username or password", "error")

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = SENDER_EMAIL
app.config['MAIL_PASSWORD'] = 'cFb401Id'
app.config['SECURITY_EMAIL_SENDER'] = SENDER_EMAIL
app.config['MAIL_SUPPRESS_SEND'] = False

mail = Mail(app)

# Setup Flask-Security
userDatastore = SQLAlchemySessionUserDatastore(dbSession,
                                                User, Role)

dbSession.commit()

security = Security(app, userDatastore, confirm_register_form=ExtendedConfirmRegisterForm, register_form=ExtendedRegisterForm)

@async
def send_security_email(msg):
    with app.app_context():
       mail.send(msg)

@security.send_mail_task
def async_security_email(msg):
    send_security_email(msg)

test = 0
# TODO: implement fresh login for password change

@app.before_first_request
def setup_db():
    """Create a user to test with only run once"""
    init_db()
    userDatastore.find_or_create_role(name = 'admin')
    userDatastore.find_or_create_role(name = 'primary')
    userDatastore.find_or_create_role(name = 'secondary')

    if not fieldExists(dbSession, Company.company_name, "Fence"):
        newCompany = Company(company_name = "Fence", email = "test@test.null")
        dbSession.add(newCompany)

    dbSession.commit()
    if not fieldExists(dbSession, Company.company_name, "Admin"):
        newCompany = Company(company_name = "Admin", email = "admin@cavalryfence.ca")
        dbSession.add(newCompany)

    dbSession.commit()


    # Test data
    if not fieldExists(dbSession, User.id, 1):
        #primary
        newUser = User(id = 1, email = 'test@test.null', username = 'test',
            password = 'password', company_name = 'Fence', active = 1)
        dbSession.add(newUser)
        userDatastore.add_role_to_user(newUser, 'primary')
        userDatastore.activate_user(newUser)
        dbSession.commit()

    if not fieldExists(dbSession, User.id, 2):
        #primary
        newUser = User(id = 2, email = 'admin@cavalryfence.ca', username = 'Admin',
            password = 'password', company_name = 'Admin', active = 1)
        dbSession.add(newUser)
        userDatastore.add_role_to_user(newUser, 'admin')
        userDatastore.activate_user(newUser)
        dbSession.commit()

    if not fieldExists(dbSession, Status.status_name, "Not Reached"):
        newStatus = Status(status_name = "Not Reached", status_number = 1)
        dbSession.add(newStatus)
        dbSession.commit()

    if not fieldExists(dbSession, Status.status_name, "Paid"):
        newStatus = Status(status_name = "Paid", status_number = 2)
        dbSession.add(newStatus)
        dbSession.commit()

    if not fieldExists(dbSession, Status.status_name, "Appraisal Booked"):
        newStatus = Status(status_name = "Appraisal Booked", status_number = 3)
        dbSession.add(newStatus)
        dbSession.commit()

    if not fieldExists(dbSession, Status.status_name, "Waiting for Appraisal"):
        newStatus = Status(status_name = "Waiting for Appraisal", status_number = 4)
        dbSession.add(newStatus)
        dbSession.commit()

    if not fieldExists(dbSession, Status.status_name, "Appraised"):
        newStatus = Status(status_name = "Appraised", status_number = 5)
        dbSession.add(newStatus)
        dbSession.commit()

    if not fieldExists(dbSession, Status.status_name, "Quote Sent"):
        newStatus = Status(status_name = "Quote Sent", status_number = 6)
        dbSession.add(newStatus)
        dbSession.commit()

    if not fieldExists(dbSession, Status.status_name, "Waiting for Alberta1Call"):
        newStatus = Status(status_name = "Waiting for Alberta1Call", status_number = 7)
        dbSession.add(newStatus)
        dbSession.commit()

    if not fieldExists(dbSession, Status.status_name, "Installation Pending"):
        newStatus = Status(status_name = "Installation Pending", status_number = 8)
        dbSession.add(newStatus)
        dbSession.commit()

    if not fieldExists(dbSession, Status.status_name, "Installing"):
        newStatus = Status(status_name = "Installing", status_number = 9)
        dbSession.add(newStatus)
        dbSession.commit()

    if not fieldExists(dbSession, Status.status_name, "No Longer Interested"):
        newStatus = Status(status_name = "No Longer Interested", status_number = 10)
        dbSession.add(newStatus)
        dbSession.commit()
    Pictures.app_root = app.root_path
    Email.staticFolder = app.root_path + "/static/"

@app.teardown_appcontext
def shutdown_session(exception=None):
    dbSession.remove()

@user_registered.connect_via(app)
def user_registered_sighandler(app, user, confirm_token):
    """Deactivates new users"""
    changeUser = dbSession.query(User).filter(User.id == user.id).one()
    newCompany = Company(company_name = user.username, email = user.email)
    dbSession.add(newCompany)
    dbSession.commit()
    changeUser.company_name = user.username

    userDatastore.deactivate_user(user)
    userDatastore.add_role_to_user(user, 'primary')
    dbSession.commit()

@app.route('/')
@login_required
def home():
    if current_user.has_role('admin'):
        users = dbSession.query(User).filter(User.active == True) # need to add filter role
        return render_template("users.html", company = "Admin", users = users)
    else:
        return render_template("dashboard.html", company = current_user.company_name)

@app.route('/customers/')
@login_required
@roles_required('primary')
def customers():
    return render_template("customer.html", company = current_user.company_name)

@app.route('/users/')
@login_required
@roles_required('admin')
def users():
    users = dbSession.query(User).filter(User.active == True).all()
    return render_template("users.html", company = "Admin", users = users)

@app.route('/accountrequests/')
@login_required
@roles_required('admin')
def accountrequests():
    return render_template("accountrequests.html", company = "Admin")

@app.route('/acceptUser/', methods=['POST'])
@login_required
@roles_required('admin')
def acceptUser():
    """ accepts user, in app.py because of userDatastore """
    if request.method == 'POST':
        user_id = request.values.get("user_id")
        user = dbSession.query(User).filter(User.id == user_id).all()
        userDatastore.activate_user(user[0])
        user[0].active = True
        dbSession.commit()
        users = dbSession.query(User).filter(User.active == False).all()
        return jsonify(users)

@app.route('/deactivateUser/', methods=['POST'])
@login_required
@roles_required('admin')
def deactivateUser():
    """ accepts user, in app.py because of userDatastore """
    if request.method == 'POST':
        user_id = request.values.get("user_id")
        user = dbSession.query(User).filter(User.id == user_id).all()
        userDatastore.deactivate_user(user[0])
        user[0].active = False
        dbSession.commit()
        users = dbSession.query(User).filter(User.active == True).filter(User.id != current_user.id).all()
        return jsonify(users)

@app.route('/newcustomer/', methods=['GET', 'POST'])
@login_required
@roles_required('primary')
def newcustomer():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        pn = request.form['pn']
        address = ""
        # add customer to database
        success = Customers.addCustomer(name,email,pn,address,current_user.company_name)

        return redirect(url_for('customers', company = current_user.company_name))

    else:
        return render_template("newcustomer.html", company = current_user.company_name)

@app.route('/editcustomer/', methods=['GET', 'POST'])
@login_required
@roles_required('primary')
def editcustomer():
    return render_template("editcustomer.html")

@app.route('/projects/')
@login_required
@roles_required('primary')
def projects():
    status = request.args.get('status')

    # Because seeing "None" in the dropdown menu is unsettling, even if it is
    # treated as "All"
    if (status is None or status == "None"):
        cust_id = request.args.get('cust_id')
        return redirect(url_for('projects', cust_id=cust_id, status="All"))

    return render_template("projects.html", company = current_user.company_name)

@app.route('/customerinfo/')
@login_required
@roles_required('primary')
def customerinfo():
    status = request.args.get('status')
    return render_template("customerinfo.html", company = current_user.company_name)

@app.route('/newproject/')
@login_required
@roles_required('primary')
def newproject():
    return render_template("newproject.html", company = current_user.company_name)

@app.route('/viewMaterialList/', methods = ['POST'])
@login_required
@roles_required('primary')
def viewMaterialList():
    """Generate and view a material list in a new tab"""
    proj_id = request.args.get('proj_id')
    project = dbSession.query(Project).filter(
        Project.project_id == proj_id).one()
    layout = dbSession.query(Layout).filter(
        Layout.layout_id == project.layout_selected).one()
    parsed = DiagramParser.parse(layout.layout_info)
    attachmentString = Messages.materialListAttachment(project)
    attachment = Email.makeAttachment(Messages.materialListPath,
        attachmentString)

    if attachment is not None:
        url = url_for("static", filename=attachment)
        return jsonify({"url": url})

    return jsonify({"reload": 1})

@app.route('/createquote/', methods = ['GET'])
@login_required
@roles_required('primary')
def createquote():
    return render_template("createquote.html",
        company = current_user.company_name)

@app.route('/viewQuote/', methods = ['POST'])
@login_required
@roles_required('primary')
def viewQuote():
    """Generate and view a quote in a new tab"""
    proj_id = request.args.get('proj_id')
    project = dbSession.query(Project).filter(
        Project.project_id == proj_id).one()
    customer = dbSession.query(Customer).filter(
        Customer.customer_id == project.customer_id).one()
    company = dbSession.query(Company).filter(
        Company.company_name == project.company_name).one()
    layout = dbSession.query(Layout).filter(
        Layout.layout_id == project.layout_selected).one()
    parsed = DiagramParser.parse(layout.layout_info)
    attachmentString = Messages.quoteAttachment(project, customer, parsed)
    attachment = Email.makeAttachment(Messages.quotePath, attachmentString)

    if attachment is not None:
        url = url_for("static", filename=attachment)
        return jsonify({"url": url})

    return jsonify({"reload": 1})

@app.route('/sendQuote/', methods = ['POST'])
@login_required
@roles_required('primary')
def sendQuote():
    """Email a quote to a customer"""
    proj_id = request.args.get('proj_id')
    custEmail = request.json['email']
    print(custEmail)
    project = dbSession.query(Project).filter(
        Project.project_id == proj_id).one()
    customer = dbSession.query(Customer).filter(
        Customer.customer_id == project.customer_id).one()
    company = dbSession.query(Company).filter(
        Company.company_name == project.company_name).one()
    message = Messages.quoteMessage(customer, company)
    layout = dbSession.query(Layout).filter(
        Layout.layout_id == project.layout_selected).one()
    parsed = DiagramParser.parse(layout.layout_info)
    attachmentString = Messages.quoteAttachment(project, customer, parsed)
    attachment = Email.makeAttachment(Messages.quotePath, attachmentString)

    if attachment is not None:
        Email.send(app, mail, project.company_name, custEmail,
            "Your quote", message, "Quote", attachment)

    return "{}"

@app.route('/sendMaterialList/', methods = ['POST'])
@login_required
@roles_required('primary')
def sendMaterialList():
    """Email a material list to a supplier"""
    proj_id = request.args.get('proj_id')
    project = dbSession.query(Project).filter(
        Project.project_id == proj_id).one()
    company = dbSession.query(Company).filter(
        Company.company_name == project.company_name).one()
    message = Messages.materialListMessage(company)
    layout = dbSession.query(Layout).filter(
        Layout.layout_id == project.layout_selected).one()
    parsed = DiagramParser.parse(layout.layout_info)
    attachmentString = Messages.materialListAttachment(project)
    attachment = Email.makeAttachment(Messages.materialListPath,
        attachmentString)

    supplierEmail = request.json["email"]

    if attachment is not None:
        Email.send(app, mail, project.company_name, supplierEmail,
            "Material list", message, "Material list", attachment)

    return "{}"

# delete later, just for testing note ---- i think we need this
@app.route('/projectinfo/', methods = ['GET', 'POST', 'PUT'])
@login_required
@roles_required('primary')
def projectinfo():
    if request.method == "GET":
        return render_template("projectinfo.html")
    else:
        # POST?
        return render_template("projectinfo.html")

@app.route('/editprojectinfo/', methods = ['GET'])
@login_required
@roles_required('primary')
def editprojectinfo():
    if request.method == "GET":
        project_id = request.args.get('proj_id')
        return render_template("editproject.html", company = current_user.company_name)

@app.route('/viewPrices/', methods = ['GET'])
@login_required
@roles_required('primary')
def viewPrices():
    return render_template("prices.html", company = current_user.company_name)

@app.route('/viewEstimates/', methods = ['GET'])
@login_required
@roles_required('primary')
def viewEstimates():
    return render_template("estimates.html", company = current_user.company_name)

@app.route('/deleteAttachments/', methods = ['POST'])
@login_required
@roles_required('primary')
def deleteAttachments():
    attachments = request.json["attachments"]
    
    for attachment in attachments:
        deleteAttachment(attachment)
    
    return "{}"

def deleteAttachment(path):
    if ".." in path or path.startswith("/") or path.startswith("\\") or \
        path.count("/") > 1 or path.count("\\") > 1:

        raise Exception("Invalid path passed to deleteAttachment")

    if not (path.startswith("quotes/") or path.startswith("materials/")):
        raise Exception("Invalid path passed to deleteAttachment")

    try:
        os.remove(Email.staticFolder + "attachments/" + path)

    except:
        traceback.print_exc()
        print("Error: could not delete attachment " + path)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', company=current_user.company_name), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

@app.route('/accounting/', methods = ['GET'])
@login_required
@roles_required('primary')
def accounting():
    info = Accounting.getQuoteInfo()
    return render_template("accounting.html", company = current_user.company_name)

@app.route('/editsupplier/', methods = ['GET'])
@login_required
@roles_required('primary')
def editsupplier():
    company = dbSession.query(Company).filter(
        Company.company_name == current_user.company_name).one()
    email = company.supplier_email

    if email is None:
        email = ""

    return render_template("editsupplier.html",
        company = company.company_name, email = email)

@app.route('/updatesupplier/', methods = ['POST'])
@login_required
@roles_required('primary')
def updatesupplier():
    company = dbSession.query(Company).filter(
        Company.company_name == current_user.company_name).one()
    company.supplier_email = request.json["email"]
    dbSession.commit()
    return "{}"

@app.route('/editquote/', methods = ['GET'])
@login_required
@roles_required('primary')
def editquote():
    proj_id = request.args.get("proj_id")
    project = dbSession.query(Project).filter(
        Project.project_id == proj_id).one()
    layout = dbSession.query(Layout).filter(
        Layout.layout_id == project.layout_selected).one()
    appearance = dbSession.query(Appearance).filter(
        Appearance.appearance_id == project.appearance_selected).one()
    parsed = DiagramParser.parse(layout.layout_info)
    appearanceValues = Quotes.getAppearanceValues(appearance)
    prices = QuoteCalculation.prices(parsed, appearanceValues[0],
        appearanceValues[1], appearanceValues[2], appearanceValues[3])
    subtotal = PriceCalculation.subtotal(prices)
    gstPercent = PriceCalculation.gstPercent
    gst = subtotal * gstPercent
    total = subtotal + gst
    return render_template("editquote.html", company = current_user.company_name, proj_id = proj_id)



if __name__ == "__main__":

    parser = argparse.ArgumentParser(description = 'Run Cavalry Fence Builder')
    parser.add_argument('-debug', action = 'store_true')
    parser.add_argument('-public', action = 'store_true')
    args = parser.parse_args()

    if args.public:
        app.run(host = '0.0.0.0', debug = False)

    else:
        app.run(debug = args.debug)
