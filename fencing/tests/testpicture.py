import os
import unittest

from flask import json
from database.db import dbSession, Base, engine
from database.models import Status, Picture
from tests.testdata import *
from io import StringIO
import requests

import api.pictures as Pictures

class TestPicture(unittest.TestCase):
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

    def test_noPicture(self):
        print("Testing Picture")
        noPic = dbSession.query(Picture).all()
        assert len(noPic) == 0


    def test_addPicture(self):
        """ Test adding a picture to a project """
        print("\n\n Testing uploadPicture API\n")
        image = open('tests/testimage.jpg','rb')
        files = {'picture': image}

        #r = requests.post(url, files=files, data=values)

        response = requests.post('http://localhost:5000/uploadPicture/', files = files, data={'proj_id': 2})
        assert response.status_code == 200
        json_obj = json.loads(response.text)
        print("\nGot json response from 'http://localhost:5000/uploadPicture/':")

        print(json_obj)
        assert json_obj['message'] == "Picture was uploaded"
        print("Json response is expected")

        image.close()

    def test_addInvalidPicture(self):
        """ Test adding an invalid picture to a project """
        print("\n\n Testing uploadPicture API with invalid project id\n")
        image = open('tests/testimage.jpg','rb')
        files = {'picture': image}

        #r = requests.post(url, files=files, data=values)

        response = requests.post('http://localhost:5000/uploadPicture/', files = files, data={'proj_id': 100})
        assert response.status_code == 400
        json_obj = json.loads(response.text)
        print("\nGot json response from 'http://localhost:5000/uploadPicture/':")

        print(json_obj)
        assert json_obj['message'] == "Invalid project id or an error when saving the file has occured"
        print("Json response is expected")

        image.close()

    def test_getPictureList(self):
        """ Test getting all pictures of a project """
        print("\n\n Testing getPictureList API\n")
        pictureTestData()

        # Test getting pictures from project id = 1.
        response = requests.get('http://localhost:5000/getPictureList/1')
        assert response.status_code == 200
        json_obj = json.loads(response.text)
        print("\nGot json response from 'http://localhost:5000/getPictureList/1':")
        print(json_obj)

        assert len(json_obj) == 2
        result1 = json_obj[0]
        result2 = json_obj[1]
        # Test the information contained in the object with expected information
        assert result1['picture_id'] == 1
        assert result1['file_name'] == 'garden.jpg'
        assert result1['thumbnail_name'] == 'thumbnail_garden.png'

        assert result2['picture_id'] == 2
        assert result2['file_name'] == 'corner.jpg'
        assert result2['thumbnail_name'] == 'thumbnail_corner.png'
        print("Json response is expected")

    def test_getInvalidPictureList(self):
        """ Test getting all pictures of a project that has no pictures """
        print("\n\n Testing getPictureList API with a project that has no pictures\n")
        response = requests.get('http://localhost:5000/getPictureList/100')
        assert response.status_code == 400
        json_obj = json.loads(response.text)
        print("\nGot json response from 'http://localhost:5000/getPictureList/100':")
        print(json_obj)
        assert json_obj['message'] == "No pictures were found for this project"
        print("Json response is expected")

    def test_picturePID(self):
        pictureTestData()

        Pics = dbSession.query(Picture).all()
        assert Pics[1].project_id != Pics[2].project_id

    # def test_getPicPID(self):
    #     pictureTestData()

    #     Pics = Pictures.getPictureList(1)
