import unittest

from flask import json
from database.db import dbSession, Base, engine
from database.models import Style, Colour, Height, Gate
from tests.testdata import *

import requests

import api.estimates as Estimate

class TestEstimate(unittest.TestCase):
    def setUp(self):
        for tbl in reversed (Base.metadata.sorted_tables):
            engine.execute(tbl.delete())
        companyTestData()
        testEstimateData()

    def tearDown(self):
        for tbl in reversed (Base.metadata.sorted_tables):
            engine.execute(tbl.delete())


    def test_positiveValues(self):
        self.tearDown()
        self.setUp()
        response = Style.query.filter_by(style_id = 1).first()
        assert(response.value > 20)
