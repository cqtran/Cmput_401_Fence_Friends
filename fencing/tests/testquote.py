import unittest

from flask import json
from database.db import dbSession, Base, engine
from database.models import Quote
from tests.testdata import *

import requests

class TestQuote(unittest.TestCase):
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

    def test_noQuote(self):
        """ Tests for adding a user """

        # Test if there are no user
        noQuote = dbSession.query(Quote).all()
        assert len(noQuote) == 0

    def test_addQuote(self):
        # Add test data
        quoteTestData()

        print("Testing Quote")
        response = Quote.query.filter_by(quote_id=1).first()
        assert response.quote == 1500

    # Test getting a user 
    def test_getQuote(self):
        quoteTestData()
        response = Quote.query.filter_by(project_id=1).all()

        # user name isnt unique
        print(len(response))
        assert len(response) > 1
        assert response[0].quote != response[1].quote

    # Test note
    def test_quoteNote(self):
        quoteTestData()
        response = dbSession.query(Quote).all()
        assert len(response) > 1
        assert response[0].note != response[1].note
        assert response[0].note == response[2].note

    # Test project_id
    def test_quotePID(self):
        quoteTestData()
        response = dbSession.query(Quote).all()
        assert len(response) > 1
        assert response[0].project_id == response[1].project_id
        assert response[1].project_id != response[2].project_id

if __name__ == '__main__':
    unittest.main()
