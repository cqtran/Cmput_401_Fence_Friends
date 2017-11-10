import unittest

from flask import json
from database.db import dbSession, Base, engine
from database.models import User
from tests.testdata import *

import requests

class TestUser(unittest.TestCase):
    def setUp(self):
        """ Create, clear and set starting data """

        # Clear all tables in the database
        for tbl in reversed (Base.metadata.sorted_tables):
            engine.execute(tbl.delete())

        companyTestData()
        statusTestData()
        customerTestData()
        projectTestData()

    def tearDown(self):
        """ Clear all tables"""
        for tbl in reversed (Base.metadata.sorted_tables):
            engine.execute(tbl.delete())
        dbSession.remove()

    def test_noUser(self):
        """ Tests for adding a user """

        # Test if there are no user
        noUserTest = dbSession.query(User).all()
        assert len(noUserTest) == 0

    def test_addUser(self):
        # Add test data
        userTestData()

        print("Testing addUser")
        response = User.query.filter_by(id=1).all()
        assert response[0].username == 'KatUser'

    # Test getting a user
    def test_getUser(self):
        userTestData()
        response = User.query.filter_by(username='aUser').all()

        # user name isnt unique
        print("Testing getUser")
        print(len(response))
        assert len(response) == 3
        assert response[0].id != response[1].id

if __name__ == '__main__':
    unittest.main()
