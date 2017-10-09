#!/usr/bin/python
import sqlalchemy

def getConnection():

    engine = sqlalchemy.create_engine(
        'mysql://root:cmput401F3nc1ng@localhost/401TEST'
    )

    return engine
