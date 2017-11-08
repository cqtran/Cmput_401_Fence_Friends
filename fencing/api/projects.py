from sqlalchemy import *
from database.db import dbSession, init_db
from database.models import Project, Customer
from flask.json import jsonify

from flask import Blueprint, request
from flask.json import jsonify
from flask_security.core import current_user
from flask_security import login_required
from flask_security.decorators import roles_required

projectBlueprint = Blueprint('projectBlueprint', __name__, template_folder='templates')

@projectBlueprint.route('/getProjectList/', defaults={'customer_id': None}, methods=['GET'])
@projectBlueprint.route('/getProjectList/<int:customer_id>', methods=['GET'])
#@login_required
#@roles_required('primary')
def getProjectList(customer_id):
    if request.method == 'GET':
        projectList = dbSession.query(Project)
        #projectList = projectList.filter(Customer.company_name == current_user.company_name)
        if customer_id is not None:
            projectList = projectList.filter(customer_id == Project.customer_id)
        projectList = projectList.filter(Customer.customer_id == Project.customer_id).all()
        return jsonify(projectList)

@projectBlueprint.route('/getProject/<int:project_id>', methods=['GET'])
#@login_required
#@roles_required('primary')
def getProject(project_id):
    if request.method == "GET":
        project = dbSession.query(Project)
        project = project.filter(Project.project_id == project_id).all()
        return jsonify(project)

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
    #Access MySQL and add in account
    newProject = Project(customer_id = customerId, address = address,
            status_name = statusName, end_date = None, note = '',
            project_name = project_name, company_name = companyName)

    dbSession.add(newProject)
    dbSession.commit()

    return True

def savenote(note, pid):
    """Save the given note to the database"""
    project = dbSession.query(Project)
    project = project.filter(Project.project_id == pid).all()
    project[0].note = note
    dbSession.commit()
    #savenoteintoserver = update(Project).where(Project.project_id == pid).values(Note = note)

    return True
