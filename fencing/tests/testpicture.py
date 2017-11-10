import os
import unittest

from flask import json
from database.db import dbSession, Base, engine
from database.models import Status, Picture
from tests.testdata import *

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
        pictureTestData()

        Pic = dbSession.query(Picture).first()
        assert Pic.picture_id == 1
        assert Pic.file_name == "file"



    def test_getPictureList(self):
        """ Test getting all pictures of a project """
        print("\n\n Testing getPictureList API\n")
        pictureTestData()

        # Test getting pictures from project id = 1.
        response = requests.get('http://localhost:5000/getPictureList/1')
        json_obj = json.loads(response.text)
        print("\nGot json response from 'http://localhost:5000/getPictureList/1':")
        print(json_obj)

        assert len(json_obj) == 2
        result1 = json_obj[0]
        result2 = json_obj[1]
        # Test the information contained in the object with expected information
        assert result1['picture_id'] == 1
        assert result1['file_name'] == 'file'

        assert result2['picture_id'] == 2
        assert result2['file_name'] == 'file1'
        print("Json response is expected")

    def test_picturePID(self):
        pictureTestData()

        Pics = dbSession.query(Picture).all()
        assert Pics[1].project_id != Pics[2].project_id

    # def test_getPicPID(self):
    #     pictureTestData()

    #     Pics = Pictures.getPictureList(1)
