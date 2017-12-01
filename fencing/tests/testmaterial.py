import unittest

from flask import json
from database.db import dbSession, Base, engine
from database.models import Material
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

    def tearDown(self):
        for tbl in reversed (Base.metadata.sorted_tables):
            engine.execute(tbl.delete())

    def test_getPriceList(self):
        self.setUp()
        testMaterialData()
        response = Material.query.all()
        for resp in response:
            assert(resp.my_price > 0)

    def test_getPieceBundle(self):
        self.tearDown()
        self.setUp()
        testMaterialData()
        response = Material.query.filter_by(material_id = 1).first()
        assert(response.pieces_in_bundle > 50)

