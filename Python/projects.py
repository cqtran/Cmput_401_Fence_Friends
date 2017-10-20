from sqlalchemy import *
from Python.db import dbSession, init_db
from Python.models import Project
import datetime



def createProject(customerId, statusId, address, companyName, project_name):
    #Access MySQL and add in account

    project = Project(customer_id = customerId, status_id = statusId, address = address,
                      start_date =  DateTime(), company_name = companyName, 
                      project_name = project_name)
    dbSession.add(project)
    dbSession.commit()

    return True


def savenote(note, pid):

    #TODO
    project = dbSession.query(Project)
    project = project.filter(Project.project_id == pid).all()
    project[0].note = note
    dbSession.commit()
    #savenoteintoserver = update(Project).where(Project.project_id == pid).values(Note = note)

    return True


