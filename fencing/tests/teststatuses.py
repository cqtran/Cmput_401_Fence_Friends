import unittest

from flask import json
from database.db import dbSession, Base, engine
from database.models import Status
from tests.testdata import *

import requests

import api.statuses as Statuses

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

    def test_getStatusList(self):
        """ Test for getting a list of project statuses """
        print("\n\n Testing getStatusList API\n")
        response = requests.get('http://localhost:5000/getStatusList/')
        json_obj = json.loads(response.text)
        print("\nGot json response from 'http://localhost:5000/getStatusList/':")
        print(json_obj)

        #assert len(json_obj) == 7:
        pass
