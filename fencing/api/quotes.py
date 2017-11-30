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

quoteBlueprint = Blueprint('quoteBlueprint', __name__, template_folder='templates')

@quoteBlueprint.route('/finalizeQuote/', methods=['POST'])
#@login_required
#@roles_required('primary')
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
        finalize = request.json['finalize']
        project = dbSession.query(Project).filter(Project.project_id == project_id).one()

        if project is None:
            print('Project does not exist')
            return bad_request('Project does not exist')

        if not finalize:
            dbSession.query(Quote).filter(Quote.project_id == project_id).delete()
            project.quote_id = None
            project.finalize = False
            dbSession.commit()
            print('Finalize set to false')
            return created_request('Finalize set to false')

        project.finalize = True
        layout_id = project.layout_selected
        appearance_id = project.appearance_selected

        layout = dbSession.query(Layout).filter(Layout.layout_id == layout_id).one()
        appearance = dbSession.query(Appearance).filter(Appearance.appearance_id == appearance_id).one()

        try:
            appearance_value, removal_value, gate_single_value, gate_double_value = getAppearanceValues(appearance)
        except:
            print('One or more appearance selections are invalid')
            return bad_request('One or more appearance selections are invalid')

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

        # TODO: Calculate needed materials and material expenses

        # Save the quote information
        newQuote = Quote(project_id = project_id, amount = subtotal, amount_gst = gst, amount_total = total, material_expense = None, material_expense_gst = None, material_expense_total = None, gst_rate = gstPercent)
        dbSession.add(newQuote)
        dbSession.commit()
        print('Quote has been generated and finalized')
        return created_request('Quote has been generated')
    print('Request is not a POST request')
    return bad_request('Request is not a POST request')

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
