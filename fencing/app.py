from flask import Flask, Blueprint, render_template, request, redirect, url_for, session, \
    flash
from flask_security import Security, login_required, \
     SQLAlchemySessionUserDatastore
from database.db import dbSession, init_db, fieldExists
from database.models import User, Role, Company, Customer, Project, Status
from diagram.DiagramParser import DiagramParser
from flask_mail import Mail
from api.email.Email import SENDER_EMAIL, Email
from api.email.Messages import Messages
from flask_security.core import current_user
from flask_security.signals import user_registered
from flask_security.decorators import roles_required

import os
# Import python files with functionality
import api.customers as Customers
import api.projects as Projects
import api.pictures as Pictures
import api.statuses as Statuses

from api.forms.extendedRegisterForm import *

import json
from api.jsonifyObjects import MyJSONEncoder
from flask.json import jsonify

import argparse

app = Flask(__name__) #, template_folder = "HTML", static_folder = "CSS")
app.register_blueprint(Customers.customerBlueprint)
app.register_blueprint(Projects.projectBlueprint)
app.register_blueprint(Pictures.pictureBlueprint)
app.register_blueprint(Statuses.statusBlueprint)

app.json_encoder = MyJSONEncoder
app.secret_key = os.urandom(24) # used for sessions

app.config['DEBUG'] = True
app.config['TESTING'] = False
app.config['SECRET_KEY'] = 'super-secret'
app.config['SECURITY_PASSWORD_SALT'] = 'testing'

app.config['SECURITY_REGISTERABLE'] = True
app.config['SECURITY_RECOVERABLE'] = True
# change to true after implemented
app.config['SECURITY_CONFIRMABLE'] = False
app.config['SECURITY_CHANGEABLE'] = True

app.config['SECURITY_MSG_INVALID_PASSWORD'] = ("Invalid username or password", "error")
app.config['SECURITY_MSG_USER_DOES_NOT_EXIST'] = ("Invalid username or password", "error")

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = SENDER_EMAIL
app.config['MAIL_PASSWORD'] = 'fencing401'
app.config['SECURITY_EMAIL_SENDER'] = SENDER_EMAIL
app.config['MAIL_SUPPRESS_SEND'] = False

mail = Mail(app)

# Setup Flask-Security
userDatastore = SQLAlchemySessionUserDatastore(dbSession,
                                                User, Role)

dbSession.commit()

security = Security(app, userDatastore, confirm_register_form=ExtendedConfirmRegisterForm, register_form=ExtendedRegisterForm)


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
        newCompany = Company(company_name = "Fence", email = "e@e.c")
        dbSession.add(newCompany)

    dbSession.commit()


    # Test data
    if not fieldExists(dbSession, User.id, 1):
        newUser = User(id = 1, email = 'test@test.null', username = 'test',
            password = 'password', company_name = 'Fence', active = 1)
        dbSession.add(newUser)
        userDatastore.add_role_to_user(newUser, 'primary')
        userDatastore.activate_user(newUser)
        dbSession.commit()

    if not fieldExists(dbSession, Customer.customer_id, 1):
        newCustomer = Customer(customer_id = 1, email = "null@null.null", first_name = "Andy"
                                ,cellphone = "1234567", company_name = "Fence")
        dbSession.add(newCustomer)
        dbSession.commit()


    if not fieldExists(dbSession, Status.status_name, "Not Reached"):
        newStatus = Status(status_name = "Not Reached")
        dbSession.add(newStatus)
        dbSession.commit()

    if not fieldExists(dbSession, Status.status_name, "Finished"):
        newStatus = Status(status_name = "Finished")
        dbSession.add(newStatus)
        dbSession.commit()

    if not fieldExists(dbSession, Project.project_id, 1):
        newProject = Project(customer_id = 1, address = "1234",
            status_name = "Not Reached", end_date = None, note = '',
            project_name = "Andy's Project", company_name = "Fence")
        dbSession.add(newProject)
        dbSession.commit()


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
def customers():
    if current_user.has_role('admin'):
        users = dbSession.query(User).filter(User.active == True) # need to add filter role
        return render_template("users.html", company = "Admin", users = users)
    else:
        return render_template("customer.html")

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
    users = dbSession.query(User).filter(User.active == False).all()
    return render_template("accountrequests.html", company = "Admin", users = users)

@app.route('/newcustomer/', methods=['GET', 'POST'])
@login_required
@roles_required('primary')
def newcustomer():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        pn = request.form['pn']
        address = request.form['address']
        # add customer to database
        success = Customers.addCustomer(name,email,pn,address,current_user.company_name)
        print(success)

        return redirect(url_for('customers'))#, company = current_user.company_name))

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
        return render_template("projects.html")

