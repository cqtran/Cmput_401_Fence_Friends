import os
import unittest
 
from flask import Flask
	
app = Flask(__name__)

class TestCase(unittest.TestCase):
    
    def setUp(self):    
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
    
    def tearDown(self):
        pass
    
    def test_assert(self):
        test = 'test'
        assert test != 'test1'
    
if __name__ == '__main__':
    unittest.main()