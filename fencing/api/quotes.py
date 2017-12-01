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

        num_t_post, num_corner_post, num_line_post, num_end_post, num_gate_posts, num_steel_post = posts(parsed)
        print('\n')
        num_caps = num_steel_post
        num_collars = num_steel_post * 2

        num_small_sections, num_medium_sections, num_big_sections, num_sections = sections(parsed)
        num_uchannel = num_sections * 2
        num_metal_uchannel = num_medium_sections + num_big_sections
        num_rails = num_sections * 2
        num_panels = panels(parsed)

        num_hinges, num_latches, num_drop_pins, num_gate_rails, num_gate_uchannel, num_gate_panels, num_cement = gates(parsed)
        num_Lsteel = num_cement

        print('\nSteel')
        print('Metal Post: ',num_steel_post)
        print('Metal U-Channel: ', num_metal_uchannel)
        print('Metal L-Steel', num_Lsteel)
        print('\nPlastic Posts')
        print('Plastic T-Post', num_t_post)
        print('Plastic Corner-Post', num_corner_post)
        print('Plastic Line-Post', num_line_post)
        print('Plastic End-Post', num_end_post)
        print('Plastic Gate-Post', num_gate_posts)
        print('\nPlastic')
        print('Plastic Rails', num_rails)
        print('Plastic U-Channel',num_uchannel)
        print('Plastic T&G (Panels)',num_panels)
        print('Plastic Collars', num_collars)
        print('Plastic Caps',num_caps)
        print('\nGate')
        print('Hinges',num_hinges)
        print('Latches',num_latches)
        print('Drop Pins',num_drop_pins)
        print('Gate Rails',num_gate_rails)
        print('Gate U-Channel', num_gate_uchannel)
        print('Gate Panels',num_gate_panels)
        print('Cement', num_cement)

        
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

def posts(parsed):
    num_t_post = 0
    num_corner_post = 0
    num_line_post = 0
    num_end_post = 0
    num_gate_posts = 0
    for post in parsed.posts():
        if not post.isRemoval:
            if post.postType == 'tPost':
                num_t_post += 1
            if post.postType == 'cornerPost':
                num_corner_post += 1
            if post.postType == 'endPost':
                num_end_post += 1
            if post.postType == 'gatePost':
                num_gate_posts += 1

    for fence in parsed.fences:
        if not fence.isRemoval:
            if (fence.length/12) % 8 == 0:
                num_line_post += (fence.length/12) // 8 - 1
            else:
                num_line_post += (fence.length/12) // 8
    num_steel_post = num_t_post + num_corner_post + num_line_post + num_end_post + num_gate_posts
    return num_t_post, num_corner_post, num_line_post, num_end_post, num_gate_posts, num_steel_post

def sections(parsed):
    num_small_sections = 0
    num_medium_sections = 0
    num_big_sections = 0
    for fence in parsed.fences:
        if not fence.isRemoval:
            num_big_sections += (fence.length/12) // 8
            if (fence.length/12) % 8 < 6 and (fence.length/12) % 8 > 0:
                num_small_sections += 1
            if (fence.length/12) % 8 > 6:
                num_medium_sections += 1
    num_sections = num_small_sections + num_medium_sections + num_big_sections
    return num_small_sections, num_medium_sections, num_big_sections, num_sections

def panels(parsed):
    num_panels = 0
    for fence in parsed.fences:
        num_panels += fence.length/12
    return num_panels

def gates(parsed):
    num_hinges = 0
    num_latches = 0
    num_drop_pins = 0
    num_gate_rails = 0
    num_gate_uchannel = 0
    num_gate_panels = 0
    num_cement = 0
    for gate in parsed.gates:
        if not gate.isRemoval:
            num_latches += 1
            num_gate_uchannel += 2
            num_gate_panels += (gate.length//12)
            if gate.length%12 > 0:
                num_gate_panels += 1
            num_cement += 1
            if gate.isDouble:
                num_hinges += 2
                num_drop_pins += 1
            else:
                num_hinges += 1
            if (gate.length/12) > 4:
                num_gate_rails += 2
            else:
                num_gate_rails += 1
    return num_hinges, num_latches, num_drop_pins, num_gate_rails, num_gate_uchannel, num_gate_panels, num_cement
