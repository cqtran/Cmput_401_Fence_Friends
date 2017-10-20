from sqlalchemy import *
from Python.db import dbSession, init_db
from Python.models import Customer

def addCustomer(name, email, ph, addr, cname):
    """Add a customer to the database with the given field values"""
    customer = Customer(email = email, first_name = name, cellphone = ph, company_name = cname)
    dbSession.add(customer)
    dbSession.commit()

    return True
