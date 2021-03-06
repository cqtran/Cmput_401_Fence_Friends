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

    def test_calculateEstimate(self):
        self.tearDown()
        self.setUp()
        Estimate.calculateEstimate()


    def test_positiveEstimate(self):
        self.tearDown()
        self.setUp()
        value = 0
        styles = Style.query.filter_by(style_id = 1).first()
        colors = Colour.query.filter_by(colour_id = 1).first()
        heights = Height.query.filter_by(height_id = 1).first()
        gates = Gate.query.filter_by(gate_id = 1).first()
        assert(styles.value >= value)
        assert(colors.value >= value)
        assert(heights.value >= value)
        assert(gates.value >= value)

    def test_negativeEstimate(self):
        self.tearDown()
        self.setUp()
        value = 0
        heights3 = Height.query.filter_by(height_id = 3).first()
        heights4 = Height.query.filter_by(height_id = 4).first()

        assert(heights3.value < value)
        assert(heights4.value < value)

    def test_getStyleEstimate(self):
        self.tearDown()
        self.setUp()
        response = Style.query.filter_by(style_id=1).first()
        response2 = Style.query.filter_by(style_id=2).first()
        assert(response.value != response2.value)
        assert(response.value > 0)

    def test_getGateEstimate(self):
        self.tearDown()
        self.setUp()
        response = Gate.query.filter_by(gate_id=1).first()
        response2 = Gate.query.filter_by(gate_id=2).first()
        assert(response.value != response2.value)
        assert(response.value > 0)

    def test_getHeightEstimate(self):
        self.tearDown()
        self.setUp()
        response = Height.query.filter_by(height_id=1).first()
        response2 = Height.query.filter_by(height_id=2).first()
        assert(response.height != response2.height)

    def test_getColourEstimate(self):
        self.tearDown()
        self.setUp()
        response = Colour.query.filter_by(colour_id=1).first()
        response2 = Colour.query.filter_by(colour_id=2).first()
        assert(response.colour != response2.colour)


