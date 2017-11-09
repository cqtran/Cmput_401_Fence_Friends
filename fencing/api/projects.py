from sqlalchemy import *
from database.db import dbSession, init_db
from database.models import Project, Customer, Quote
from flask.json import jsonify

from flask import Blueprint, request
from flask.json import jsonify
from flask_security.core import current_user
from flask_security import login_required
from flask_security.decorators import roles_required

projectBlueprint = Blueprint('projectBlueprint', __name__, template_folder='templates')

@projectBlueprint.route('/getProjectList/', defaults={'customer_id': None}, methods=['GET'])
@projectBlueprint.route('/getProjectList/<int:customer_id>', methods=['GET'])
#@login_required
#@roles_required('primary')
def getProjectList(customer_id):
    if request.method == 'GET':
        projectList = dbSession.query(Project)
        #projectList = projectList.filter(Customer.company_name == current_user.company_name)
        if customer_id is not None:
            projectList = projectList.filter(customer_id == Project.customer_id)
        projectList = projectList.filter(Customer.customer_id == Project.customer_id).all()
        return jsonify(projectList)

@projectBlueprint.route('/getProject/<int:project_id>', methods=['GET'])
#@login_required
#@roles_required('primary')
def getProject(project_id):
    if request.method == "GET":
        project = dbSession.query(Project)
        project = project.filter(Project.project_id == project_id).all()
        return jsonify(project)

def updateProjectInfo(project_id, project_name, address, status, note):
    """ Updates the project information of a given project id """
    project = dbSession.query(Project).filter(Project.project_id == project_id).all()

    project[0].project_name = project_name
    project[0].address = address
    project[0].status_name = status
    project[0].note = note

    dbSession.commit()
    return True

