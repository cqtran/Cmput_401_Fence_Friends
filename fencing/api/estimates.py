from sqlalchemy import *
from database.db import dbSession, init_db
from database.models import Company, Style, Colour, Height, Gate
from flask.json import jsonify

from flask import Blueprint, request
from flask_security.core import current_user
from flask_security import login_required
from flask_security.decorators import roles_required
from api.errors import *
from decimal import Decimal
import json
import io
import csv

estimateBlueprint = Blueprint('estimateBlueprint', __name__, template_folder='templates')

@estimateBlueprint.route('/getStyleEsimates/', methods=['GET'])
#@login_required
#@roles_required('primary')
def getStyleEsimates():
    pass

@estimateBlueprint.route('/getColourEsimates/', methods=['GET'])
#@login_required
#@roles_required('primary')
def getColourEsimates():
    pass

@estimateBlueprint.route('/getHeightEsimates/', methods=['GET'])
#@login_required
#@roles_required('primary')
def getHeightEsimates():
    pass

@estimateBlueprint.route('/getGateEsimates/', methods=['GET'])
#@login_required
#@roles_required('primary')
def getGateEsimates():
    pass

@estimateBlueprint.route('/uploadEstimates/', methods=['POST'])
#@login_required
#@roles_required('primary')
def uploadEstimates():
    pass
