from sqlalchemy import *
from database.db import dbSession, init_db
from database.models import Project, Quote, Layout, Appearance
from database.models import Style, Colour, Height, Gate
from flask.json import jsonify

from flask import Blueprint, request
from flask_security.core import current_user
from flask_security import login_required
from flask_security.decorators import roles_required
from api.errors import *
from decimal import Decimal
from diagram.DiagramParser import DiagramParser
from priceCalculation.QuoteCalculation import QuoteCalculation
from priceCalculation.MaterialListCalculation import MaterialListCalculation
import priceCalculation.priceCalculation as PriceCalculation

import api.appearances as Appearances
import api.layouts as Layouts
import math

quoteBlueprint = Blueprint('quoteBlueprint', __name__, template_folder='templates')

@quoteBlueprint.route('/finalizeQuote/', methods=['POST'])
@login_required
@roles_required('primary')
def finalizeQuote():
    if request.method == 'POST':
        """
        Given a project ID and a boolean finalize.
        Turn finalize to false if finalize is False.
        Generate and save the quote and material expenses if finalize is True

        Customer quote is calculated for each fence by the following formula.
        quote = length * (style + height + base price + (border colour + panel colour) / 2)
        """

        project_id = request.args.get('proj_id')
        material_types = request.json['material_types']
        material_amounts = request.json['material_amounts']

        project = dbSession.query(Project).filter(Project.project_id == project_id).one()
        if project is None:
            print('Project does not exist')
            return bad_request('Project does not exist')

        if project.finalize:
            print('Finalize set to false')
            return bad_request('Project has already been finalized')

        project.finalize = True

        try:
            subtotal, gst, total = calculateQuote(project)
            calculateExpense(material_types, material_amounts)
        except:
            print('Error in saving the quote')
            return bad_request('Error in saving the quote')

        dbSession.commit()
        print('Quote has been generated and finalized')
        return created_request('Quote has been generated')
    print('Request is not a POST request')
    return bad_request('Request is not a POST request')

def calculateExpense(material_types, material_amounts):
    subtotal = 0
    subtotal += math.ceil(material_amounts['metalpost'] / material_types['metal_post']['pieces_in_bundle']) * material_types['metal_post']['my_price']
    subtotal += math.ceil(material_amounts['metal_u_channel'] / material_types['metal_u_channel']['pieces_in_bundle']) * material_types['metal_u_channel']['my_price']
    subtotal += math.ceil(material_amounts['metal_lsteel'] / material_types['metal_lsteel']['pieces_in_bundle']) * material_types['metal_lsteel']['my_price']
    subtotal += math.ceil(material_amounts['plastic_t_post'] / material_types['plastic_t_post']['pieces_in_bundle']) * material_types['plastic_t_post']['my_price']
    subtotal += math.ceil(material_amounts['plastic_corner_post'] / material_types['plastic_corner_post']['pieces_in_bundle']) * material_types['plastic_corner_post']['my_price']
    subtotal += math.ceil(material_amounts['plastic_line_post'] / material_types['plastic_line_post']['pieces_in_bundle']) * material_types['plastic_line_post']['my_price']
    subtotal += math.ceil(material_amounts['plastic_end_post'] / material_types['plastic_end_post']['pieces_in_bundle']) * material_types['plastic_end_post']['my_price']
    subtotal += math.ceil(material_amounts['plastic_gate_post'] / material_types['plastic_gate_post']['pieces_in_bundle']) * material_types['plastic_gate_post']['my_price']
    subtotal += math.ceil(material_amounts['plastic_rail'] / material_types['plastic_rail']['pieces_in_bundle']) * material_types['plastic_rail']['my_price']
    subtotal += math.ceil(material_amounts['plastic_u_channel'] / material_types['plastic_u_channel']['pieces_in_bundle']) * material_types['plastic_u_channel']['my_price']
    subtotal += math.ceil(material_amounts['plastic_panel'] / material_types['plastic_panel']['pieces_in_bundle']) * material_types['plastic_panel']['my_price']
    subtotal += math.ceil(material_amounts['plastic_collar'] / material_types['plastic_collar']['pieces_in_bundle']) * material_types['plastic_collar']['my_price']
    subtotal += math.ceil(material_amounts['plastic_cap'] / material_types['plastic_cap']['pieces_in_bundle']) * material_types['plastic_cap']['my_price']
    subtotal += math.ceil(material_amounts['gate_hinge'] / material_types['gate_hinge']['pieces_in_bundle']) * material_types['gate_hinge']['my_price']
    subtotal += math.ceil(material_amounts['gate_latch'] / material_types['gate_latch']['pieces_in_bundle']) * material_types['gate_latch']['my_price']

    gstPercent = PriceCalculation.gstPercent
    gst = subtotal * gstPercent
    total = subtotal + gst

    return subtotal, gst, total

def calculateQuote(project):
    layout_id = project.layout_selected
    appearance_id = project.appearance_selected

    layout = dbSession.query(Layout).filter(Layout.layout_id == layout_id).one()
    appearance = dbSession.query(Appearance).filter(Appearance.appearance_id == appearance_id).one()

    appearance_value, removal_value, gate_single_value, gate_double_value = Appearances.getAppearanceValues(appearance)

    # Get layout info and pass to parser
    parsed = DiagramParser.parse(layout.layout_info)
    print(parsed)
    # Pass parsed layout to calculate prices for each object
    prices = QuoteCalculation.prices(parsed, appearance_value, removal_value, gate_single_value, gate_double_value)
    print(prices)
    # Calculate subtotal, gst, and total
    subtotal = PriceCalculation.subtotal(prices)
    gstPercent = PriceCalculation.gstPercent
    gst = subtotal * gstPercent
    total = subtotal + gst

    return subtotal, gst, total
