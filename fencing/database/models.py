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
    email = Column(String(255))
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
    status_number = Column(Integer, unique = True)

    def __init__(self, status_name, status_number):
        self.status_name = status_name
        self.status_number = status_number

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'status_name'         : self.status_name,
            'status_number'       : self.status_number
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
    layout_selected = Column('layout_selected', Integer, ForeignKey('layout.layout_id', ondelete="SET NULL"))
    appearance_selected = Column('appearance_selected', Integer, ForeignKey('appearance.appearance_id', ondelete="SET NULL"))
    finalize = Column(Boolean())

    def __init__(self, customer_id, status_name, address, end_date, note,
                 project_name, company_name, layout_selected, appearance_selected, finalize, project_id = None):
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
        self.finalize = finalize

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
			'appearance_selected'       : self.appearance_selected,
            'finalize'                  : self.finalize
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
    style = Column(String(100))
    height = Column(String(100))
    border_colour = Column(String(100))
    panel_colour = Column(String(100))
    base_price = Column(Numeric(12, 2))
    # TODO: Columns referencing material list

    def __init__ (self, appearance_name, project_id, style, height, border_colour, panel_colour, base_price, appearance_id=None):
        self.appearance_id = appearance_id
        self.appearance_name = appearance_name
        self.project_id = project_id
        self.style = style
        self.height = height
        self.border_colour = border_colour
        self.panel_colour = panel_colour
        self.base_price = base_price
        # TODO: initialize data for other columns

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'appearance_id'             : self.appearance_id,
            'appearance_name'           : self.appearance_name,
            'project_id'                : self.project_id,
            'style'                     : self.style,
            'height'                    : self.height,
            'border_colour'             : self.border_colour,
            'panel_colour'              : self.panel_colour,
            'base_price'                : self.base_price
        }

class Material(Base):
    __tablename__ = 'material'
    material_id = Column(Integer, primary_key=True)
    material_name = Column(String(255))
    my_price = Column(Numeric(12, 2))
    pieces_in_bundle = Column(Numeric)
    category = Column(String(255))
    note = Column(String(255))
    company_name = Column('company_name', String(255), ForeignKey('company.company_name'))
    #last_update = Column(DateTime(), default = datetime.datetime.utcnow)

    def __init__(self, material_name, my_price, pieces_in_bundle, category, note, company_name, material_id = None):
        self.material_id = material_id
        self.material_name = material_name
        self.my_price = my_price
        self.pieces_in_bundle = pieces_in_bundle
        self.category = category
        self.note = note
        self.company_name = company_name

class Style(Base):
    __tablename__ = 'style'
    style_id = Column(Integer, primary_key=True)
    style = Column(String(255))
    value = Column(Numeric(12, 2))
    company_name = Column('company_name', String(255), ForeignKey('company.company_name'))

    def __init__(self, style, value, company_name, style_id = None):
        self.style_id = style_id
        self.style = style
        self.value = value
        self.company_name = company_name

class Colour(Base):
    __tablename__ = 'colour'
    colour_id = Column(Integer, primary_key=True)
    colour = Column(String(255))
    value = Column(Numeric(12, 2))
    company_name = Column('company_name', String(255), ForeignKey('company.company_name'))

    def __init__(self, colour, value, company_name, colour_id = None):
        self.colour_id = colour_id
        self.colour = colour
        self.value = value
        self.company_name = company_name

class Height(Base):
    __tablename__ = 'height'
    height_id = Column(Integer, primary_key=True)
    height = Column(String(255))
    value = Column(Numeric(12, 2))
    company_name = Column('company_name', String(255), ForeignKey('company.company_name'))

    def __init__(self, height, value, company_name, height_id = None):
        self.height_id = height_id
        self.height = height
        self.value = value
        self.company_name = company_name

class Gate(Base):
    __tablename__ = 'gate'
    gate_id = Column(Integer, primary_key=True)
    gate = Column(String(255))
    value = Column(Numeric(12, 2))
    company_name = Column('company_name', String(255), ForeignKey('company.company_name'))

    def __init__(self, gate, value, company_name, gate_id = None):
        self.gate_id = gate_id
        self.gate = gate
        self.value = value
        self.company_name = company_name

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
