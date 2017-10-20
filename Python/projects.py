import Python.db as DB
from sqlalchemy import *
from Python.db import dbSession, init_db
from Python.models import Project



def createProject(customerId, statusId, address, note, startDate):
    #Access MySQL and add in account
    project = Project(customer_id = customerId, status_id = statusId, address = address,
                      start_date =  sqlalchemy.DateTime())
    dbSession.add(project)
    dbSession.commit()

    return True


def savenote(note, pid):

    #TODO

    savenoteintoserver = update(Project).where(Project.project_id == pid).values(Note = note)

    return True





