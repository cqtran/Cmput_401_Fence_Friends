from sqlalchemy import *
from database.db import dbSession, init_db
from database.models import Customer, Project, Quote
from flask.json import jsonify
import json
from flask import Blueprint, request
from flask_security.core import current_user
from flask_security import login_required
from flask_security.decorators import roles_required
from api.errors import bad_request

accountingBlueprint = Blueprint('accountingBlueprint', __name__, template_folder='templates')

@accountingBlueprint.route('/getAccountingSummary/', methods=['GET'])
#@login_required
#@roles_required('primary')
def getAccountingSummary():
    """ Returns a list of accounting related calculations """
    pass

@accountingBlueprint.route('/exportAccountingSummary/', methods=['GET'])
#@login_required
#@roles_required('primary')
def exportAccountingSummary():
    """ Returns a downloadable file of the accounting summary """
    #return send_from_directory(directory=uploads, filename=filename)
    pass
