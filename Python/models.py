from Python.db import Base
from flask_security import UserMixin, RoleMixin
from sqlalchemy import create_engine
from sqlalchemy.orm import relationship, backref
from sqlalchemy import Boolean, DateTime, Column, Integer, \
                       String, ForeignKey, Numeric, LargeBinary

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
    company_id = Column('company_id', Integer(), ForeignKey('company.company_id'))
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
    company_id = Column(Integer, primary_key=True)
    name = Column(String(255))
    email = Column(String(255), unique=True)

class Customer(Base):
    __tablename__ = 'customer'
    customer_id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True)
    first_name = Column(String(255))
    last_name = Column(String(255))
    cellphone = Column(String(20))
    company_id = Column('company_id', Integer(), ForeignKey('company.company_id'))
    
class Status (Base):
    __tablename__ = 'status'
    status_id = Column(Integer, primary_key=True)
    status_name = Column(String(100))

class Project(Base):
    __tablename__ = 'project'
    project_id = Column(Integer, primary_key=True)
    customer_id = Column('customer_id', Integer(), ForeignKey('customer.customer_id'))
    status_id = Column('status_id', Integer(), ForeignKey('status.status_id'))
    address = Column(String(100))
    start_date = Column(DateTime())
    end_date = Column(DateTime())
    
class Quote(Base):
    __tablename__ = 'quote'
    quote_id = Column(Integer, primary_key=True)
    project_id = Column('project_id', Integer, ForeignKey('project.project_id'))
    quote = Column(Numeric)
    project_info = Column(LargeBinary)
    note = Column(String(255))
    last_modified = Column(DateTime())
    
class Material(Base):
    __tablename__ = 'material'
    material_id = Column(Integer, primary_key=True)
    material_name = Column(String(255))
    cost = Column(Numeric)