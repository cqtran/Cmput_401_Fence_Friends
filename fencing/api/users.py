from sqlalchemy import *
from database.db import dbSession, init_db
from database.models import User
from flask.json import jsonify

from flask import Blueprint, request
from flask.json import jsonify
from flask_security.core import current_user
from flask_security import login_required
from flask_security.decorators import roles_required
from api.errors import bad_request

userBlueprint = Blueprint('userBlueprint', __name__, template_folder='templates')

@userBlueprint.route('/getInactiveUsers/', methods=['GET'])
def getInactiveUsers():
    """ Returns a list of inactive users"""
    if request.method == 'GET':
        users = dbSession.query(User).filter(User.active == False).all()
        if len(users) == 0:
            return bad_request("No inactive users were found")
        return jsonify(users)

@userBlueprint.route('/getActiveUsers/', methods=['GET'])
def getActiveUsers():
    """ Returns a list of active users"""
    if request.method == 'GET':
        users = dbSession.query(User).filter(User.active == True).all()
        if len(users) == 0:
            return bad_request("No active users were found")
        return jsonify(users)
