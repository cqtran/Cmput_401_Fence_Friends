from sqlalchemy import *
from database.db import dbSession, init_db
from database.models import Customer, Project, Quote
from flask.json import jsonify
import json
from flask import Blueprint, request
from flask_security.core import current_user
from flask_security import login_required
from flask_security.decorators import roles_required
from api.errors import bad_request

accountingBlueprint = Blueprint('accountingBlueprint', __name__, template_folder='templates')

@accountingBlueprint.route('/getAccountingSummary/', methods=['POST'])
@login_required
@roles_required('primary')
def getAccountingSummary():
    """ Returns a list of accounting related calculations """
    if request.method == 'POST':
        year_filter = request.values.get('year')
        
        quotes = dbSession.query(Quote).filter(Project.company_name == current_user.company_name).filter(Project.status_name == 'Paid').filter(Project.finalize == True).filter(Quote.project_id == Project.project_id)

        # Filter Quotes by year if 0 is not given
        if year_filter != '0' and year_filter is not None:
            year_filter = int(year_filter)
            quotes = quotes.filter(extract('year', Project.end_date) == year_filter)

        quotes = quotes.order_by(Project.end_date).all()
        send = {"data" : quotes}
        print("here")
        if len(quotes) == 0:
            return bad_request('no quotes were found')
        return jsonify(send)
    pass

@accountingBlueprint.route('/exportAccountingSummary/', methods=['GET'])
@login_required
@roles_required('primary')
def exportAccountingSummary():
    """ Returns a downloadable file of the accounting summary """
    #return send_from_directory(directory=uploads, filename=filename)
    pass




def getQuoteInfo():

    quote = dbSession.query(Quote).all()

    dbSession.commit()


    return quote
