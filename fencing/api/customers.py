from sqlalchemy import *
from database.db import dbSession, init_db
from database.models import Customer, Company

def addCustomer(name, email, ph, addr, cname):
    """Add a customer to the database with the given field values"""
    customer = Customer(email = email, first_name = name, cellphone = ph, company_name = cname)
    dbSession.add(customer)
    dbSession.commit()

    return True

def getCustomer(customer_id):
    """ Returns a json of customer information of the given customer id """
    customer = dbSession.query(Customer)
    customer = customer.filter(Customer.customer_id == customer_id).all()
    json_response = [i.serialize for i in customer]
    return json_response

def getCompanyCustomers(company_name):
    """ Returns a json list of all customers to a given company """
    customers = dbSession.query(Customer)
    customers = customer.filter(Customer.company_name == company_name).all()
    json_response = [i.serialize for i in customers]
    return json_response

def updateCustomerInfo(customer_id, email, first_name, cellphone):
    """ Updates the customer information of a given customer id """
    customer = dbSession.query(Customer).filter(Customer.customer_id == customer_id).all()

    customer[0].email = email
    customer[0].first_name = first_name
    customer[0].cellphone = cellphone

    dbSession.commit()
    return True
