from sqlalchemy import *
from database.db import dbSession, init_db
from database.models import Project, Customer
from flask.json import jsonify

def getProject(project_id):
    """ Returns the project information of the given project id """
    project = dbSession.query(Project)
    project = project.filter(Project.project_id == project_id).all()
    json_response = [i.serialize for i in project]
    return json_response

def getCompanyProjects(companyName, customer_id = None):
    """ Returns a json list of all projects to a given company """
    projects = dbSession.query(Project)

    # Filter projects to the company
    projects = projects.filter(Customer.company_name == companyName)

    # Filter projects on a given customer_id if provided
    if customer_id is not None:
        projects = projects.filter(customer_id == Project.customer_id)

    # Filter projects with matching customer_ids and execute query
    projects = projects.filter(Customer.customer_id == Project.customer_id).all()

    json_response = [i.serialize for i in projects]
    return json_response

def updateProjectInfo(project_id, project_name, address, status, note):
    """ Updates the project information of a given project id """
    project = dbSession.query(Project).filter(Project.project_id == project_id).all()

    project[0].project_name = project_name
    project[0].address = address
    project[0].status = status
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
