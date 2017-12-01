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

def getAccountingSummary():
    """ Returns a list of accounting related calculations """
    if request.method == 'POST':
        quote = dbSession.query(Quote).all()
        send = {"data" : quote}
        print("here")
        if len(quote) == 0:
            return bad_request('no quotes were found')
        return jsonify(send)
    pass

@accountingBlueprint.route('/exportAccountingSummary/', methods=['GET'])

def exportAccountingSummary():
    """ Returns a downloadable file of the accounting summary """
    #return send_from_directory(directory=uploads, filename=filename)
    pass




def getQuoteInfo():

    quote = dbSession.query(Quote).all()

    dbSession.commit()


    return quote