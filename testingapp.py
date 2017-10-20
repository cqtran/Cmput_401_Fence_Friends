import os
import unittest

from flask import Flask

app = Flask(__name__)

class TestCase(unittest.TestCase):
    
    def setUp(self):    
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:password@localhost/testingdata'
        self.app = app.test_client()
        db.create_all()        
    
    def tearDown(self):
        db.session.remove()
        db.drop_all()
    
    def test_test(self):
        test = 'test'
        assert test != 'test1'
    
if __name__ == '__main__':
    unittest.main()