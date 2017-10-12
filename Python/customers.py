import Python.db as DB
from sqlalchemy import *

def addCustomer(name, email, ph, addr):
    db = DB.getConnection()
    metadata = MetaData(db)
    customers = Table('Customers', metadata, autoload=True)
    add = customers.insert().values(First_name = name, Email = email, Cellphone = ph, Last_name = addr)
    add.execute()

    return True

