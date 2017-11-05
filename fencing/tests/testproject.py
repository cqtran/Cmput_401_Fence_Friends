import unittest

from flask import Flask
from database.db import dbSession, Base, init_db, engine
from database.models import Customer, Project, Company, Status
from tests.testdata import *

import api.projects as Projects

app = Flask(__name__)
app.config['TESTING'] = True
app.config['WTF_CSRF_ENABLED'] = False
app.config['DEBUG'] = False

class TestProject(unittest.TestCase):
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

    def test_createProject(self):
        """ Test for creating a project """
        customerTestData()

        # Test if there are to projects
        noProjectTest = dbSession.query(Project).all()
        assert len(noProjectTest)  == 0

        # Try adding a project through Project api
        Projects.createProject(1, 'Not Reached', 'Somewhere Ave', 'Fence', "Kat's house fence")
        oneProjectTest = dbSession.query(Project).all()

        # Test if the project is successfully added
        assert len(oneProjectTest) == 1

        # Test the information from the found project
        result = oneProjectTest[0].serialize
        assert result['status_name'] == 'Not Reached'
        assert result['address'] == 'Somewhere Ave'
        assert result['project_name'] == "Kat's house fence"

    def test_savingNote(self):
        # CHANGED: This function may be deprecated
        newCustomer = Customer(customer_id = 1, first_name = 'Kat', email = 'Kat@gmail.com', cellphone = '555-555-5555', company_name = 'Fence')
        dbSession.add(newCustomer)
        dbSession.commit()

        Projects.createProject(1, 'Not Reached', 'Somewhere Ave', 'Fence', 'A fun fencing project')
        oneProjectTest = dbSession.query(Project).all()
        result = oneProjectTest[0].serialize

        # Test if the note is empty
        assert result['note'] == ''

        Projects.savenote('This is a new note', oneProjectTest[0].project_id)
        oneProjectTest = dbSession.query(Project).all()

        # Test if the not has changed
        result = oneProjectTest[0].serialize
        assert result['note'] == 'This is a new note'

    def test_getProject(self):
        """ Test for getting a project of a project id """
        pass

    def test_getCompanyProjects(self):
        """ Test for getting all projects of a company """
        pass

    def test_updateProjectInfo(self):
        """ Test the updating of project information """
        pass
