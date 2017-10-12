#!/usr/bin/python
import sqlalchemy

def getConnection():

    engine = sqlalchemy.create_engine(
<<<<<<< Updated upstream
    	#change password to your db password and root to your db username
        'mysql+mysqlconnector://root:password@localhost/data'
=======
        'mysql ://root:cmput401F3nc1ng@localhost/401TEST'
>>>>>>> Stashed changes
    )

    return engine
