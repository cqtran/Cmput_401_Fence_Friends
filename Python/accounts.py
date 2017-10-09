import Python.db as DB
from sqlalchemy import *

def authenticate(username, password):
    # Access MySQL and authenticate the username/password
    
    db = DB.getConnection()
    metadata = MetaData(db)
    accounts = Table('accounts', metadata, autoload=True)
	
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

def createAccount(username, email, password):
    # Access MySQL and add in account
    db = DB.getConnection()
    metadata = MetaData(db)
    accounts = Table('accounts', metadata, autoload = True)
    
    i = accounts.insert().values(Username = username, Password = password)
    i.execute()
    
    return True

def requestAccount(username, email, password):
    # TODO
    return