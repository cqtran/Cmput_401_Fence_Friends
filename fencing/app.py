from flask import Flask, render_template, request, redirect, url_for, session, \
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

from api.forms.extendedRegisterForm import *

import json
from api.jsonifyObjects import MyJSONEncoder
from flask.json import jsonify

import argparse

app = Flask(__name__) #, template_folder = "HTML", static_folder = "CSS")
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
        # gets customers and display
        customers = dbSession.query(Customer).filter(Customer.company_name == current_user.company_name).all()
        s = []
        id = []
        for i in customers:
            s.append(i.first_name)
            id.append(i.customer_id)

        return render_template("customer.html", company = current_user.company_name, listcust = json.dumps(s), custid = json.dumps(id)) #change to companyname

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

    # Get the argument 'cust_id' if it is given
    customer_id = request.args.get('cust_id')

    # Start a query on Project
    projects= dbSession.query(Project)

    # If the current user is an admin, then allow them to look at all projects
    if current_user.has_role('admin'):
        pass
    # Otherwise, find projects in the same company as the logged in user
    else:
        projects = projects.filter(Customer.company_name == current_user.company_name)

    # If an customer id is given, then filter projects on the customer
    if customer_id is not None:
        projects = projects.filter(customer_id == Project.customer_id)
        print('\ncustomer_id: ' + customer_id)

    # Filter projects with matching customer_ids and execute query
    projects = projects.filter(Customer.customer_id == Project.customer_id).all()

    # Serialize results
    json_list=[i.serialize for i in projects]

    if customer_id is None:
        return render_template("projects.html", listproj = json.dumps(json_list), company = current_user.company_name)

    else:
        customer = dbSession.query(Customer).filter(Customer.customer_id == customer_id).first()
        return render_template("projects.html", listproj = json.dumps(json_list),
                 name = customer.first_name, company = customer.company_name,
                 phone = customer.cellphone, email = customer.email, cid = customer_id)

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

@app.route('/viewMaterialList/', methods = ['POST'])
@login_required
@roles_required('primary')
def viewMaterialList():
    """Generate and view a material list in a new tab"""
    proj_id = request.args.get('proj_id')
    project = dbSession.query(Project).filter(
        Project.project_id == proj_id).one()
    customer = dbSession.query(Customer).filter(
        Customer.customer_id == project.customer_id).one()
    return Messages.materialListMessage(project)

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
    attachmentString = Messages.quoteAttachment(project, customer)
    attachment = Email.makeAttachment(Messages.quotePath, attachmentString)

    if attachment is not None:
        return redirect(url_for("static", filename=attachment[7:]))

    return redirect(url_for("projectinfo", proj_id=proj_id))

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
    attachmentString = Messages.quoteAttachment(project, customer)
    attachment = Email.makeAttachment(Messages.quotePath, attachmentString)

    if attachment is not None:
        Email.send(app, mail, project.company_name, customer.email,
            "Your quote", message, "Quote", attachment)

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
            # get project info to pass to html and display
            json_projectinfo = Projects.getProject(project_id)
            print(json_projectinfo)

            # Get project pictures to display
            json_pictures = Pictures.getPictures(project_id)
            json_quotepic = Projects.getdrawiopic(project_id)
            print(json_pictures)
            print(json_quotepic)

            # Get relative path to project pictures
            imgPath = repr(os.path.join('..', Pictures.directory, ''))
            print('Relative Path: ' + imgPath)

            return render_template("projectinfo.html", proj = json.dumps(json_projectinfo),
                company = current_user.company_name, images = json.dumps(json_pictures),
                path = imgPath, drawiopic = json.dumps(json_quotepic))
    else:
        # POST?
        print("post")
        long_url = request.form['myField']
        print(long_url)

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
            # Grab project information to set into the editing form
            json_projectinfo = Projects.getProject(project_id)
            print(json_projectinfo)

            # Grab the list of statuses to set into the dropdown list
            # TODO: Refactor this into an API
            statuses = dbSession.query(Status).all()
            json_statuses = [i.serialize for i in statuses]
            print(json_statuses)

            return render_template("editproject.html", proj = json.dumps(json_projectinfo),
                statuses = json.dumps(json_statuses), company = current_user.company_name)
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
