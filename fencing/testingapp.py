import os
import unittest

from flask import Flask
from database.db import dbSession, Base, init_db, fieldExists, engine
from database.models import Customer, Project, Company, Status

import api.customers as Customers
import api.projects as Projects

app = Flask(__name__)

# Helper function for inserting customer test data
def customerTestData():
    newCustomer1 = Customer(customer_id = 1, first_name = 'Kat', email = 'Kat@gmail.com', cellphone = '541-689-4681', company_name = 'Fence')
    newCustomer2 = Customer(customer_id = 2, first_name = 'Davis', email = 'Davis@gmail.com', cellphone = '761-158-2113', company_name = 'Builder')
    newCustomer3 = Customer(customer_id = 3, first_name = 'Jason', email = 'Jason@gmail.com', cellphone = '688-946-8781', company_name = 'Fence')
    dbSession.add(newCustomer1)
    dbSession.add(newCustomer2)
    dbSession.add(newCustomer3)
    dbSession.commit()

# Helper function for inserting project test data
def projectTestData():
    newProject1 = Project(1, 'Not Reached', 'Bear St', None, 'A fun fencing project', "Kat's house fence", 'Fence')
    newProject2 = Project(1, 'Not Reached', 'Grand Ave', None, 'Dog lives here', "Kat's second house fence", 'Fence')
    dbSession.add(newProject1)
    dbSession.add(newProject2)
    dbSession.commit()

class TestCase(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        init_db()

        # Clear all tables in the database
        for tbl in reversed (Base.metadata.sorted_tables):
            engine.execute(tbl.delete())

        # Insert required info such as companies and status
        newCompany1 = Company(company_name = "Fence", email = "Fence@Fence.com")
        newCompany2 = Company(company_name = "Builder", email = "Build@Build.com")

        dbSession.add(newCompany1)
        dbSession.add(newCompany2)

        status1 = Status(status_name = "Not Reached")
        dbSession.add(status1)

        dbSession.commit()

    def tearDown(self):
        """Clear all tables"""
        for tbl in reversed (Base.metadata.sorted_tables):
            engine.execute(tbl.delete())
        dbSession.remove()

    def test_addCustomer(self):
        """ Test for adding a customer """
        # Test if there are no customers
        noCustomerTest = dbSession.query(Customer).all()
        assert len(noCustomerTest) == 0

        # Try adding a customer through Customers api
        Customers.addCustomer('Kat', 'Kat@gmail.com', '555-555-5555', 'Place','Fence')
        oneCustomerTest = dbSession.query(Customer).all()
        # Test the customer is successfully added
        assert len(oneCustomerTest) == 1

        # Test the information from the found customer
        result = oneCustomerTest[0].serialize
        assert result['first_name'] == 'Kat'
        assert result['email'] == 'Kat@gmail.com'
        assert result['cellphone'] == '555-555-5555'
        assert result['company_name'] == 'Fence'

    def test_getCustomer(self):
        """ Test for getting a customer of a customer id """
        customerTestData()

        # Test getting customer with id = 2
        customer2 = Customers.getCustomer(2)
        assert len(customer2) == 1
        result = customer2[0]

        assert result['first_name'] == 'Davis'
        assert result['email'] == 'Davis@gmail.com'
        assert result['cellphone'] == '761-158-2113'
        assert result['company_name'] == 'Builder'

        # Test getting customer with id = 3
        customer3 = Customers.getCustomer(3)
        assert len(customer3) == 1
        result = customer3[0]

        assert result['first_name'] == 'Jason'
        assert result['email'] == 'Jason@gmail.com'
        assert result['cellphone'] == '688-946-8781'
        assert result['company_name'] == 'Fence'

    def test_getCompanyCustomers(self):
        """ Test for getting all customers of company """
        customerTestData()

        # Test getting customers from the only the 'Fence' company
        fenceCustomers = Customers.getCompanyCustomers('Fence')
        assert len(fenceCustomers) == 2
        result1 = fenceCustomers[0]
        result2 = fenceCustomers[1]

        assert result1['first_name'] == 'Kat'
        assert result1['email'] == 'Kat@gmail.com'
        assert result1['cellphone'] == '555-555-5555'
        assert result1['company_name'] == 'Fence'

        assert result2['first_name'] == 'Jason'
        assert result2['email'] == 'Jason@gmail.com'
        assert result2['cellphone'] == '688-946-8781'
        assert result2['company_name'] == 'Fence'


    def test_updateCustomerInfo(self):
        """ Test for updating customer information """
        pass

    def test_createProject(self):
        """ Test for creating a project """
        customerTestData()

        # Test if there are to projects
        noProjectTest = dbSession.query(Project).all()
        assert len(noProjectTest)  == 0

        # Try adding a project through Project api
        Projects.createProject(1, 'Not Reached', 'Somewhere Ave', 'Fence', "Kat's house fence")
        oneProjectTest = dbSession.query(Project).all()

        # Test if the project is successfully added
        assert len(oneProjectTest) == 1

        # Test the information from the found project
        result = oneProjectTest[0].serialize
        assert result['status_name'] == 'Not Reached'
        assert result['address'] == 'Somewhere Ave'
        assert result['project_name'] == "Kat's house fence"

    def test_savingNote(self):
        # CHANGED: This function may be deprecated
        newCustomer = Customer(customer_id = 1, first_name = 'Kat', email = 'Kat@gmail.com', cellphone = '555-555-5555', company_name = 'Fence')
        dbSession.add(newCustomer)
        dbSession.commit()

        Projects.createProject(1, 'Not Reached', 'Somewhere Ave', 'Fence', 'A fun fencing project')
        oneProjectTest = dbSession.query(Project).all()
        result = oneProjectTest[0].serialize

        # Test if the note is empty
        assert result['note'] == None

        Projects.savenote('This is a new note', oneProjectTest[0].project_id)
        oneProjectTest = dbSession.query(Project).all()

        # Test if the not has changed
        result = oneProjectTest[0].serialize
        assert result['note'] == 'This is a new note'

    def test_getProject(self):
        """ Test for getting a project of a project id """
        pass

    def test_getCompanyProjects(self):
        """ Test for getting all projects of a company """
        pass

    def test_updateProjectInfo(self):
        """ Test the updating of project information """
        pass

    def test_addPicture(self):
        """ Test adding a picture to a project """
        pass

    def test_getPictures(self):
        """ Test getting pictures of a project """
        pass


if __name__ == '__main__':
    unittest.main()
