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
import api.users as Users
import api.customers as Customers
import api.projects as Projects
import api.pictures as Pictures
import api.statuses as Statuses
import api.admin as Admins
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
app.register_blueprint(Admins.adminBlueprint)
app.register_blueprint(Users.userBlueprint)
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
app.config['SECURITY_FLASH_MESSAGES'] = False

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
    if not fieldExists(dbSession, Company.company_name, "Admin"):
        newCompany = Company(company_name = "Admin", email = "a@a.c")
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
        newUser = User(id = 2, email = 'admin@admin.null', username = 'Admin',
            password = 'password', company_name = 'Admin', active = 1)
        dbSession.add(newUser)
        userDatastore.add_role_to_user(newUser, 'admin')
        userDatastore.activate_user(newUser)
        dbSession.commit()

    if not fieldExists(dbSession, Status.status_name, "Not Reached"):
        newStatus = Status(status_name = "Not Reached")
        dbSession.add(newStatus)
        dbSession.commit()

    if not fieldExists(dbSession, Status.status_name, "Paid"):
        newStatus = Status(status_name = "Paid")
        dbSession.add(newStatus)
        dbSession.commit()

    if not fieldExists(dbSession, Status.status_name, "Appraisal Booked"):
        newStatus = Status(status_name = "Appraisal Booked")
        dbSession.add(newStatus)
        dbSession.commit()

    if not fieldExists(dbSession, Status.status_name, "Appraised"):
        newStatus = Status(status_name = "Appraised")
        dbSession.add(newStatus)
        dbSession.commit()

    if not fieldExists(dbSession, Status.status_name, "Quote Sent"):
        newStatus = Status(status_name = "Quote Sent")
        dbSession.add(newStatus)
        dbSession.commit()

    if not fieldExists(dbSession, Status.status_name, "Waiting for Alberta1Call"):
        newStatus = Status(status_name = "Waiting for Alberta1Call")
        dbSession.add(newStatus)
        dbSession.commit()

    if not fieldExists(dbSession, Status.status_name, "Installation Pending"):
        newStatus = Status(status_name = "Installation Pending")
        dbSession.add(newStatus)
        dbSession.commit()

    if not fieldExists(dbSession, Status.status_name, "Installing"):
        newStatus = Status(status_name = "Installing")
        dbSession.add(newStatus)
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

@app.route('/acceptUser/', methods=['POST'])
@login_required
@roles_required('admin')
def acceptUser():
    if request.method == 'POST':
        user_id = request.form["user_id"]
        print(user_id)
        user = dbSession.query(User).filter(User.id == user_id).all()
        userDatastore.activate_user(user[0])
        user[0].active = True
        dbSession.commit()
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
    status = request.args.get('status')

    # Because seeing "None" in the dropdown menu is unsettling, even if it is
    # treated as "All"
    if (status is None or status == "None"):
        cust_id = request.args.get('cust_id')
        return redirect(url_for('projects', cust_id=cust_id, status="All"))

    return render_template("projects.html")

@app.route('/customerinfo/')
@login_required
@roles_required('primary')
def customerinfo():
    status = request.args.get('status')

    # Because seeing "None" in the dropdown menu is unsettling, even if it is
    # treated as "All"

    return render_template("customerinfo.html")

@app.route('/autocomplete/', methods=["GET"])
@login_required
@roles_required('primary')
def autocomplete():
    # pulls in customers to populate dropdown table in new project
    search = request.args.get("q")
    customers = dbSession.query(Customer).filter(Customer.company_name == current_user.company_name).all()
    return jsonify(customers)


@app.route('/newproject/', methods=['GET', 'POST'])
@login_required
@roles_required('primary')
def newproject():
    if request.method == 'POST':
        customer = request.form["customer"]
        customer = customer.split("-")
        customerId = customer[1]
        projectname = request.form["name"]
        address = request.form["address"]
        success = Projects.createProject(customerId, "Not Reached",  address,
                                         current_user.company_name, projectname)
        return redirect(url_for('projects', status="All"))
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
    attachmentString = Messages.materialListAttachment(project)
    attachment = Email.makeAttachment(Messages.materialListPath,
        attachmentString)

    if attachment is not None:
        return redirect(url_for("static", filename=attachment[7:]))

    return redirect(url_for("projectinfo", proj_id=proj_id))

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
    company = dbSession.query(Company).filter(
        Company.company_name == project.company_name).one()
    message = Messages.materialListMessage(company)
    attachmentString = Messages.materialListAttachment(project)
    attachment = Email.makeAttachment(Messages.materialListPath,
        attachmentString)
    
    supplierEmail = "hey@hey.hey"

    if attachment is not None:
        Email.send(app, mail, project.company_name, supplierEmail,
            "Material list", message, "Material list", attachment)
    
    return redirect(url_for("projectinfo", proj_id=proj_id))

# delete later, just for testing note
@app.route('/projectinfo/', methods = ['GET', 'POST', 'PUT'])
@login_required
@roles_required('primary')
def projectinfo():
    if request.method == "GET":
        project_id = request.args.get('proj_id')
        if project_id is not None:

            json_quotepic = Projects.getdrawiopic(project_id)

            # Get relative path to project pictures
            imgPath = repr(os.path.join('..', Pictures.directory, ''))

            return render_template("projectinfo.html", path = imgPath, drawiopic = json.dumps(json_quotepic))

    else:
        # POST?
        return render_template("projectinfo.html", company = current_user.company_name)

@app.route('/uploadpicture/', methods = ['GET', 'POST'])
@login_required
@roles_required('primary')
def uploadpicture():
    if request.method == 'POST':
        project_id = request.form['proj_id']
        picture = request.files['picture']

        # Store the picture in the database
        Pictures.addPicture(app.root_path, project_id, picture)

        return redirect(url_for('projectinfo', proj_id = project_id))

@app.route('/saveDiagram/', methods = ['POST'])
@login_required
@roles_required('primary')
def saveDiagram():
    # parse draw io image and get coordinates and measurements
    project_id = request.args.get('proj_id')
    image = request.form['image'] #long url
    parsed = DiagramParser.parse(image)

    # Test parsed output
    check = str(parsed)
    if check == '[]':
        print("WE OUT")
    print(parsed)

    json_quotepic = Projects.getdrawiopic(project_id)
    qid = json_quotepic[0].get("quote_id")

    # If parsed is empty don't changed the drawing
    if check !=  '[]':
        update = Projects.updatedrawiopic(qid, 5, image, 0)

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
