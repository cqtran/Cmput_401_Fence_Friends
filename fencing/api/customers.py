from sqlalchemy import *
from fencing.database.db import dbSession, init_db
from fencing.database.models import Customer

def addCustomer(name, email, ph, addr, cname):

    customer = Customer(email = email, first_name = name, cellphone = ph, company_name = cname)
    dbSession.add(customer)
    dbSession.commit()

    return True
