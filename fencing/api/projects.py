from sqlalchemy import *
from fencing.database.db import dbSession, init_db
from fencing.database.models import Project



def createProject(customerId, statusName, address, companyName, project_name):
    #Access MySQL and add in account
    newProject = Project(customer_id = customerId, address = address,
            status_name = statusName, end_date = None, note = None,
            project_name = project_name, company_name = companyName)

    dbSession.add(newProject)
    dbSession.commit()

    return True


def savenote(note, pid):
    """Save the given note to the database"""
    #TODO
    project = dbSession.query(Project)
    project = project.filter(Project.project_id == pid).all()
    project[0].note = note
    dbSession.commit()
    #savenoteintoserver = update(Project).where(Project.project_id == pid).values(Note = note)

    return True


