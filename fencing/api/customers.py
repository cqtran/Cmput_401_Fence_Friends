from sqlalchemy import *
from database.db import dbSession, init_db
from database.models import Customer, Project
from api.projects import removeProject

from flask import Blueprint, request
from flask.json import jsonify
from flask_security.core import current_user
from flask_security import login_required
from flask_security.decorators import roles_required
from api.errors import *

"""Api relating to get, update, or delete Customer info"""

customerBlueprint = Blueprint('customerBlueprint', __name__, template_folder='templates')

@customerBlueprint.route('/getCustomerList/', defaults={'company_name': None}, methods=['GET'])
@customerBlueprint.route('/getCustomerList/<company_name>', methods=['GET'])
@login_required
@roles_required('primary')
def getCustomerList(company_name):
    """ Returns a list of customers. If a company name is provided, the list will
    only contain customers from that company"""
    if request.method == 'GET':
        company_name = current_user.company_name
        search = request.args.get("search")
        customers = dbSession.query(Customer)
        if company_name is not None:
            # filter customer list by company_name if provided
            customers = customers.filter(Customer.company_name == company_name)
        if search is not None and search != "":
            customers = customers.filter(Customer.first_name.contains(search))
        customers = customers.all()
        if len(customers) == 0:
            return bad_request("No customers were found")
        return jsonify(customers)

@customerBlueprint.route('/getCustomer/<int:customer_id>', methods=['GET'])
@login_required
@roles_required('primary')
def getCustomer(customer_id):
    """ Returns a response for a single customer of the given customer id """
    if request.method == 'GET':
        customer = dbSession.query(Customer)
        customer = customer.filter(Customer.customer_id == customer_id).all()
        if len(customer) == 0:
            return bad_request("The customer was not found")
        return jsonify(customer)

def addCustomer(name, email, ph, addr, cname):
    """Add a customer to the database with the given field values"""
    customer = Customer(email = email, first_name = name, cellphone = ph, company_name = cname)
    dbSession.add(customer)
    dbSession.commit()

    return True

@customerBlueprint.route('/deletecustomer/', methods = ['POST'])
@login_required
@roles_required('primary')
def deleteproject():
    """Gets the customer id and removes their projects"""
    cust_id = request.values.get("cust_id")
    removeCustomer(cust_id)

    return created_request("Good")

def removeCustomer(cust_id):
    """Helper function for deleteproject()"""
    #Get all projects
    projects = dbSession.query(Project).filter(Project.customer_id == cust_id)

    for proj in projects:
        removeProject(proj.project_id)

    # Cascade delete all information related to project
    cust = dbSession.query(Customer).filter(Customer.customer_id == cust_id).one()
    dbSession.delete(cust)
    dbSession.commit()

@customerBlueprint.route('/updatecustomer/', methods=['POST'])
@login_required
@roles_required('primary')
def updateCustomer():
    """Updates customer information in the database"""
    if request.method == "POST":
        customer_id = request.values.get("cust_id")
        f_name = request.values.get("fname")
        email = request.values.get("email")
        cell = request.values.get("cellphone")

        updateCustomerInfo(customer_id = customer_id, email = email, first_name = f_name,
                            cellphone = cell)

        return jsonify(customer_id)

def updateCustomerInfo(customer_id, email, first_name, cellphone):
    """ Updates the customer information of a given customer id """
    customer = dbSession.query(Customer).filter(Customer.customer_id == customer_id).all()

    customer[0].email = email
    customer[0].first_name = first_name
    customer[0].cellphone = cellphone

    dbSession.commit()
    return True
