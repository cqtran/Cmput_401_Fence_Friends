from sqlalchemy import *
from database.db import dbSession, init_db
from database.models import User
from flask.json import jsonify

from flask import Blueprint, request, redirect, url_for
from flask.json import jsonify
from flask_security.core import current_user
from flask_security import login_required
from flask_security.decorators import roles_required

#from app import userDatastore

adminBlueprint = Blueprint('adminBlueprint', __name__, template_folder='templates')
# TODO: This was moved into app.py due to it being tied to flask_security
"""
@adminBlueprint.route('/acceptUser/', methods=['POST'])
@login_required
@roles_required('admin')
def acceptUser():
    if request.method == 'POST':
        user_id = request.form["user_id"]
        print(user_id)
        user = dbSession.query(User).filter(User.id == user_id).all()
        #userDatastore.activate_user(user[0])
        user[0].active = True
        dbSession.commit()
        return redirect(url_for('accountrequests'))
    """
