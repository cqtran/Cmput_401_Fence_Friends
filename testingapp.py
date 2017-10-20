import os
import unittest
 
from flask import Flask
from Python.db import dbSession, Base, init_db, fieldExists, engine
from Python.models import Customer, Project

import Python.accounts as Accounts
import Python.customers as Customers
import Python.projects as Projects

app = Flask(__name__)

class TestCase(unittest.TestCase):
    
    def setUp(self):    
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        init_db()
        for tbl in reversed (Base.metadata.sorted_tables):
            engine.execute(tble.delete())
    
    def tearDown(self):
        dbSession.remove()
    
    def test_assert(self):
        test = 'test'
        assert test != 'test1'
        
    def test_addCustomer(self):
        noCustomerTest = dbSession.query(Customer).all()
        assert len(noCustomerTest) == 0
        
        Customers.addCustomer('Kat', 'Kat@gmail.com', '555-555-5555', 'Fence')
        oneCustomerTest = dbSession.query(Customer).all()
        assert len(oneCustomerTest) == 1
        assert oneCustomerTest[0].serialize == ' '
        
    def test_createProject(self):
        noProjectTest = dbSession.query(Project).all()
        assert len(noProjectTest == 0)
        
        Projects.createProject(1, 'Not Reached', 'Somewhere Ave', 'Fence', 'A fun fencing project')
        oneProjectTest = dbSession.query(Project).all()
        assert len(oneProjectTest) == 1
        
    def test_savingNote(self):
        oneProjectTest = dbSession.query(Project).all()
        assert oneProjectTest[0].note == None
    
if __name__ == '__main__':
    unittest.main()