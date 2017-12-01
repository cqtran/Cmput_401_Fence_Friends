import unittest

from flask import json
from database.db import dbSession, Base, engine
from database.models import Materials
from tests.testdata import *

import requests

import api.materials as Materials

class TestMaterials(unittest.TestCase):
	def setUp(self):
        """ Initialize, clear, and set starting data """

        # Clear all tables in the database
        for tbl in reversed (Base.metadata.sorted_tables):
            engine.execute(tbl.delete())
        companyTestData()