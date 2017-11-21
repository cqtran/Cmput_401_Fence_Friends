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

@materialBlueprint.route('/getPriceList/', methods=['GET'])
#@login_required
#@roles_required('primary')
def getPriceList():
    """ Returns a list of prices to a company for a certain year """
    if request.method == 'GET':
        materials = dbSession.query(Material)
        #materials = materials.filter(Material.company_name == current_user.company_name).all()
        materials = materials.all()
        if len(materials) == 0:
            return bad_request('No materials and prices were found for this company')
        return jsonify(materials)

@materialBlueprint.route('/uploadPrice/', methods=['POST'])
#@login_required
#@roles_required('primary')
def uploadPrice():
    """ Parses the given csv file into fencing materials prices for a given company """
    company_name = current_user.company_name
    if request.method == 'POST':
        priceFile = request.files['prices']
        if not priceFile:
            return bad_request('Invalid price file uploaded')
        stream = io.StringIO(priceFile.stream.read().decode("UTF8"), newline=None)
        csv_input = csv.reader(stream)
        print(csv_input)
        # Clear materials list? This will cause issues for appearances due to ForeignKeys
        # dbSession.query(Material.company_name == current_user.company_name).delete()

        category = ''
        for row in csv_input:
            #TODO: Parse the csv file.
            if row[2] == 'My Price' and row[4] == 'Pieces in Bundle':
                # Category
                print(row)
                category = row[0]
            if row[0] != '' and row[2] == '' and row[4] == '':
                # Category
                print(row)
                category = row[0]
            if row[1].startswith('$') and row[2].startswith('$'):
                # Material
                print('MATERIAL: ' + row[0] + ' | ' + row[2] + ' | ' + category + ' | ' + row[5])
                material_name = row[0]
                my_price = row[2]
                note = row[5]
                # Insert data into db

                # newMaterial = Material()
                #dbSession.add(newMaterial)
            # Otherwise, ignore row
        #dbSession.commit()
        return created_request('Prices were changed')
    return bad_request('Oops')
