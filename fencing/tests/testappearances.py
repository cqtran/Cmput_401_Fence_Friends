import unittest

from flask import json
from database.db import dbSession, Base, engine
from database.models import Appearance
from tests.testdata import *

import api.appearances as Appearance

import requests

class TestAppearances(unittest.TestCase):
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
        """Clear all tables"""
        for tbl in reversed (Base.metadata.sorted_tables):
            engine.execute(tbl.delete())
        dbSession.remove()

    def test_getAppearanceList(self):
        testAppearanceData()
        response = Appearance.getAppearanceList(project_id=1)
        assert(len(response) > 0)

    def test_createAppearance(self):
        Appearance.createAppearance(project_id=1)
        response = Appearance.getAppearanceList(project_id=1)
        assert response[0]['height'] == '0.01'
        assert response[0]['panel_gap'] == '0.01'

    def test_removeAppearance(self):
        response = Appearance.getAppearanceList(project_id=1)
        assert(len(response) == 0)
        Appearance.createAppearance(project_id=1)
        response = Appearance.getAppearanceList(project_id=1)
        assert(len(response) > 0)
        Appearance.removeAppearance(appearance_id = int(response[0]['appearance_id']))

    def test_updateAppearanceInfo(self):
        Appearance.createAppearance(project_id=1)
        response = Appearance.getAppearanceList(project_id=1)
        Appearance.updateAppearanceInfo(int(response[0]['project_id']), int(response[0]['appearance_id']), "Test", 0.05, 0.8)
        response = Appearance.getAppearanceList(project_id=1)
        assert response[0]['appearance_name'] == "Test"


