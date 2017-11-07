from sqlalchemy import *
from database.db import dbSession, init_db
from database.models import Status
from flask.json import jsonify

from flask import Blueprint, request
from flask.json import jsonify
from flask_security.core import current_user
from flask_security import login_required
from flask_security.decorators import roles_required

statusBlueprint = Blueprint('statusBlueprint', __name__, template_folder='templates')

@statusBlueprint.route('/getStatusList/', methods=['GET'])
@login_required
@roles_required('primary')
def getStatusList():
    if request.method == "GET":
        statuses = dbSession.query(Status).all()
        return jsonify(statuses)
