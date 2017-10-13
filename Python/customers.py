import Python.db as DB
from sqlalchemy import *

def addCustomer(name, email, ph, addr):
    db = DB.getConnection()
    metadata = MetaData(db)
    customers = Table('Customers', metadata, autoload=True)
    add = customers.insert().values(First_name = name, Email = email, Cellphone = ph, Last_name = addr
									,Company_ID = 1)
    add.execute()

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