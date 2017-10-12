#!/usr/bin/python
import sqlalchemy

def getConnection():

    engine = sqlalchemy.create_engine(
    #change password to your db password and root to your db username
    'mysql+mysqlconnector://root:password@localhost/data'
 	)

    return engine
