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

"""Api relating to calculations and selecting appearance items in fences includes style, height and colour"""


appearanceBlueprint = Blueprint('appearanceBlueprint', __name__, template_folder='templates')
@appearanceBlueprint.route('/saveAppearance/', methods = ['POST'])
@login_required
@roles_required('primary')
def saveAppearance():
    """For saving or updating apperance options"""
    project_id = request.args.get('proj_id')

    appearance_id = None

    if 'appearanceId' in request.json:
        appearance_id = request.json['appearanceId']

    appearance_name = request.json['name']
    style = request.json['style']
    height = request.json['height']
    border_colour = request.json['borderColor']
    panel_colour = request.json['panelColor']
    base_price = request.json['basePrice']

    appearance_id = updateAppearanceInfo(project_id, appearance_id,
        appearance_name, style, height, border_colour, panel_colour, base_price)

    if "saveSelection" in request.json:
        project = dbSession.query(Project).filter(
            Project.project_id == project_id).one()
        project.appearance_selected = appearance_id
        dbSession.commit()

    return "{" + '"appearanceId": {appearance_id}'.format(
        appearance_id=appearance_id) + "}"


@appearanceBlueprint.route('/removeAppearance/', methods = ['POST'])
@login_required
@roles_required('primary')
def removeAppearance():
    """For deleting appearance options"""
    project_id = request.args.get('proj_id')
    appearance_id = request.json['appearanceId']
    removeAppearance(appearance_id)
    return "{}"

def createAppearance(project_id):
    """Helper function for saveApperance"""
    newAppearance = Appearance(project_id = project_id,
        appearance_name = "Appearance 1", style = None, height = None, border_colour = None, panel_colour = None, base_price = 0)
    dbSession.add(newAppearance)
    dbSession.commit()
    return newAppearance

def updateAppearanceInfo(project_id, appearance_id, appearance_name, style, height, border_colour, panel_colour, base_price):
    """Helper function for saveApperance"""
    if appearance_id is None:
        appearance = createAppearance(project_id)
    else:
        appearance = dbSession.query(Appearance)
        appearance = appearance.filter(
            Appearance.appearance_id == appearance_id).one()

    appearance.appearance_name = appearance_name
    appearance.style = style
    appearance.height = height
    appearance.border_colour = border_colour
    appearance.panel_colour = panel_colour
    appearance.base_price = base_price

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
    """Helper function for removeAppearance"""
    dbSession.query(Appearance).filter(
        Appearance.appearance_id == appearance_id).delete()
    dbSession.commit()

def getAppearanceValues(appearance):
    """ Finds and Returns values related to the given appearance object """
    # Get values of selected Appearance using Contains query
    style_value = dbSession.query(Style).filter(Style.style == appearance.style).filter(Style.company_name == current_user.company_name).one().value
    height_value = dbSession.query(Height).filter(Height.height == appearance.height).filter(Height.company_name == current_user.company_name).one().value
    border_colour_value = dbSession.query(Colour).filter(Colour.colour == appearance.border_colour).filter(Colour.company_name == current_user.company_name).one().value
    panel_colour_value = dbSession.query(Colour).filter(Colour.colour == appearance.panel_colour).filter(Colour.company_name == current_user.company_name).one().value
    base_price = appearance.base_price
    # Calculate appearance multiplier for fence quotation
    appearance_value = style_value + height_value + base_price + ((border_colour_value + panel_colour_value) / 2)
    # Get value of fence removal
    removal_value = dbSession.query(Style).filter(Style.style == 'Removal').filter(Style.company_name == current_user.company_name).one().value
    # Get values of Gates
    gate_single_value = dbSession.query(Gate).filter(Gate.gate.contains('Man')).filter(Gate.company_name == current_user.company_name).one().value
    gate_double_value = dbSession.query(Gate).filter(Gate.gate.contains('RV')).filter(Gate.company_name == current_user.company_name).one().value

    return appearance_value, removal_value, gate_single_value, gate_double_value
