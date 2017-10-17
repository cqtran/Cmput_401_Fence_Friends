import Python.db as DB
from sqlalchemy import *
from Python.db import dbSession, init_db
from Python.models import Customer

def addCustomer(name, email, ph, addr, cname):

    customer = Customer(email = email, first_name = name, cellphone = ph, company_name = cname)
    dbSession.add(customer)
    dbSession.commit()

    return True






def displayCustomers(company_id):
    db = DB.getConnection()
    metadata = MetaData(db)
    customers = Table('Customers', metadata, autoload=True)
    s = customers.select(customers.c.Company_ID == company_id)
    result = s.execute()
    listofcustomers = []
    for row in result:
        listofcustomers.append(row.First_name)
    return listofcustomers

def getCustomer(customer_id):
    db = DB.getConnection()
    metadata = MetaData(db)
    customers = Table('Customers', metadata, autoload=True)
    s = customers.select(customers.c.Customer_ID == customer_id)
    result = s.fetchone()
    return result