from sqlalchemy import *
from database.db import dbSession, init_db
from database.models import Customer, Company

from flask import Blueprint, request
from flask.json import jsonify
from flask_security.core import current_user
from flask_security import login_required
from flask_security.decorators import roles_required

customerBlueprint = Blueprint('customerBlueprint', __name__, template_folder='templates')

@customerBlueprint.route('/getCustomerList', methods=['GET'])
@login_required
@roles_required('primary')
def getCustomerList():
    if request.method == 'GET':
        customers = dbSession.query(Customer)
        customers = customers.filter(Customer.company_name == current_user.company_name).all()
        return jsonify(customers)

@customerBlueprint.route('/getCustomer/<int:customer_id>', methods=['GET'])
@login_required
@roles_required('primary')
def getCustomer(customer_id):
    if request.method == 'GET':
        customer = dbSession.query(Customer)
        customer = customer.filter(Customer.customer_id == customer_id).all()
        return jsonify(customer)

def addCustomer(name, email, ph, addr, cname):
    """Add a customer to the database with the given field values"""
    customer = Customer(email = email, first_name = name, cellphone = ph, company_name = cname)
    dbSession.add(customer)
    dbSession.commit()

    return True

def updateCustomerInfo(customer_id, email, first_name, cellphone):
    """ Updates the customer information of a given customer id """
    customer = dbSession.query(Customer).filter(Customer.customer_id == customer_id).all()

    customer[0].email = email
    customer[0].first_name = first_name
    customer[0].cellphone = cellphone

    dbSession.commit()
    return True
