import unittest

from flask import json
from database.db import dbSession, Base, engine
from database.models import Project, Layout
from tests.testdata import *

import requests

import api.layouts as Layouts

class TestLayout(unittest.TestCase): 
    def setUp(self):
        """ Initialize, clear, and set starting data """

        # Clear all tables in the database
        for tbl in reversed (Base.metadata.sorted_tables):
            engine.execute(tbl.delete())

        companyTestData()
        statusTestData()
        customerTestData()
        projecTestData()

    def tearDown(self):
        """Clear all tables"""
        for tbl in reversed (Base.metadata.sorted_tables):
            engine.execute(tbl.delete())
        dbSession.remove()
