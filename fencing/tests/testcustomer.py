import unittest

from flask import json
from database.db import dbSession, Base, engine
from database.models import Customer
from tests.testdata import *

import requests

import api.customers as Customers

class TestCustomer(unittest.TestCase):
    def setUp(self):
        """ Initialize, clear, and set starting data """

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
        print("\n\n Testing getCustomer API\n")
        customerTestData()

        # Test getting customer with id = 2
        response = requests.get('http://localhost:5000/getCustomer/2')
        json_obj = json.loads(response.text)
        print("\nGot json response from 'http://localhost:5000/getCustomer/2':")
        print(json_obj)

        assert len(json_obj) == 1
        result = json_obj[0]
        # Test the information contained in the object with expected information
        assert result['first_name'] == 'Davis'
        assert result['email'] == 'Davis@gmail.com'
        assert result['cellphone'] == '761-158-2113'
        assert result['company_name'] == 'Builder'
        print("Json response is expected")

        # Test getting non-existing customer with id = 4.
        response = requests.get('http://localhost:5000/getCustomer/4')
        json_obj = json.loads(response.text)
        print("\nGot json response from 'http://localhost:5000/getCustomer/4':")
        print(json_obj)
        assert len(json_obj) == 0
        print("Json response is expected")

    def test_getCustomerList(self):
        """ Test for getting all customers of company """
        print("\n\n Testing getCustomerList API\n")
        customerTestData()

        # Test getting customers from the only the 'Fence' company
        response = requests.get('http://localhost:5000/getCustomerList/Fence')
        json_obj = json.loads(response.text)
        print(json_obj)
        assert len(json_obj) == 2
        result1 = json_obj[0]
        result2 = json_obj[1]

        assert result1['first_name'] == 'Kat'
        assert result1['email'] == 'Kat@gmail.com'
        assert result1['cellphone'] == '541-689-4681'
        assert result1['company_name'] == 'Fence'

        assert result2['first_name'] == 'Jason'
        assert result2['email'] == 'Jason@gmail.com'
        assert result2['cellphone'] == '688-946-8781'
        assert result2['company_name'] == 'Fence'
        print("Json response is expected")

    def test_updateCustomerInfo(self):
        """ Test for updating customer information """
        pass

if __name__ == '__main__':
    unittest.main()
