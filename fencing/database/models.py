from database.db import Base
from flask_security import UserMixin, RoleMixin
from sqlalchemy import create_engine
from sqlalchemy import *
from sqlalchemy.orm import relationship, backref
from sqlalchemy import Boolean, DateTime, Column, Integer, \
                       String, ForeignKey, LargeBinary

from sqlalchemy.sql import func
from flask.json import JSONEncoder
import datetime

def dump_datetime(value):
    """Deserialize datetime object into string form for JSON processing"""
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
    cellphone = Column(String(20))
    company_name = Column('company_name', String(255), ForeignKey('company.company_name', ondelete="CASCADE"))

    def __int__(self, customer_id, email, first_name, cellphone, company_name):
        self.customer_id = customer_id
        self.email = email
        self.first_name = first_name
        self.cellphone = cellphone
        self.company_name = company_name

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'customer_id'        : self.customer_id,
            'email'              : self.email,
            'first_name'         : self.first_name,
            'cellphone'          : self.cellphone,
            'company_name'       : self.company_name
        }

class Status (Base):
    __tablename__ = 'status'
    status_name = Column(String(100), primary_key = True)

    def __init__(self, status_name):
        self.status_name = status_name

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'status_name'         : self.status_name
        }

class Project(Base):
    __tablename__ = 'project'
    project_id = Column(Integer, primary_key=True)
    customer_id = Column('customer_id', Integer, ForeignKey('customer.customer_id', ondelete="CASCADE"))
    status_name = Column('status_name', String(100), ForeignKey('status.status_name', ondelete="CASCADE"))
    company_name = Column('company_name', String(255), ForeignKey('company.company_name', ondelete="CASCADE"))
    address = Column(String(100))
    start_date = Column(DateTime(), default = datetime.datetime.utcnow)
    end_date = Column(DateTime())
    note = Column('Note', String(400))
    project_name = Column("project_name", String(50))
    layout_selected = Column('layout_selected', Integer, ForeignKey('layout.layout_id', ondelete="CASCADE"))
    appearance_selected = Column('appearance_selected', Integer, ForeignKey('appearance.appearance_id', ondelete="CASCADE"))

    def __init__(self, customer_id, status_name, address, end_date, note,
                 project_name, company_name, layout_selected, appearance_selected, project_id = None):
        self.project_id = project_id
        self.customer_id = customer_id
        self.status_name = status_name
        self.address = address
        self.end_date = end_date
        self.note = note
        self.project_name = project_name
        self.company_name = company_name
        self.layout_selected = layout_selected
        self.appearance_selected = appearance_selected

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'project_id'                : self.project_id,
            'customer_id'               : self.customer_id,
            'status_name'               : self.status_name,
            'address'                   : self.address,
            'start_date'                : dump_datetime(self.start_date),
            'end_date'                  : dump_datetime(self.end_date),
            'note'                      : self.note,
            'project_name'              : self.project_name,
            'layout_selected'           : self.layout_selected,
			'appearance_selected'       : self.appearance_selected
        }

class Layout(Base):
    __tablename__ = 'layout'
    layout_id = Column(Integer, primary_key=True)
    project_id = Column('project_id', Integer, ForeignKey('project.project_id', ondelete="CASCADE"))
    layout_name = Column(String(100))
    layout_info = Column(TEXT)

    def __init__(self, project_id, layout_name, layout_info, layout_id=None):
        self.layout_id = layout_id
        self.layout_name = layout_name
        self.project_id = project_id
        self.layout_info = layout_info

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'layout_id'                 : self.layout_id,
            'layout_name'               : self.layout_name,
            'project_id'                : self.project_id,
            'layout_info'               : self.layout_info,
        }

class Quote(Base):
	# Should not currently be in use
    __tablename__ = 'quote'
    quote_id = Column(Integer, primary_key=True)
    project_id = Column('project_id', Integer, ForeignKey('project.project_id', ondelete="CASCADE"))
    quote_name = Column(TEXT)
    quote = Column(Integer)
    layout_id = Column('layout_id', Integer, ForeignKey('layout.layout_id', ondelete="CASCADE"))
    appearance_id = Column('appearance_id', Integer, ForeignKey('appearance.appearance_id', ondelete="CASCADE"))

class Appearance(Base):
    __tablename__ = 'appearance'
    appearance_id = Column(Integer, primary_key=True)
    appearance_name = Column(String(100))
    project_id = Column('project_id', Integer, ForeignKey('project.project_id', ondelete="CASCADE"))
    panel_gap = Column(String(100))
    height = Column(String(100))
    # TODO: Columns referencing material list

    def __init__ (self, appearance_name, project_id, panel_gap, height, appearance_id=None):
        self.appearance_id = appearance_id
        self.appearance_name = appearance_name
        self.project_id = project_id
        self.panel_gap = panel_gap
        self.height = height
        # TODO: initialize data for other columns

class Material(Base):
    __tablename__ = 'material'
    material_id = Column(Integer, primary_key=True)
    material_name = Column(String(255))
    cost = Column(Numeric)

class Picture(Base):
    __tablename__ = 'picture'
    picture_id = Column(Integer, primary_key=True)
    project_id = Column('project_id', Integer, ForeignKey('project.project_id', ondelete="CASCADE"))
    file_name = Column(String(100))
    thumbnail_name = Column(String(100))
    upload_date = Column(DateTime(), default = datetime.datetime.utcnow)

    def __init__(self, project_id, file_name, thumbnail_name,  picture_id = None):
        self.picture_id = picture_id
        self.project_id = project_id
        self.file_name = file_name
        self.thumbnail_name = thumbnail_name

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'picture_id'                : self.picture_id,
            'project_id'                : self.project_id,
            'file_name'                 : self.file_name,
            'thumbnail_name'            : self.thumbnail_name
        }
