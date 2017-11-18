from sqlalchemy import *
from database.db import dbSession
from database.models import Project, Appearance
from flask.json import jsonify
import json
from flask import Blueprint, request
from flask_security.core import current_user
from flask_security import login_required
from flask_security.decorators import roles_required
from api.errors import bad_request

appearanceBlueprint = Blueprint('appearanceBlueprint', __name__, template_folder='templates')

@appearanceBlueprint.route('/getAppearanceList/<int:project_id>', methods=['GET'])
#@login_required
#@roles_required('primary')
def getAppearanceList(project_id):
    """ Returns a list of appearances of a given project id """
    pass
