from Python.db import Base
from flask_security import UserMixin, RoleMixin
from sqlalchemy import create_engine
from sqlalchemy.orm import relationship, backref
from sqlalchemy import Boolean, DateTime, Column, Integer, \
                       String, ForeignKey, Numeric, LargeBinary

from flask.json import JSONEncoder

def dump_datetime(value):
    """Deserialize datetime object into string form for JSON processing."""
    if value is None:
        return None
    return [value.strftime("%Y-%m-%d")]

class RolesUsers(Base):
    __tablename__ = 'roles_users'
    id = Column(Integer(), primary_key=True)
    user_id = Column('user_id', Integer(), ForeignKey('user.id'))
    role_id = Column('role_id', Integer(), ForeignKey('role.id'))

class Role(Base, RoleMixin):
    __tablename__ = 'role'
    id = Column(Integer(), primary_key=True)
    name = Column(String(80), unique=True)
    description = Column(String(255))

class User(Base, UserMixin):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True)
    username = Column(String(255))
    password = Column(String(255))
    company_name = Column('company_name', String(255), ForeignKey('company.company_name'))
    last_login_at = Column(DateTime())
    current_login_at = Column(DateTime())
    last_login_ip = Column(String(100))
    current_login_ip = Column(String(100))
    login_count = Column(Integer)
    active = Column(Boolean())
    confirmed_at = Column(DateTime())
    roles = relationship('Role', secondary='roles_users',
                         backref=backref('users', lazy='dynamic'))
    
class Company(Base):
    __tablename__ = 'company'
    company_name = Column(String(255), primary_key=True)
    email = Column(String(255), unique=True)

class Customer(Base):
    __tablename__ = 'customer'
    customer_id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True)
    first_name = Column(String(255))
    last_name = Column(String(255))
    cellphone = Column(String(20))
    company_name = Column('company_name', String(255), ForeignKey('company.company_name'))

    def __int__(self, customer_id, email, first_name, last_name, cellphone, company_name):
        self.customer_id = customer_id
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.cellphone = cellphone
        self.company_name = company_name
        
    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'customer_id'        : self.customer_id,
            'email'              : self.email,
            'first_name'         : self.first_name,
            'last_name'          : self.last_name,
            'cellphone'          : self.cellphone,
            'company_name'       : self.company_name
        }    
    
class Status (Base):
    __tablename__ = 'status'

    status_name = Column(String(100), primary_key = True)

class Project(Base):
    __tablename__ = 'project'
    project_id = Column(Integer, primary_key=True)
    customer_id = Column('customer_id', Integer(), ForeignKey('customer.customer_id'))
    status_name = Column('status_name', String(100), ForeignKey('status.status_name'))
    address = Column(String(100))
    start_date = Column(DateTime())
    end_date = Column(DateTime())
    note = Column('Note', String(400))
    
    def __init__(self, project_id, customer_id, status_name, address, start_date, end_date, note:
        self.project_id = project_id
        self.customer_id = customer_id
        self.status_name = status_name
        self.address = address
        self.start_date = start_date
        self.end_date = end_date
        self.note = note
    
    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'project_id'         : self.project_id,
            'customer_id'        : self.customer_id,
            'status_name'        : self.status_name,
            'address'            : self.address,
            'start_date'         : dump_datetime(self.start_date),
            'end_date'           : dump_datetime(self.end_date)
        }
    
class Quote(Base):
    __tablename__ = 'quote'
    quote_id = Column(Integer, primary_key=True)
    project_id = Column('project_id', Integer, ForeignKey('project.project_id'))
    quote = Column(Numeric)
    project_info = Column(LargeBinary)
    note = Column(String(255))
    last_modified = Column(DateTime())
    
    def __init__(self, quote_id, project_id, quote, project_info, note, last_modified):
        self.quote_id = quote_id
        self.project_id = project_id
        self.quote = quote
        self.project_info = project_info
        self.note = note
        self.last_modified = last_modified
    
    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'quote_id'                : self.quote_id,
            'project_id'              : self.project_id,
            'quote'                   : self.quote,
            'project_info'            : self.project_info,
            'note'                    : self.note,
            'last_modified'           : dump_datetime(self.last_modified)
        }
    
class Material(Base):
    __tablename__ = 'material'
    material_id = Column(Integer, primary_key=True)
    material_name = Column(String(255))
    cost = Column(Numeric)


