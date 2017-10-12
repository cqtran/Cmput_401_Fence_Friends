import Python.db as DB
from sqlalchemy import *

def authenticate(username, password):
    # Access MySQL and authenticate the username/password
    
    db = DB.getConnection()
    metadata = MetaData(db)
    accounts = Table('Accounts', metadata, autoload=True)
	
    s = accounts.select(and_(accounts.c.Username == username, accounts.c.Password == password))
    rs = s.execute()

    numrows = 0
    for row in rs:
        print(row.Username, row.Password)
        numrows += 1
        
    rs.close()
    
    print(numrows)
    if numrows == 1:
        return True
    return False

def createAccount(username, password, email):
    #Access MySQL and add in account
    db = DB.getConnection()
    metadata = MetaData(db)
    accounts = Table('Accounts', metadata, autoload = True)
    
    i = accounts.insert().values(Username = username, Password = password, Email = email)
    i.execute()
    
    return True

def requestAccount(username, email, password):
    # TODO
    return


# def getCompany(username):
#     db = DB.connection()
#     metadata = MetaData(db)
#     accounts = Tables('Accounts', metadata, autoload=True)
#     s = accounts.select(and_ (accounts.c.Username == username, accouts.c.Company_ID))
#     rs = s.execute()

#     for row in rs:
#         print(row.Username, row.Company_ID)
#         return Company_ID
#     return False

