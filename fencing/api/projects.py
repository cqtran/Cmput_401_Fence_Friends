from sqlalchemy import *
from fencing.database.db import dbSession, init_db
from fencing.database.models import Project


def createProject(customerId, statusId, address, note, startDate):
    #Access MySQL and add in account
    project = Project(customer_id = customerId, status_id = statusId, address = address,
                      start_date =  sqlalchemy.DateTime())
    dbSession.add(project)
    dbSession.commit()

    return True


def savenote(note, pid):

    #TODO
    customer = Customer(email = email, first_name = name, cellphone = ph, company_name = cname)
    dbSession.add(customer)
    dbSession.commit()

    return True




