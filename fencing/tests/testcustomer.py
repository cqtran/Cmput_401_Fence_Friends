import unittest

from flask import Flask
from database.db import dbSession, Base, init_db, engine
from database.models import Customer, Project, Company, Status
from tests.testdata import *

import api.customers as Customers

app = Flask(__name__)
app.config['TESTING'] = True
app.config['WTF_CSRF_ENABLED'] = False
app.config['DEBUG'] = False

class TestCustomer(unittest.TestCase):
    def setUp(self):
        """ Initialize, clear, and set starting data """
        init_db()

        # Clear all tables in the database
        for tbl in reversed (Base.metadata.sorted_tables):
            engine.execute(tbl.delete())
        companyTestData()
        statusTestData()

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
        Customers.addCustomer('Kat', 'Kat@gmail.com', '541-689-4681', 'Place','Fence')
        oneCustomerTest = dbSession.query(Customer).all()
        # Test the customer is successfully added
        assert len(oneCustomerTest) == 1

        # Test the information from the found customer
        result = oneCustomerTest[0].serialize
        assert result['first_name'] == 'Kat'
        assert result['email'] == 'Kat@gmail.com'
        assert result['cellphone'] == '541-689-4681'
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
        assert result1['cellphone'] == '541-689-4681'
        assert result1['company_name'] == 'Fence'

        assert result2['first_name'] == 'Jason'
        assert result2['email'] == 'Jason@gmail.com'
        assert result2['cellphone'] == '688-946-8781'
        assert result2['company_name'] == 'Fence'


    def test_updateCustomerInfo(self):
        """ Test for updating customer information """
        pass

if __name__ == '__main__':
    unittest.main()
