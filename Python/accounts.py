import Python.db as DB
import sqlalchemy import *

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
	
    print(numrows)
    if numrows == 1:
        return True
    return False

def createAccount():
    # TODO
    return

def requestAccount(username, email, password):
    # TODO
    return