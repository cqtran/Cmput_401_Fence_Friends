from sqlalchemy import *
from database.db import dbSession, init_db
from database.models import Company, Style, Colour, Height, Gate
from flask.json import jsonify

from flask import Blueprint, request
from flask_security.core import current_user
from flask_security import login_required
from flask_security.decorators import roles_required
from api.errors import *
from decimal import Decimal
import json
import io
import csv

"""Api relating to estimation of quotes for fence. Deals with Styles, Colour, Height and Gate"""


estimateBlueprint = Blueprint('estimateBlueprint', __name__, template_folder='templates')

"""Helper functions"""
def getStyles():
    return dbSession.query(Style).filter(
        Style.company_name == current_user.company_name).all()

def getColours():
    return dbSession.query(Colour).filter(
        Colour.company_name == current_user.company_name).all()

def getHeights():
    return dbSession.query(Height).filter(
        Height.company_name == current_user.company_name).all()

@estimateBlueprint.route('/getStyleEstimates/', methods=['GET'])
@login_required
@roles_required('primary')
def getStyleEstimates():
    """ Returns a list of Styles for the current_user's company """
    if request.method == 'GET':
        styles = getStyles()
        if len(styles) == 0:
            return bad_request('No style estimate values were found')
        return jsonify(styles)

@estimateBlueprint.route('/getColourEstimates/', methods=['GET'])
@login_required
@roles_required('primary')
def getColourEstimates():
    """ Returns a list of colours for the current_user's company """
    if request.method == 'GET':
        colours = getColours()
        if len(colours) == 0:
            return bad_request('No colour estimate values were found')
        return jsonify(colours)

@estimateBlueprint.route('/getHeightEstimates/', methods=['GET'])
@login_required
@roles_required('primary')
def getHeightEstimates():
    """ Returns a list of fence heights for the current_user's company """
    if request.method == 'GET':
        heights = getHeights()
        if len(heights) == 0:
            return bad_request('No height estimate values were found')
        return jsonify(heights)

@estimateBlueprint.route('/getGateEstimates/', methods=['GET'])
@login_required
@roles_required('primary')
def getGateEstimates():
    """ Returns a list of gate estimates for the current_user's company """
    if request.method == 'GET':
        gates = dbSession.query(Gate)
        gates = gates.filter(Gate.company_name == current_user.company_name).all()
        if len(gates) == 0:
            return bad_request('No gate estimate values were found')
        return jsonify(gates)

@estimateBlueprint.route('/uploadEstimates/', methods=['POST'])
@login_required
@roles_required('primary')
def uploadEstimates():
    """ Parses the given csv file into estimate values """
    company_name = current_user.company_name
    if request.method == 'POST':
        estimateFile = request.files['estimates']
        if not estimateFile:
            return bad_request('Invalid estimate values file uploaded')
        stream = io.StringIO(estimateFile.stream.read().decode("UTF8"), newline=None)
        csv_input = csv.reader(stream)
        # Clear materials list? This will cause issues for appearances due to ForeignKeys
        dbSession.query(Style).filter(Style.company_name == current_user.company_name).delete()
        dbSession.query(Colour).filter(Colour.company_name == current_user.company_name).delete()
        dbSession.query(Height).filter(Height.company_name == current_user.company_name).delete()
        dbSession.query(Gate).filter(Gate.company_name == current_user.company_name).delete()

        category = ''
        for row in csv_input:
            #TODO: Parse the csv file
            # Change the category in which the data is saved into
            if row[0] == 'Style':
                category = 'Style'
            elif row[0] == 'Colours' or row[0] == 'Colour':
                category = 'Colour'
            elif row[0] == 'Height':
                category = 'Height'
            elif row[0] == 'Gate':
                category = 'Gate'
            elif row[0] != '' and category != '':
                name = row[0]
                try:
                    value = row[1]
                except:
                    value = 0
                insertEstimateValue(category, name, value, company_name)
            else:
                print('Empty row found')
        dbSession.commit()
        return created_request('Estimate values were updated')
    return bad_request('Request is not a POST request')

def insertEstimateValue(category, name, value, company_name):
    """Inserts estimate information based on category"""
    if category == 'Style':
        newStyle = Style(style = name, value = value, company_name = company_name)
        dbSession.add(newStyle)
    elif category == 'Colour':
        newColour = Colour(colour = name, value = value, company_name = company_name)
        dbSession.add(newColour)
    elif category == 'Height':
        newHeight = Height(height = name, value = value, company_name = company_name)
        dbSession.add(newHeight)
    elif category == 'Gate':
        newGate = Gate(gate = name, value = value, company_name = company_name)
        dbSession.add(newGate)
    else:
        print('Category not found, no data inserted')
    return
