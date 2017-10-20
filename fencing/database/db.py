#!/usr/bin/python
from sqlalchemy import create_engine, MetaData, exists
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine(
	#change password to your db password and root to your db username
    'mysql+mysqlconnector://root:password@localhost/testdata'
)

dbSession = scoped_session(sessionmaker(autocommit=False,
										autoflush=False,
										bind=engine))

Base = declarative_base()
Base.query = dbSession.query_property()

def init_db():
	import database.models
	Base.metadata.create_all(bind=engine)

def fieldExists(session, fieldName, fieldValue):
	"""
	Return whether a field with the given value exists
	eg. fieldExists(dbSession, Company.company_name, "Fence") returns whether
	the table Company has a row with the company_name field equal to "Fence"
	"""
	return session.query(exists().where(fieldName == fieldValue)).scalar()