def createProject(customerId, statusName, address, companyName, project_name):
    #Access MySQL and add in account
    newProject = Project(customer_id = customerId, address = address,
            status_name = statusName, end_date = None, note = '',
            project_name = project_name, company_name = companyName)

    dbSession.add(newProject)
    dbSession.commit()
    newQuote = Quote(project_id = newProject.project_id, quote = 0 , project_info = "data:image/svg+xml;base64,PCFET0NUWVBFIHN2ZyBQVUJMSUMgIi0vL1czQy8vRFREIFNWRyAxLjEvL0VOIiAiaHR0cDovL3d3dy53My5vcmcvR3JhcGhpY3MvU1ZHLzEuMS9EVEQvc3ZnMTEuZHRkIj4KPHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHhtbG5zOnhsaW5rPSJodHRwOi8vd3d3LnczLm9yZy8xOTk5L3hsaW5rIiB3aWR0aD0iMzAxcHgiIGhlaWdodD0iMzAxcHgiIHZlcnNpb249IjEuMSIgY29udGVudD0iJmx0O214ZmlsZSB1c2VyQWdlbnQ9JnF1b3Q7TW96aWxsYS81LjAgKE1hY2ludG9zaDsgSW50ZWwgTWFjIE9TIFggMTBfMTNfMSkgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgQ2hyb21lLzYxLjAuMzE2My4xMDAgU2FmYXJpLzUzNy4zNiZxdW90OyB2ZXJzaW9uPSZxdW90OzcuNi43JnF1b3Q7IGVkaXRvcj0mcXVvdDt3d3cuZHJhdy5pbyZxdW90OyZndDsmbHQ7ZGlhZ3JhbSZndDtqVk5OVTRNd0VQMDFISjBCVXR0NjFMYnF4Uk1Ienlzc1NjWkFNSVFDL25xWEpvRXluYzdJQVhiZmZzNTdTOFFPMWZCbW9CRWZ1a0FWcFhFeFJPd1lwZWt1VHVrOUFhTUROazk3QjNBakN3Y2xDNURKWC9SZzdORk9GdGl1RXEzV3lzcG1EZWE2cmpHM0t3eU0wZjA2cmRScVBiVUJqamRBbG9PNlJUOWxZWVZEOTQveGdyK2o1Q0pNVG1JZitZTDhteHZkMVg1ZWxMTHk4cmh3QmFHWHoyOEZGTHEvZ3RncFlnZWp0WFZXTlJ4UVRkUUcybHpkNjUzb3ZMZkIydjZud090MEJ0VmgySGlycVBTbDFOU0JGclNqSjJYNzAra1FlR2d2a2oxVHdpWnVoaVZJRnArK1J3UDlwTDhFYnFBS1BXa1AxOVlsZVFybUNXa3ZwTVdzZ1h6eWU3b3NTaEsyVXVRbFpFTGJPTEZMT1dBeE56aWpzVGpjSlNDWmFhVnJSVjJoTlNPbGhJS2RWMklNcCt2Y2ZwR2RCWEhGbGVRekNQN1UrTng2b1pzTXozaHdGMlV2c2F1L2g1MytBQT09Jmx0Oy9kaWFncmFtJmd0OyZsdDsvbXhmaWxlJmd0OyIgc3R5bGU9ImJhY2tncm91bmQtY29sb3I6IHJnYigyNTUsIDI1NSwgMjU1KTsiPjxkZWZzLz48ZyB0cmFuc2Zvcm09InRyYW5zbGF0ZSgwLjUsMC41KSI+PHJlY3QgeD0iMCIgeT0iMCIgd2lkdGg9IjMwMCIgaGVpZ2h0PSIzMDAiIGZpbGw9IiNmZmZmZmYiIHN0cm9rZT0iIzAwMDAwMCIgcG9pbnRlci1ldmVudHM9Im5vbmUiLz48ZyB0cmFuc2Zvcm09InRyYW5zbGF0ZSgyNS41LDEyNi41KSI+PHN3aXRjaD48Zm9yZWlnbk9iamVjdCBzdHlsZT0ib3ZlcmZsb3c6dmlzaWJsZTsiIHBvaW50ZXItZXZlbnRzPSJhbGwiIHdpZHRoPSIyNDgiIGhlaWdodD0iNDYiIHJlcXVpcmVkRmVhdHVyZXM9Imh0dHA6Ly93d3cudzMub3JnL1RSL1NWRzExL2ZlYXR1cmUjRXh0ZW5zaWJpbGl0eSI+PGRpdiB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMTk5OS94aHRtbCIgc3R5bGU9ImRpc3BsYXk6IGlubGluZS1ibG9jazsgZm9udC1zaXplOiAxMnB4OyBmb250LWZhbWlseTogSGVsdmV0aWNhOyBjb2xvcjogcmdiKDAsIDAsIDApOyBsaW5lLWhlaWdodDogMS4yOyB2ZXJ0aWNhbC1hbGlnbjogdG9wOyB3aWR0aDogMjUwcHg7IHdoaXRlLXNwYWNlOiBub3dyYXA7IHdvcmQtd3JhcDogbm9ybWFsOyB0ZXh0LWFsaWduOiBjZW50ZXI7Ij48ZGl2IHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8xOTk5L3hodG1sIiBzdHlsZT0iZGlzcGxheTppbmxpbmUtYmxvY2s7dGV4dC1hbGlnbjppbmhlcml0O3RleHQtZGVjb3JhdGlvbjppbmhlcml0OyI+PGZvbnQgc3R5bGU9ImZvbnQtc2l6ZTogNDBweCI+RHJhdyBkaWFncmFtPC9mb250PjwvZGl2PjwvZGl2PjwvZm9yZWlnbk9iamVjdD48dGV4dCB4PSIxMjQiIHk9IjI5IiBmaWxsPSIjMDAwMDAwIiB0ZXh0LWFuY2hvcj0ibWlkZGxlIiBmb250LXNpemU9IjEycHgiIGZvbnQtZmFtaWx5PSJIZWx2ZXRpY2EiPiZsdDtmb250IHN0eWxlPSJmb250LXNpemU6IDQwcHgiJmd0O0RyYXcgZGlhZ3JhbSZsdDsvZm9udCZndDs8L3RleHQ+PC9zd2l0Y2g+PC9nPjwvZz48L3N2Zz4="
                     , note = "")
    dbSession.add(newQuote)
    dbSession.commit()

    return True

def getdrawiopic(project_id):
    #TODO: function should be renamed in the future for clarity purposes
    getpic = dbSession.query(Quote).filter(Quote.project_id == project_id).all()
    json_response = [i.serialize for i in getpic]
    return json_response

def updatedrawiopic(quote_id, quote, project_info, note):
    # ERIC PLEASE HELP
    #TODO: function should be renamed in the future for clarity purposes
    quotation = dbSession.query(Quote)
    quotation = quotation.filter(Quote.quote_id == quote_id).all()
    quotation[0].quote = quote
    quotation[0].project_info = project_info
    print("this is projectinfo")
    print(project_info)
    quotation[0].note = note
    dbSession.commit()
    return True

def savenote(note, pid):
    """Save the given note to the database"""
    #CHANGED: savenote function may be deprecated
    project = dbSession.query(Project)
    project = project.filter(Project.project_id == pid).all()
    project[0].note = note
    dbSession.commit()
    #savenoteintoserver = update(Project).where(Project.project_id == pid).values(Note = note)

    return True
