import Python.db as DB
from sqlalchemy import *


def createProject(customerId, statusId, address, note, startDate):
    #Access MySQL and add in account
    db = DB.getConnection()
    metadata = MetaData(db)
    accounts = Table('Projects', metadata, autoload = True)
    
    i = accounts.insert().values(Customer_ID = customerId, Status_ID = statusId,
		Address = address, Note = note, Start_Date = startDate)
    i.execute()
    
    return True

