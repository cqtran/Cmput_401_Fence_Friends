from sqlalchemy import *
from database.db import dbSession, init_db
from database.models import Company, Material, Appearance
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

materialBlueprint = Blueprint('materialBlueprint', __name__, template_folder='templates')

@materialBlueprint.route('/getPriceList/', methods=['GET'])

def getPriceList():
    """ Returns a list of prices to a company for a certain year """
    if request.method == 'GET':
        materials = dbSession.query(Material)
        materials = materials.filter(Material.company_name == current_user.company_name).all()
        if len(materials) == 0:
            return bad_request('No materials and prices were found for this company')
        return jsonify(materials)

@materialBlueprint.route('/uploadPrice/', methods=['POST'])

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
        dbSession.query(Material).filter(Material.company_name == current_user.company_name).delete()

        category = ''
        for row in csv_input:
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
                try:
                    my_price = Decimal(row[2][1:])
                except:
                    print('My Price value could not be converted into a Decimal, default to 0')
                    my_price = 0

                try:
                    pieces_in_bundle = Decimal(row[4])
                except:
                    print('Pieces in bundle value could not be converted into a number, default to 1')
                    pieces_in_bundle = 1
                material_name = row[0]
                note = row[5]
                # Insert data into db

                newMaterial = Material(material_name = material_name, my_price = my_price, pieces_in_bundle = pieces_in_bundle, category = category, note = note, company_name = current_user.company_name)
                dbSession.add(newMaterial)
            # Otherwise, ignore row
        dbSession.commit()
        return created_request('Prices were changed')
    return bad_request('Request is not a POST request')

@materialBlueprint.route('/getMaterialLists/', methods=['GET'])
@login_required
@roles_required('primary')
def getMaterialLists():
    if request.method == 'GET':
        appearance_id = request.args.get('appearance_id')
        appearance = dbSession.query(Appearance).filter(Appearance.appearance_id == appearance_id).one()
        if appearance is None:
            return bad_request('Appearance does not exist')
        return jsonify(getMaterialList(appearance))
    return bad_request('Request is not a POST request')

def getMaterialList(appearance):
    materials = dbSession.query(Material).filter(Material.company_name == current_user.company_name)

    # Filtering for specific materials from the database depending
    # on what appearance values the user has selected
    # Specific rules and formulas provided by the client
    if appearance.height == '6':
        post_height = '6.5'
        panel_height = '62.25'
        u_channel_height = '5'

    if appearance.height == '5':
        post_height = '5.5'
        panel_height = '50.25'
        u_channel_height = '4'

    if appearance.height == '4':
        post_height = '5.5'
        panel_height = '50.25'
        u_channel_height = '3'

    if appearance.height =='3':
        post_height = '6.5'
        panel_height = '62.25'
        u_channel_height = '5'

    metal_materials = materials.filter(Material.category.contains('Metal'))
    metal_post = metal_materials.filter(Material.material_name.contains('Steel Post')).all()
    metal_u_channel = metal_materials.filter(Material.material_name.contains('Rail Insert Rail')).all()
    metal_lsteel = metal_materials.filter(Material.material_name.contains('Metal Gate Insert')).all()

    plastic_post_materials = materials.filter(Material.category.contains('Post Profiles'))
    plastic_t_post = plastic_post_materials.filter(Material.material_name.contains(appearance.border_colour)).filter(Material.material_name.contains(post_height)).all()
    plastic_corner_post = plastic_post_materials.filter(Material.material_name.contains(appearance.border_colour)).filter(Material.material_name.contains(post_height)).all()
    plastic_line_post = plastic_post_materials.filter(Material.material_name.contains(appearance.border_colour)).filter(Material.material_name.contains(post_height)).all()
    plastic_end_post = plastic_post_materials.filter(Material.material_name.contains(appearance.border_colour)).filter(Material.material_name.contains(post_height)).all()
    plastic_gate_post = plastic_post_materials.filter(Material.material_name.contains(appearance.border_colour)).filter(Material.material_name.contains(post_height)).all()

    plastic_rail = materials.filter(Material.category.contains('Privacy Fence Rails')).filter(Material.material_name.contains(appearance.border_colour)).filter(Material.material_name.contains('93.75')).all()
    plastic_u_channel = materials.filter(Material.category.contains('U-Channel (Plastic)')).filter(Material.material_name.contains(appearance.border_colour)).filter(Material.material_name.contains(u_channel_height)).all()
    plastic_panel = materials.filter(Material.category.contains('T&G')).filter(Material.material_name.contains(appearance.panel_colour)).filter(Material.material_name.contains(panel_height)).all()
    plastic_collar = materials.filter(Material.category.contains('Collars')).all()
    plastic_cap = materials.filter(Material.category.contains('Caps')).filter(Material.material_name.contains(appearance.border_colour)).filter(Material.material_name.contains('Cap')).all()

    gate_hardware = materials.filter(Material.category.contains('Gate Hardware'))
    gate_hinge = gate_hardware.filter(Material.material_name.contains('Hinge')).all()
    gate_latch = gate_hardware.filter(Material.material_name.contains('Latch')).all()

    return {
        'metal_post'            : metal_post,
        'metal_u_channel'       : metal_u_channel,
        'metal_lsteel'          : metal_lsteel,
        'plastic_t_post'        : plastic_t_post,
        'plastic_corner_post'   : plastic_corner_post,
        'plastic_line_post'     : plastic_line_post,
        'plastic_end_post'      : plastic_end_post,
        'plastic_gate_post'     : plastic_gate_post,
        'plastic_rail'          : plastic_rail,
        'plastic_u_channel'     : plastic_u_channel,
        'plastic_panel'         : plastic_panel,
        'plastic_collar'        : plastic_collar,
        'plastic_cap'           : plastic_cap,
        'gate_hinge'            : gate_hinge,
        'gate_latch'            : gate_latch
        }
