from sqlalchemy import *
from database.db import dbSession, init_db
from database.models import Project, Customer, Layout
from flask.json import jsonify
import json
from flask import Blueprint, request
from flask.json import jsonify
from flask_security.core import current_user
from flask_security import login_required
from flask_security.decorators import roles_required
from api.errors import bad_request
import api.layouts as Layouts
import api.pictures as Pictures
import os

projectBlueprint = Blueprint('projectBlueprint', __name__, template_folder='templates')

@projectBlueprint.route('/saveLayoutSelection/', methods=['POST'])
def saveLayoutSelection():
    project_id = request.args.get("proj_id")
    selected = request.json["selected"]
    project = dbSession.query(Project).filter(
        Project.project_id == project_id).one()
    project.layout_selected = selected
    dbSession.commit()
    return "{}"

@projectBlueprint.route('/getProjectList/', defaults={'customer_id': None}, methods=['GET'])
@projectBlueprint.route('/getProjectList/<int:customer_id>', methods=['GET'])
#@login_required
#@roles_required('primary')
def getProjectList(customer_id):
    """ Returns a list of projects. If a customer id is provided, the list will contain
    only contain projects to the given customer id """
    if request.method == 'GET':
        search = request.args.get("search")
        status = request.args.get('status')
        projectList = dbSession.query(Project)
        projectList.filter(Project.company_name == current_user.company_name)

        if customer_id is not None:
           projectList = projectList.filter(Project.customer_id == customer_id)

        if status is None or status == "All" or status == "None":
            projectList = projectList.filter(Customer.customer_id == Project.customer_id).order_by(desc(Project.start_date))

        else:
            projectList = projectList.filter(Customer.customer_id == Project.customer_id).filter(Project.status_name == status)

        if search is not None and search != "":
            projectList = projectList.filter(
                Project.project_name.contains(search))

        projectList = projectList.order_by(desc(Project.start_date)).all()

        if len(projectList) == 0:
            return bad_request("No projects were found")
        return jsonify(projectList)

@projectBlueprint.route('/getProject/<int:project_id>', methods=['GET'])
#@login_required
#@roles_required('primary')
def getProject(project_id):
    """ Returns a single project of a given project id """
    if request.method == "GET":
        project = dbSession.query(Project)
        project = project.filter(Project.project_id == project_id).all()
        if len(project) == 0:
            return bad_request("The project was not found")
        return jsonify(project)

@projectBlueprint.route('/addproject/', methods=['GET', 'POST'])
#login_required
#roles_required('primary')
def addproject():
    print("test it")
    if request.method == 'POST':
        print("made it")
        customer = request.values.get("customer")
        customer = json.loads(customer)
        print("customers", customer)
        customerId = customer[0]
        projectname = request.values.get("name")
        address = request.values.get("address")
        proj_id = createProject(customerId, "Not Reached",  address,
                                         current_user.company_name, projectname)
        print(proj_id)
        return jsonify(proj_id)

# delete later, just for testing note ---- i think we need this
# I dont think we should have this hosted like this. These belong in their respective API files, Pictures and Layouts
@projectBlueprint.route('/projectdetails/', defaults={'project_id': None}, methods=['GET'])
@projectBlueprint.route('/projectdetails/<int:project_id>', methods=['GET'])
@login_required
@roles_required('primary')
def projectdetails(project_id):
    if request.method == "GET":
        project = dbSession.query(Project).filter(
            Project.project_id == project_id).one()
        selectedLayout = project.layout_selected
        selectedAppearance = project.appearance_selected

        json_layouts = Layouts.getLayoutHelper(project_id)

        # Get relative path to project pictures
        imgPath = repr(os.path.join('..', Pictures.pictureDir, ''))
        tbnPath = repr(os.path.join('..', Pictures.thumbnailDir, ''))

        company = current_user.company_name
        lst = [imgPath, tbnPath, json_layouts, company, selectedLayout,
            selectedAppearance]

        return jsonify(lst)

def updateProjectInfo(project_id, project_name, address, status, note):
    """ Updates the project information of a given project id """
    project = dbSession.query(Project).filter(Project.project_id == project_id).all()

    project[0].project_name = project_name
    project[0].address = address
    project[0].status_name = status
    project[0].note = note

    dbSession.commit()
    return True

def createProject(customerId, statusName, address, companyName, project_name):
    # TODO: Turn this into a route
    #Access MySQL and add in account
    newProject = Project(customer_id = customerId, address = address,
            status_name = statusName, end_date = None, note = '',
            project_name = project_name, company_name = companyName, layout_selected=None, appearance_selected=None)
    dbSession.add(newProject)
    dbSession.commit()
    newLayout = Layouts.createLayout(newProject.project_id)
    newProject.layout_selected = newLayout.layout_id
    # TODO: Set appearance ID as well
    dbSession.commit()
    return newProject.project_id
