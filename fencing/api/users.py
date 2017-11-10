from sqlalchemy import *
from database.db import dbSession, init_db
from database.models import User
from flask.json import jsonify

from flask import Blueprint, request
from flask.json import jsonify
from flask_security.core import current_user
from flask_security import login_required
from flask_security.decorators import roles_required

userBlueprint = Blueprint('userBlueprint', __name__, template_folder='templates')

@userBlueprint.route('/getInactiveUsers/', methods=['GET'])
def getUser(customer_id):
    users = dbSession.query(User).filter(User.active == False).all()
    return jsonify(users)
