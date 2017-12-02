from sqlalchemy import *
from database.db import dbSession, init_db
from database.models import Status
from flask.json import jsonify

from flask import Blueprint, request
from flask.json import jsonify
from flask_security.core import current_user
from flask_security import login_required
from flask_security.decorators import roles_required
from api.errors import bad_request

"""Api relating to the multiple statuses a project can hold"""

statusBlueprint = Blueprint('statusBlueprint', __name__, template_folder='templates')

@statusBlueprint.route('/getStatusList/', methods=['GET'])
@login_required
@roles_required('primary')
def getStatusList():
    """ Returns the list of statuses """
    if request.method == "GET":
        statuses = dbSession.query(Status).all()
        if len(statuses) == 0:
            return bad_request("No statuses were found")
        return jsonify(statuses)
