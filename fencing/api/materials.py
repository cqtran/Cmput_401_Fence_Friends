from sqlalchemy import *
from database.db import dbSession, init_db
from database.models import Company, Material
from flask.json import jsonify

from flask import Blueprint, request
from flask_security.core import current_user
from flask_security import login_required
from flask_security.decorators import roles_required
from api.errors import *

import json
import io
import csv

materialBlueprint = Blueprint('materialBlueprint', __name__, template_folder='templates')

@materialBlueprint.route('/getPriceList/<company_name>/', methods=['GET'])
#@login_required
#@roles_required('primary')
def getPriceList(company_name):
    """ Returns a list of prices to a company for a certain year """
    if request.method == 'GET':
        materials = dbSession.query(Material)
        # materials = materials.filter(company_name = current_user.company_name)
        materials = materials.filter(Material.company_name == company_name).all()
        if len(materials) == 0:
            return bad_request('No materials and prices were found for this company')
        return jsonify(materials)

@materialBlueprint.route('/uploadPrice/<company_name>/', methods=['POST'])
#@login_required
#@roles_required('primary')
def uploadPrice(company_name):
    """ Parses the given csv file into fencing materials prices for a given company """
    if request.method == 'POST':
        priceFile = request.files['prices']
        if not priceFile:
            return bad_request('Invalid price file uploaded')
        stream = io.StringIO(priceFile.stream.read().decode("UTF8"), newline=None)
        csv_input = csv.reader(stream)
        print(csv_input)

        for row in csv_input:
            print(row)
            #TODO: Parse the csv file

        return created_request('Prices were changed')
    return bad_request('Oops')
