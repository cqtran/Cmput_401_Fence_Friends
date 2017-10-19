#!/usr/bin/python
from sqlalchemy import create_engine, MetaData, exists
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

def getConnection():

    engine = create_engine(
    	#change password to your db password and root to your db username
        'mysql+mysqlconnector://root:password@localhost/data'
    )

    print(engine.table_names())
    meta = MetaData()

    meta.reflect(bind=engine)

    print(meta.tables.keys())

    return engine

engine = create_engine(
	#change password to your db password and root to your db username
    'mysql+mysqlconnector://root:password@localhost/testData'
)

dbSession = scoped_session(sessionmaker(autocommit=False,
										autoflush=False,
										bind=engine))

Base = declarative_base()
Base.query = dbSession.query_property()

def init_db():
	import Python.models
	Base.metadata.create_all(bind=engine)

def fieldExists(session, fieldName, fieldValue):
    return session.query(exists().where(fieldName == fieldValue)).scalar()
