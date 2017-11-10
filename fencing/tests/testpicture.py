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



    def test_getPictures(self):
        """ Test getting pictures of a project """
        pictureTestData()

        Pics = Picture.query.filter_by(project_id=1).all()
        assert len(Pics) > 1
        assert Pics[0].file_name != Pics[1].file_name

    def test_picturePID(self):
        pictureTestData()

        Pics = dbSession.query(Picture).all()
        assert Pics[1].project_id != Pics[2].project_id

    # def test_getPicPID(self):
    #     pictureTestData()

    #     Pics = Pictures.getPictureList(1)
