#!/usr/bin/python
import MySQLdb

def getConnection():

    hostname = 'localhost'
    username = 'root@localhost'
    password = 'cmput401F3nc1ng'
    database = '401TEST'


    # Should be able to conenct if everything has been setup correctly
    myConnection = MySQLdb.connect( host=hostname, user=username, passwd=password, db=database )
    return myConnection