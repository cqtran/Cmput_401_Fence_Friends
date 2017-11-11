import unittest

from flask import json
from database.db import dbSession, Base, engine
from database.models import Project
from tests.testdata import *

import requests

import api.projects as Projects

class TestProject(unittest.TestCase):
    def setUp(self):
        """ Initialize, clear, and set starting data """

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

        # Test getting project with id = 3
        response = requests.get('http://localhost:5000/getProject/3')
        json_obj = json.loads(response.text)
        print("\nGot json response from 'http://localhost:5000/getProject/3':")
        print(json_obj)

        assert len(json_obj) == 1
        result = json_obj[0]
        # Test the information contained in the object with expected information
        assert result['status_name'] == 'Complete'
        assert result['address'] == 'Park St'
        assert result['note'] == 'Concrete fence'
        assert result['project_name'] == "Jason's fence for company building"
        print("Json response is expected")

    def test_getInvalidProject(self):
        """ Test for getting a project of a non-exsitng project id """
        print("\n\n Testing getProject API for non-existing project\n")
        projectTestData()
        
        # Test getting non-existing project with id = 100.
        response = requests.get('http://localhost:5000/getProject/100')
        assert response.status_code == 400
        json_obj = json.loads(response.text)
        print("\nGot json response from 'http://localhost:5000/getProject/100':")
        print(json_obj)
        assert json_obj['message'] == "The project was not found"
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

    def test_getInvalidProjectList(self):
        """ Test for getting all project of a non-existing customer """
        print("\n\n Testing getCustomerList API for non-existing customer \n")
        projectTestData()

        # Test getting projects from a non-existing customer
        response = requests.get('http://localhost:5000/getProjectList/100')
        assert response.status_code == 400
        json_obj = json.loads(response.text)
        print("\nGot json response from 'http://localhost:5000/getProjectList/100':")
        print(json_obj)
        assert json_obj['message'] == "No projects were found"
        print("Json response is expected")

    def test_updateProjectInfo(self):
        """ Test the updating of project information """
        pass
