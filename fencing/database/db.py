#!/usr/bin/python
from sqlalchemy import create_engine, MetaData, exists
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

with open("user.txt", "r") as user:
	lines = user.readlines()

username = lines[0].strip()
password = lines[1].strip()
database = lines[2].strip()
host = lines[3].strip()

engine = create_engine(
    'mysql+mysqlconnector://{username}:{password}@{host}/{database}'.format(
		username=username, password=password, database=database, host=host
	),
    pool_recycle=3600
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