@app.route('/autocomplete/', methods=["GET"])
@login_required
@roles_required('primary')
def autocomplete():
    # pulls in customers to populate dropdown table in new project
    search = request.args.get("q")
    print(search)
    customers = dbSession.query(Customer).filter(Customer.company_name == current_user.company_name).all()
    return jsonify(customers)


@app.route('/newproject/', methods=['GET', 'POST'])
@login_required
@roles_required('primary')
def newproject():
    print("new project" + request.method)
    if request.method == 'POST':
        #customer = request.form["customer"]
        #print()
        #customer = request.args.get('customer')
        customer = request.form["customer"]
        customer = customer.split("-")
        print(customer)
        customerId = customer[1]
        print(customer)
        projectname = request.form["name"]
        print(projectname)
        address = request.form["address"]
        print(address)
        # cid = request.form[]
        #print(customer)
        success = Projects.createProject(customerId, "Not Reached",  address,
                                         current_user.company_name, projectname)
        return redirect(url_for('projects'))
    else:
        return render_template("newproject.html")

@app.route('/sendQuote/', methods = ['POST'])
@login_required
@roles_required('primary')
def sendQuote():
    """Email a quote to a customer"""
    proj_id = request.args.get('proj_id')
    project = dbSession.query(Project).filter(
        Project.project_id == proj_id).one()
    customer = dbSession.query(Customer).filter(
        Customer.customer_id == project.customer_id).one()
    company = dbSession.query(Company).filter(
        Company.company_name == project.company_name).one()
    message = Messages.quoteMessage(customer, company)
    attachment = Messages.quoteAttachment(project, customer)
    Email.send(app, mail, project.company_name, customer.email, "Your quote",
        message, "Quote", attachment, True)
    return redirect(url_for("projectinfo", proj_id=proj_id))

@app.route('/sendMaterialList/', methods = ['POST'])
@login_required
@roles_required('primary')
def sendMaterialList():
    """Email a material list to a supplier"""
    proj_id = request.args.get('proj_id')
    project = dbSession.query(Project).filter(
        Project.project_id == proj_id).one()
    customer = dbSession.query(Customer).filter(
        Customer.customer_id == project.customer_id).one()
    message = Messages.materialListMessage(project)
    Email.send(app, mail, project.company_name, customer.email, "Material list",
        message, "Material list")
    return redirect(url_for("projectinfo", proj_id=proj_id))

# delete later, just for testing note
@app.route('/projectinfo/', methods = ['GET', 'POST', 'PUT'])
@login_required
@roles_required('primary')
def projectinfo():
    if request.method == "GET":
        project_id = request.args.get('proj_id')
        if project_id is not None:
            # Get relative path to project pictures
            imgPath = repr(os.path.join('..', Pictures.directory, ''))
            print('Relative Path: ' + imgPath)

            return render_template("projectinfo.html", path = imgPath)

    else:
        return render_template("projectinfo.html", company = current_user.company_name)

@app.route('/uploadpicture/', methods = ['GET', 'POST'])
@login_required
@roles_required('primary')
def uploadpicture():
    if request.method == 'POST':
        project_id = request.form['proj_id']
        picture = request.files['picture']

        print('\nProject ID: ' + project_id)
        print('File name: ' + picture.filename)
        # Store the picture in the database
        Pictures.addPicture(app.root_path, project_id, picture)

        return redirect(url_for('projectinfo', proj_id = project_id))

@app.route('/editprojectinfo/', methods = ['GET', 'POST'])
@login_required
@roles_required('primary')
def editprojectinfo():
    if request.method == "GET":
        project_id = request.args.get('proj_id')
        if project_id is not None:
            return render_template("editproject.html")
        else:
            # Error handling
            pass

    if request.method == "POST":
        project_id = request.form['project_id']
        project_name = request.form['project_name']
        address = request.form['address']
        status = request.form['status']
        note = request.form['note']

        Projects.updateProjectInfo(project_id = project_id, project_name = project_name,
            address = address, status = status, note = note)

        return redirect(url_for('projectinfo', proj_id = project_id))

@app.route('/testdraw/',  methods = ['GET', 'POST'])
def testdraw():
    return render_template("self-editing-embed.html")



if __name__ == "__main__":

    parser = argparse.ArgumentParser(description = 'Run Cavalry Fence Builder')
    parser.add_argument('-debug', action = 'store_true')
    parser.add_argument('-public', action = 'store_true')
    args = parser.parse_args()

    if args.public:
        app.run(host = '0.0.0.0', debug = False)

    else:
        app.run(debug = args.debug)
