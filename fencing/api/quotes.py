from sqlalchemy import *
from database.db import dbSession, init_db
from database.models import Project, Layout, Appearance
from flask.json import jsonify

from flask import Blueprint, request
from flask_security.core import current_user
from flask_security import login_required
from flask_security.decorators import roles_required
from api.errors import *
from decimal import Decimal
from diagram.DiagramParser import DiagramParser

quoteBlueprint = Blueprint('quoteBlueprint', __name__, template_folder='templates')

@quoteBlueprint.route('/finalizeQuote/', methods=['POST'])
#@login_required
#@roles_required('primary')
def finalizeQuote():
    if request.method == 'POST':
        """
        Given a project ID and a boolean finalize.
        Turn finalize to false if finalize is False.
        Generate and save the quote if finalize is True
        """

        project_id = request.args.get('proj_id')
        finalize = request.json['finalize']
        project = dbSession.query(Project).filter(Project.project_id == project_id).one()

        if project is None:
            return bad_request('Project does not exist')

        if not finalize:
            project.finalize = False
            dbSession.commit()
            return created_request('Finalize set to false')

        project.finalize = True
        dbSession.commit()
        layout_id = project.layout_selected
        appearance_id = project.appearance_selected

        layout = dbSession.query(Layout).filter(Layout.layout_id == layout_id).one()
        appearance = dbSession.query(Appearance).filter(Appearance.appearance_id == appearance_id).one()
        if layout is None or appearance is None:
            return bad_request('Invalid layout or appearance')

        # Get layout info and pass to parser
        layout.layout_info
        parsed = DiagramParser.parse(layout.layout_info)
        print(parsed)
        # Get appearance info and calculate a quote with the formula
        # quote  = length(style + height + base_price + ((border_colour + panel_colour) / 2))

        # Calculate needed materials and material expenses

        # Save the quote information
        # newQuote = Quote(project_id = project_id, amount = quote, amount_gst = quote * 0.05, material_expense = material_expense, material_expense_gst = material_expense_gst)
        # dbSession.add(newQuote)
        # dbSession.commit()

        return created_request('Quote has been generated')
    return bad_request('Request is not a POST request')
