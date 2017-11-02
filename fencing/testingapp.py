import os
import unittest

from flask import Flask
from database.db import dbSession, Base, init_db, fieldExists, engine
from database.models import Customer, Project, Company, Status

import api.customers as Customers
import api.projects as Projects

app = Flask(__name__)

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
        newCompany = Company(company_name = "Fence", email = "e@e.c")
        newStatus = Status(status_name = "Not Reached")
        dbSession.add(newCompany)
        dbSession.add(newStatus)
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
        pass

    def test_getCompanyCustomers(self):
        """ Test for getting all customers of company """
        pass

    def test_updateCustomerInfo(self):
        """ Test for updating customer information """
        pass

    def test_createProject(self):
        """ Test for creating a project """
        newCustomer = Customer(customer_id = 1, first_name = 'Kat', email = 'Kat@gmail.com', cellphone = '555-555-5555', company_name = 'Fence')
        dbSession.add(newCustomer)
        dbSession.commit()

        # Test if there are to projects
        noProjectTest = dbSession.query(Project).all()
        assert len(noProjectTest)  == 0

        # Try adding a project through Project api
        Projects.createProject(1, 'Not Reached', 'Somewhere Ave', 'Fence', 'A fun fencing project')
        oneProjectTest = dbSession.query(Project).all()

        # Test if the project is successfully added
        assert len(oneProjectTest) == 1

        # Test the information from the found project
        result = oneProjectTest[0].serialize
        assert result['status_name'] == 'Not Reached'
        assert result['address'] == 'Somewhere Ave'
        assert result['project_name'] == 'A fun fencing project'

    def test_savingNote(self):
        # TODO: This function may be deprecated
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
