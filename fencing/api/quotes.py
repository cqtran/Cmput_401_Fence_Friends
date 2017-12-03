from sqlalchemy import *
from database.db import dbSession, init_db
from database.models import Project, Quote, Layout, Appearance, Material
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
from api.email.Messages import Messages
from api.email.Email import Email
import math
import json
import os

quoteBlueprint = Blueprint('quoteBlueprint', __name__, template_folder='templates')
app_root = ''

@quoteBlueprint.route('/unfinalizeQuote/', methods=['POST'])
@login_required
@roles_required('primary')
def unfinalizeQuote():
    if request.method == 'POST':
        project_id = request.values.get('proj_id')
        project = dbSession.query(Project).filter(Project.project_id == project_id).one()

        quoteToDelete = dbSession.query(Quote).filter(Quote.project_id == project_id)
        quoteFiles = quoteToDelete.one()

        deletePDFHelper(quoteFiles.quote_pdf)
        deletePDFHelper(quoteFiles.supply_pdf)
        quoteToDelete.delete()

        project.finalize = False
        dbSession.commit()
        return "{}"
    return bad_request('Request is not a POST request')

def deletePDFHelper(filename):
    try:
        filePath = os.path.join(app_root, 'static', filename)
        os.remove(filePath)
    except:
        print('Could not delete PDF at: ' + filePath)
    return

def generateQuote(project, material_types, material_amounts,
    misc_modifier):

    project_id = project.project_id

    gst_rate = PriceCalculation.gstPercent()
    amount, amount_gst, amount_total = calculateQuote(project, misc_modifier, gst_rate)
    material_expense, material_expense_gst, material_expense_total = calculateExpense(material_types, material_amounts, gst_rate)
    profit = amount - material_expense_total

    quoteRecord = Messages.quoteAttachment(project, misc=misc_modifier)
    materialRecord = Messages.materialListAttachment(project, material_types,
        material_amounts)
    quotePath = Email.makeAttachment("finalized/quotes", quoteRecord)
    materialListPath = Email.makeAttachment("finalized/materials",
        materialRecord)

    return Quote(project_id = project_id, amount = amount, amount_gst = amount_gst, amount_total = amount_total, material_expense = material_expense, material_expense_gst = material_expense_gst, material_expense_total = material_expense_total, profit = profit, gst_rate = gst_rate, quote_pdf = quotePath, supply_pdf = materialListPath)

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

        project_id = request.values.get('proj_id')
        # A dictionary with keywords and values of material_ids
        material_types = json.loads(request.values.get('material_types'))
        # A dictionary with keywords and values of the amount of material needed
        material_amounts = json.loads(request.values.get('material_amounts'))

        # A flat rate which allows the user to alter the subtotal of the quote
        misc_modifier = request.values.get('misc_modifier')
        if misc_modifier == "":
            misc_modifier = 0
        else:
            misc_modifier = int(misc_modifier)

        project = dbSession.query(Project).filter(Project.project_id == project_id).one()
        if project is None:
            print('Project does not exist')
            return bad_request('Project does not exist')

        if material_types is None or material_amounts is None:
            print('Material Parameters not given')
            return bad_request('Material Parameters not given')

        if project.finalize:
            print('Project has already been finalized')
            return bad_request('Project has already been finalized')

        project.finalize = True

        try:
            newQuote = generateQuote(project, material_types, material_amounts,
                misc_modifier)
            dbSession.add(newQuote)
            dbSession.commit()
        except BaseException as e:
            raise e
            print('Error in saving the quote')
            return bad_request('Error in saving the quote')

        return created_request('Quote has been generated')
    print('Request is not a POST request')
    return bad_request('Request is not a POST request')

@quoteBlueprint.route('/getProfit/', methods=['POST'])
@login_required
@roles_required('primary')
def getProfit():
    if request.method == 'POST':
        year_filter = request.values.get('year')

        quotes = dbSession.query(Quote).filter(Project.company_name == current_user.company_name).filter(Project.status_name == 'Paid').filter(Project.finalize == True).filter(Quote.project_id == Project.project_id)

        # Filter Quotes by year if 0 is not given
        if year_filter != '0' and year_filter is not None:
            year_filter = int(year_filter)
            quotes = quotes.filter(extract('year', Project.end_date) == year_filter)

        quotes = quotes.order_by(Project.end_date).all()
        profits = []
        projects = []
        for quote in quotes:
            project = dbSession.query(Project).filter(Project.project_id == quote.project_id).one()
            projects.append(project.project_name)
            profits.append(quote.profit)

        dictionary = {"projects" : projects, "profits" : profits}

        return jsonify(dictionary)
    return bad_request('Request is not a POST request')

def calculateExpense(material_types, material_amounts, gst_rate):
    categories = ['metal_post', 'metal_u_channel', 'metal_lsteel', 'plastic_t_post', 'plastic_corner_post', 'plastic_line_post', 'plastic_end_post',
        'plastic_gate_post', 'plastic_rail', 'plastic_u_channel', 'plastic_panel', 'plastic_collar', 'plastic_cap', 'gate_hinge', 'gate_latch']
    subtotal = 0

    materials = dbSession.query(Material).filter(Material.company_name == current_user.company_name)

    # For each category in the dictionary, use the material_id and query for data
    # number of materials needed / number of materials per bundle * price of material
    for category in categories:
        amount = material_amounts[category]

        if amount == "":
            amount = 0
        else:
            amount = int(amount)

        material = materials.filter(Material.material_id == int(material_types[category])).one()
        subtotal += math.ceil(amount / material.pieces_in_bundle) * material.my_price

    # Calculate gst
    gst = subtotal * gst_rate
    total = subtotal + gst

    # PDF Should be generated too
    return subtotal, gst, total

def calculateQuote(project, misc_modifier, gst_rate):
    layout_id = project.layout_selected
    appearance_id = project.appearance_selected

    layout = dbSession.query(Layout).filter(Layout.layout_id == layout_id).one()
    appearance = dbSession.query(Appearance).filter(Appearance.appearance_id == appearance_id).one()

    appearance_value, removal_value, gate_single_value, gate_double_value = Appearances.getAppearanceValues(appearance)

    # Get layout info and pass to parser
    parsed = DiagramParser.parse(layout.layout_info)
    # Pass parsed layout to calculate prices for each object
    prices = QuoteCalculation.prices(parsed, appearance_value, removal_value, gate_single_value, gate_double_value)
    # Calculate subtotal, gst, and total
    subtotal = PriceCalculation.subtotal(prices)

    if misc_modifier is not None:
        subtotal += misc_modifier


    gst = subtotal * gst_rate
    total = subtotal + gst

    # PDF Should be generated too
    return subtotal, gst, total
