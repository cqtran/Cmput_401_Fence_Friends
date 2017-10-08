import db as DB

def authenticate(username, password):
    # Access MySQL and authenticate the username/password
    
    connection = DB.getConnection()
    cursor = connection.cursor()

    statement = "SELECT * FROM accounts WHERE Username = '" + username + "' AND Password = '" + password + "'"
    cursor.execute(statement)

    numrows = int(cursor.rowcount)
    print(numrows)

    cursor.close()
    connection.close()
    
    if numrows == 1:
        return True   
    return False

def createAccount():
    # TODO
    return

def requestAccount(username, email, password):
    # TODO
    
    return