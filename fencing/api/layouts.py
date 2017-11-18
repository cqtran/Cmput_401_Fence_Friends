from sqlalchemy import *
from database.db import dbSession
from database.models import Project, Layout, Appearance
from flask.json import jsonify
import json
from flask import Blueprint, request
from flask_security.core import current_user
from flask_security import login_required
from flask_security.decorators import roles_required
from api.errors import bad_request

layoutBlueprint = Blueprint('layoutBlueprint', __name__, template_folder='templates')

@layoutBlueprint.route('/getLayoutList/<int:project_id>', methods=['GET'])
#@login_required
#@roles_required('primary')
def getLayoutList(project_id):
    """ Returns a list of layouts of a given project id """
    pass

@layoutBlueprint.route('/getLayout/<int:layout_id>', methods=['GET'])
#@login_required
#@roles_required('primary')
def getLayout(layout_id):
	""" Returns a layout of the given layout id """
	pass

@layoutBlueprint.route('/updateLayout/<int:layout_id>', methods=['pass'])
#@login_required
#@roles_required('primary')
def updateLayout(layout_id):
	""" Returns a layout of the given layout id """
	pass

def getLayoutHelper(project_id):
#TODO: function should be renamed in the future for clarity purposes
	layouts = dbSession.query(Layout).filter(Layout.project_id == project_id).all()
	json_response = [i.serialize for i in layouts]
	return json_response

def updateLayoutInfo(layout_id, layout_info):
    # ERIC PLEASE HELP
    #TODO: function should be renamed in the future for clarity purposes
    layout = dbSession.query(Layout)
    layout = layout.filter(Layout.layout_id == layout_id).all()
    layout[0].layout_info = layout_info
    dbSession.commit()
    return True
