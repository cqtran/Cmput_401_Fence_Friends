import os
import unittest

from flask import Flask
from database.db import dbSession, Base, init_db, engine
from database.models import Customer, Project, Company, Status
from tests.testdata import *

import api.pictures as Pictures

app = Flask(__name__)
app.config['TESTING'] = True
app.config['WTF_CSRF_ENABLED'] = False
app.config['DEBUG'] = False

class TestPicture(unittest.TestCase):
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

    def test_addPicture(self):
        """ Test adding a picture to a project """
        pass

    def test_getPictures(self):
        """ Test getting pictures of a project """
        pass
