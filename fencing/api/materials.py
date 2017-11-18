from sqlalchemy import *
from database.db import dbSession, init_db
from database.models import Material
from flask.json import jsonify

import json

from flask import Blueprint, request
from flask_security.core import current_user
from flask_security import login_required
from flask_security.decorators import roles_required
from api.errors import *

materialBlueprint = Blueprint('materialBlueprint', __name__, template_folder='templates')

@materialBlueprint.route('/getPriceList/<company_name>/', methods=['GET'])
#@login_required
#@roles_required('primary')
def getPriceList(company_name):
    """ Returns a list of prices to a company for a certain year """
    pass
