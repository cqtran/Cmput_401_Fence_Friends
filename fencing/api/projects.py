from sqlalchemy import *
from database.db import dbSession, init_db
from database.models import Project, Customer, Layout, Status, Picture
from diagram.DiagramParser import DiagramParser
from diagram.JsonDiagramData import JsonDiagramData
from flask.json import jsonify
import json
from flask import Blueprint, request
from flask_security.core import current_user
from flask_security import login_required
from flask_security.decorators import roles_required
from api.errors import *
import api.layouts as Layouts
import api.appearances as Appearances
import api.pictures as Pictures
import os
import datetime

projectBlueprint = Blueprint('projectBlueprint', __name__, template_folder='templates')

@projectBlueprint.route('/saveAppearanceSelection/', methods=['POST'])
def saveAppearanceSelection():
    project_id = request.args.get("proj_id")
    selected = request.json["selected"]
    project = dbSession.query(Project).filter(
        Project.project_id == project_id).one()
    project.appearance_selected = selected
    dbSession.commit()
    return "{}"

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
        projectList = projectList.filter(Project.company_name == current_user.company_name)

        if customer_id is not None:
           projectList = projectList.filter(Project.customer_id == customer_id)

        if status is None or status == "All" or status == "None":
            projectList = projectList.filter(Customer.customer_id == Project.customer_id)

        else:
            projectList = projectList.filter(Customer.customer_id == Project.customer_id).filter(Project.status_name == status)

        if search is not None and search != "":
            projectList = projectList.filter(
                or_(Project.project_name.contains(search),
                Project.address.contains(search)))

        projectList = projectList.filter(Project.status_name == Status.status_name).order_by(Status.status_number)
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

@projectBlueprint.route('/addproject/', methods=['POST'])
#login_required
#roles_required('primary')
def addproject():
    if request.method == 'POST':
        customer = request.values.get("customer")
        customer = json.loads(customer)
        customerId = customer[0]
        projectname = request.values.get("name")
        address = request.values.get("address")
        proj_id = createProject(customerId, "Not Reached",  address,
                                         current_user.company_name, projectname)
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

        layouts = Layouts.getLayouts(project_id)
        json_layouts = [i.serialize for i in layouts]
        parsedLayouts = [DiagramParser.parse(i.layout_info) for i in layouts]
        displayStrings = []
        jsonDiagramData = []
        json_appearances = Appearances.getAppearanceList(project_id)
        customer = dbSession.query(Customer).filter(
            Customer.customer_id == project.customer_id).one()
        customerName = customer.first_name
        customerId = customer.customer_id

        for layout in parsedLayouts:
            if layout is None:
                displayStrings.append([])
                jsonDiagramData.append([])

            else:
                displayStrings.append(layout.displayStrings())
                jsonDiagramData.append(JsonDiagramData.parse(layout))

        # Get relative path to project pictures
        imgPath = repr(os.path.join('..', Pictures.pictureDir, ''))
        tbnPath = repr(os.path.join('..', Pictures.thumbnailDir, ''))

        company = current_user.company_name
        lst = [imgPath, tbnPath, json_layouts, json_appearances, company,
            selectedLayout, selectedAppearance, displayStrings, customerName,
            customerId, jsonDiagramData]

        return jsonify(lst)


@projectBlueprint.route('/updateproject/', methods=['POST'])
@login_required
@roles_required('primary')
def updateProject():
    if request.method == "POST":
        customer = request.values.get("customer")
        customer = json.loads(customer);
        # customer is a list of customer ids
        project_id = request.values.get("proj_id")
        project_name = request.values.get("name")
        address = request.values.get("address")
        status = request.values.get("status")
        note = request.values.get("note")
        end_date = None

        if status == 'Paid' or status == 'No Longer Interested':
            end_date = datetime.datetime.utcnow()

        updateProjectInfo(project_id = project_id, project_name = project_name,
            address = address, status = status, note = note, customer = customer, end_date = end_date)

        print("done")
        return jsonify(project_id)

@projectBlueprint.route('/deleteproject/', methods = ['POST'])
@login_required
@roles_required('primary')
def deleteproject():
    proj_id = request.values.get("proj_id")
    print(proj_id)
    removeProject(proj_id)

    return created_request("Good")

def removeProject(proj_id):
    # Delete image files
    pictures = dbSession.query(Picture).filter(Picture.project_id == proj_id).all()
    for image in pictures:
        Pictures.deleteImageHelper(image.file_name)
        Pictures.deleteImageHelper(image.thumbnail_name)

    # Cascade delete all information related to project
    project = dbSession.query(Project).filter(Project.project_id == proj_id).one()
    dbSession.delete(project)
    dbSession.commit()

def updateProjectInfo(project_id, project_name, address, status, note, customer, end_date):
    """ Updates the project information of a given project id """
    project = dbSession.query(Project).filter(Project.project_id == project_id).all()

    project[0].project_name = project_name
    project[0].address = address
    project[0].status_name = status
    project[0].note = note
    project[0].end_date = end_date
    dbSession.commit()
    return True

def createProject(customerId, statusName, address, companyName, project_name):
    # TODO: Turn this into a route
    #Access MySQL and add in account
    newProject = Project(customer_id = customerId, address = address,
            status_name = statusName, end_date = None, note = '',
            project_name = project_name, company_name = companyName, finalize = False, layout_selected=None, appearance_selected=None)
    dbSession.add(newProject)
    dbSession.commit()
    newAppearance = Appearances.createAppearance(newProject.project_id)
    newProject.appearance_selected = newAppearance.appearance_id
    newLayout = Layouts.createLayout(newProject.project_id)
    newProject.layout_selected = newLayout.layout_id
    dbSession.commit()
    return newProject.project_id
