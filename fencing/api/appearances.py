from sqlalchemy import *
from database.db import dbSession
from database.models import Project, Appearance, Style, Height, Colour, Gate
from flask.json import jsonify
import json
from flask import Blueprint, request
from flask_security.core import current_user
from flask_security import login_required
from flask_security.decorators import roles_required
from api.errors import bad_request

appearanceBlueprint = Blueprint('appearanceBlueprint', __name__, template_folder='templates')

@appearanceBlueprint.route('/saveAppearance/', methods = ['POST'])

def saveAppearance():
    project_id = request.args.get('proj_id')

    appearance_id = None

    if 'appearanceId' in request.json:
        appearance_id = request.json['appearanceId']
    
    appearance_name = request.json['name']
    panelGap = request.json['panelGap']
    fenceHeight = request.json['fenceHeight']

    appearance_id = updateAppearanceInfo(project_id, appearance_id,
        appearance_name, panelGap, fenceHeight)
    
    if "saveSelection" in request.json:
        project = dbSession.query(Project).filter(
            Project.project_id == project_id).one()
        project.appearance_selected = appearance_id
        dbSession.commit()

    return "{" + '"appearanceId": {appearance_id}'.format(
        appearance_id=appearance_id) + "}"


@appearanceBlueprint.route('/removeAppearance/', methods = ['POST'])

def removeAppearance():
    project_id = request.args.get('proj_id')
    appearance_id = request.json['appearanceId']
    removeAppearance(appearance_id)
    return "{}"

def createAppearance(project_id):
    newAppearance = Appearance(project_id = project_id,
        appearance_name = "Appearance 1", panel_gap = "0.01", height = "0.01")
    dbSession.add(newAppearance)
    dbSession.commit()
    return newAppearance

def updateAppearanceInfo(project_id, appearance_id, appearance_name, panelGap,
    fenceHeight):

    if appearance_id is None:
        appearance = createAppearance(project_id)
    else:
        appearance = dbSession.query(Appearance)
        appearance = appearance.filter(
            Appearance.appearance_id == appearance_id).one()

    appearance.appearance_name = appearance_name
    appearance.panel_gap = panelGap
    appearance.height = fenceHeight
    dbSession.commit()
    appearance_id = appearance.appearance_id
    return appearance_id

def getAppearanceList(project_id):
    """ Returns a list of appearances of a given project id """
    appearances = dbSession.query(Appearance).filter(
        Appearance.project_id == project_id).all()
    json_response = [i.serialize for i in appearances]
    return json_response

def removeAppearance(appearance_id):
    dbSession.query(Appearance).filter(
        Appearance.appearance_id == appearance_id).delete()
    dbSession.commit()

def getAppearanceValues(appearance):
    """ Finds and Returns values related to the given appearance object """
    # Get values of selected Appearance using Contains query
    style_value = dbSession.query(Style).filter(Style.style.contains(appearance.style)).filter(Style.company_name == current_user.company_name).one().value
    height_value = dbSession.query(Height).filter(Height.height.contains(appearance.height)).filter(Height.company_name == current_user.company_name).one().value
    border_colour_value = dbSession.query(Colour).filter(Colour.colour.contains(appearance.border_colour)).filter(Colour.company_name == current_user.company_name).one().value
    panel_colour_value = dbSession.query(Colour).filter(Colour.colour.contains(appearance.panel_colour)).filter(Colour.company_name == current_user.company_name).one().value
    base_price = appearance.base_price
    # Calculate appearance multiplier for fence quotation
    appearance_value = style_value + height_value + base_price + ((border_colour_value + panel_colour_value) / 2)
    # Get value of fence removal
    removal_value = dbSession.query(Style).filter(Style.style.contains('Removal')).filter(Style.company_name == current_user.company_name).one().value
    # Get values of Gates
    gate_single_value = dbSession.query(Gate).filter(Gate.gate.contains('Man')).filter(Gate.company_name == current_user.company_name).one().value
    gate_double_value = dbSession.query(Gate).filter(Gate.gate.contains('RV')).filter(Gate.company_name == current_user.company_name).one().value

    return appearance_value, removal_value, gate_single_value, gate_double_value
