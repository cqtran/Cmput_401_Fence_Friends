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
        projectTestData()

    def tearDown(self):
        """Clear all tables"""
        for tbl in reversed (Base.metadata.sorted_tables):
            engine.execute(tbl.delete())
        dbSession.remove()

    def test_getLayouts(self):
        testLayoutData()
        response = Layout.query.filter_by(project_id=1).first()
        checks = Layouts.getLayouts(response.project_id)
        assert(len(checks) > 1)
        

    def test_removeLayouts(self):
        self.tearDown()
        self.setUp()
        testLayoutData()
        response = Layout.query.filter_by(layout_id=1).first()
        Layouts.removeLayout(response.layout_id)
        response = None
        response = Layout.query.filter_by(layout_id=1).first()
        # Response should be none
        assert(response == None)

    def test_updateLayoutName(self):
        self.tearDown()
        self.setUp()
        testLayoutData()
        response = Layout.query.filter_by(layout_id=1).first()
        Layouts.updateLayoutName(response.layout_id, "This is a test")
        response = None
        response = Layout.query.filter_by(layout_id=1).first()
        assert(response.layout_name == "This is a test")

    def test_createLayout(self):
        self.tearDown()
        self.setUp()
        testLayoutData()
        proj_id = 2
        response = Layouts.createLayout(proj_id)
        checks = Layout.query.filter_by(layout_id=response.layout_id).first()
        assert(checks.layout_id == response.layout_id)

    def test_updateLayoutInfo(self):
        self.tearDown()
        self.setUp()
        testLayoutData()
        response = Layout.query.filter_by(layout_id=1).first()
        r_id = Layouts.updateLayoutInfo(response.project_id, "New Layout", "New Info", response.layout_id)
        check = Layout.query.filter_by(layout_id=1).first()
        assert(check.layout_name == "New Layout")
        assert(check.layout_info == "New Info")



