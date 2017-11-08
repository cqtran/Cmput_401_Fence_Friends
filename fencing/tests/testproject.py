import unittest

from flask import Flask, json
from database.db import dbSession, Base, init_db, engine
from database.models import Customer, Project, Company, Status
from tests.testdata import *

import requests

import api.projects as Projects

app = Flask(__name__)
app.config['TESTING'] = True
app.config['WTF_CSRF_ENABLED'] = False
app.config['DEBUG'] = False

app.register_blueprint(Projects.projectBlueprint)

class TestProject(unittest.TestCase):
    def setUp(self):
        """ Initialize, clear, and set starting data """
        init_db()

        # Clear all tables in the database
        for tbl in reversed (Base.metadata.sorted_tables):
            engine.execute(tbl.delete())

        companyTestData()
        statusTestData()
        customerTestData()

    def tearDown(self):
        """Clear all tables"""
        for tbl in reversed (Base.metadata.sorted_tables):
            engine.execute(tbl.delete())
        dbSession.remove()

    def test_createProject(self):
        """ Test for creating a project """
        """customerTestData()

        # Test if there are no projects
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
        assert result['project_name'] == "Kat's house fence" """
        pass

    def test_savingNote(self):
        # CHANGED: This function may be deprecated
        """newCustomer = Customer(customer_id = 1, first_name = 'Kat', email = 'Kat@gmail.com', cellphone = '555-555-5555', company_name = 'Fence')
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
        assert result['note'] == 'This is a new note'"""
        pass

    def test_getProject(self):
        """ Test for getting a project of a project id """
        print("\n\n Testing getProject API\n")
        projectTestData()

        # TODO: SQLalchemy ORM autoincrements project_id but does not allow
        # setting a static project_id when adding a project unlike the
        # Customer table. This makes it difficult to test getting projects

        # Test getting project with id = 10
        response = requests.get('http://localhost:5000/getProject/10')
        json_obj = json.loads(response.text)
        print("\nGot json response from 'http://localhost:5000/getProject/10':")
        print(json_obj)

        assert len(json_obj) == 1
        result = json_obj[0]
        # Test the information contained in the object with expected information
        assert result['status_name'] == 'Complete'
        assert result['address'] == 'Park St'
        assert result['note'] == 'Concrete fence'
        assert result['project_name'] == "Jason's fence for company building"
        print("Json response is expected")

    def test_getProjectList(self):
        """ Test for getting all projects of a company """
        print("\n\n Testing getProjectList API\n")
        projectTestData()

        # Test getting projects from only customer 1
        response = requests.get('http://localhost:5000/getProjectList/1')
        json_obj = json.loads(response.text)
        print("\nGot json response from 'http://localhost:5000/getProjectList/1':")
        print(json_obj)
        assert len(json_obj) == 2
        result1 = json_obj[0]
        result2 = json_obj[1]
        # Test the information contained in the object with expected information
        assert result1['status_name'] == 'Not Reached'
        assert result1['address'] == 'Bear St'
        assert result1['note'] == 'A fun fencing project'
        assert result1['project_name'] == "Kat's house fence"

        assert result2['status_name'] == 'Not Reached'
        assert result2['address'] == 'Grand Ave'
        assert result2['note'] == 'Dog lives here'
        assert result2['project_name'] == "Kat's second house fence"

        print("Json response is expected")

    def test_updateProjectInfo(self):
        """ Test the updating of project information """
        pass
