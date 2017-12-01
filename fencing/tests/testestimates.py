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

        getEstimateData()

    def tearDown(self)
        for tbl in reversed (Base.metadata.sorted_tables):
            engine.execute(tbl.delete())