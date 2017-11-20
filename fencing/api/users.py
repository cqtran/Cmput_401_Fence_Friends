from sqlalchemy import *
from database.db import dbSession, init_db
from database.models import User, Company
from flask.json import jsonify

from flask import Blueprint, request
from flask.json import jsonify
from flask_security.core import current_user
from flask_security import login_required
from flask_security.decorators import roles_required
from api.errors import *

userBlueprint = Blueprint('userBlueprint', __name__, template_folder='templates')

@userBlueprint.route('/getInactiveUsers/', methods=['GET'])
@login_required
@roles_required('admin')
def getInactiveUsers():
    """ Returns a list of inactive users"""
    if request.method == 'GET':
        users = dbSession.query(User).filter(User.active == False).all()
        if len(users) == 0:
            return bad_request("No inactive users were found")
        return jsonify(users)

@userBlueprint.route('/getActiveUsers/', methods=['GET'])
@login_required
@roles_required('admin')
def getActiveUsers():
    """ Returns a list of active users"""
    if request.method == 'GET':
        users = dbSession.query(User).filter(User.active == True).filter(User.id != current_user.id).all()
        if len(users) == 0:
            return bad_request("No active users were found")
        return jsonify(users)

@userBlueprint.route('/checkcompany/', methods=['POST'])
def checkcompany():
    """ Checks if company exists """
    if request.method == 'POST':
        company = request.values.get("name")
        check = len(dbSession.query(Company).filter(Company.company_name == company).all())
        if check == 0:
            return created_request("Good")

    return bad_request("Bad")

@userBlueprint.route('/checkemail/', methods=['POST'])
def checkemail():
    """ Checks if company exists """
    if request.method == 'POST':
        email = request.values.get("email")
        check = len(dbSession.query(User).filter(User.email == email).all())
        if check == 0:
            return created_request("Good")

    return bad_request("Bad")

@userBlueprint.route('/getcompany/', methods=['GET'])
@login_required
def getcompany():
    """ returns company name """
    if request.method == 'GET':
        company_name = current_user.company_name
        return jsonify(company_name)
    return bad_request("Bad")