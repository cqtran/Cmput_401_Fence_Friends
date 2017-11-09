import os
import unittest

from flask import json
from database.db import dbSession, Base, engine
from database.models import Status
from tests.testdata import *

import requests

import api.pictures as Pictures

class TestPicture(unittest.TestCase):
    def setUp(self):
        """ Initialize, clear, and set starting data """

        # Clear all tables in the database
        for tbl in reversed (Base.metadata.sorted_tables):
            engine.execute(tbl.delete())
        companyTestData()
        statusTestData()
        customerTestData()
        projectTestData()

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