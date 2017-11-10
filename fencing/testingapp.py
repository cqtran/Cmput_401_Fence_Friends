
from flask import Flask

from database.db import dbSession, init_db
from api.jsonifyObjects import MyJSONEncoder

from tests.testdata import *
import api.customers as Customers
import api.projects as Projects
import api.pictures as Pictures
import api.statuses as Statuses
#import api.errors as Errors
import argparse

app = Flask(__name__)
app.config['TESTING'] = True
app.config['WTF_CSRF_ENABLED'] = False
app.config['DEBUG'] = False

app.register_blueprint(Projects.projectBlueprint)
app.register_blueprint(Customers.customerBlueprint)
app.register_blueprint(Projects.projectBlueprint)
app.register_blueprint(Pictures.pictureBlueprint)
app.register_blueprint(Statuses.statusBlueprint)
app.register_blueprint(Errors.errorBlueprint)
app.json_encoder = MyJSONEncoder

"""
    The purpose of the testingapp is to test the endpoint APIs.

    To run the tests; run 'testingapp.py' with the command 'python testingapp.py'
    In a browser, go to http://127.0.0.1:5000/ to initialize the database
    In another terminal from the '/fencing' directory:
        - Run the command 'python -m unittest discover' to run all tests
        - Run the command 'python -m unittest tests/<testfile.py>' to run
            a specific set of tests
"""

@app.before_first_request
def setup_db():
    init_db()

@app.teardown_appcontext
def shutdown_session(exception=None):
    dbSession.remove()

@app.route('/')
def testingHomePage():
    return """
    Database has been initialized for testing 'Cavalry Fence Builder'.
    Run python -m unittest to run all tests.
    """

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = 'Run Cavalry Fence Builder')
    parser.add_argument('-debug', action = 'store_true')
    parser.add_argument('-public', action = 'store_true')
    args = parser.parse_args()

    if args.public:
        app.run(host = '0.0.0.0', debug = False)

    else:
        app.run(debug = args.debug)
