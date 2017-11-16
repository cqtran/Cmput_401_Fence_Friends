from sqlalchemy import *
from database.db import dbSession, init_db
from database.models import Project, Customer, Quote
from flask.json import jsonify

from flask import Blueprint, request
from flask.json import jsonify
from flask_security.core import current_user
from flask_security import login_required
from flask_security.decorators import roles_required
from api.errors import bad_request

projectBlueprint = Blueprint('projectBlueprint', __name__, template_folder='templates')

@projectBlueprint.route('/getProjectList/', defaults={'customer_id': None}, methods=['GET'])
@projectBlueprint.route('/getProjectList/<int:customer_id>', methods=['GET'])
#@login_required
#@roles_required('primary')
def getProjectList(customer_id):
    """ Returns a list of projects. If a customer id is provided, the list will contain
    only contain projects to the given customer id """
    if request.method == 'GET':
        search = request.args.get("search")
        status = request.args.get('status')
        projectList = dbSession.query(Project)

        if customer_id is not None:
           projectList = projectList.filter(Project.customer_id == customer_id)

        if status is None or status == "All" or status == "None":
            projectList = projectList.filter(Customer.customer_id == Project.customer_id).order_by(desc(Project.start_date))

        else:
            projectList = projectList.filter(Customer.customer_id == Project.customer_id).filter(Project.status_name == status)
        
        if search is not None and search != "":
            projectList = projectList.filter(
                Project.project_name.contains(search))
        
        projectList = projectList.order_by(desc(Project.start_date)).all()

        if len(projectList) == 0:
            return bad_request("No projects were found")
        return jsonify(projectList)

@projectBlueprint.route('/getProject/<int:project_id>', methods=['GET'])
#@login_required
#@roles_required('primary')
def getProject(project_id):
    """ Returns a single project of a given project id """
    if request.method == "GET":
        project = dbSession.query(Project)
        project = project.filter(Project.project_id == project_id).all()
        if len(project) == 0:
            return bad_request("The project was not found")
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
    newQuote = Quote(project_id = newProject.project_id, quote = 0 , project_info = "data:image/svg+xml;base64,PCFET0NUWVBFIHN2ZyBQVUJMSUMgIi0vL1czQy8vRFREIFNWRyAxLjEvL0VOIiAiaHR0cDovL3d3dy53My5vcmcvR3JhcGhpY3MvU1ZHLzEuMS9EVEQvc3ZnMTEuZHRkIj4KPHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHhtbG5zOnhsaW5rPSJodHRwOi8vd3d3LnczLm9yZy8xOTk5L3hsaW5rIiB3aWR0aD0iNzAxcHgiIGhlaWdodD0iMzIxcHgiIHZlcnNpb249IjEuMSIgY29udGVudD0iJmx0O214ZmlsZSB1c2VyQWdlbnQ9JnF1b3Q7TW96aWxsYS81LjAgKE1hY2ludG9zaDsgSW50ZWwgTWFjIE9TIFggMTBfMTNfMSkgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgQ2hyb21lLzYxLjAuMzE2My4xMDAgU2FmYXJpLzUzNy4zNiZxdW90OyB2ZXJzaW9uPSZxdW90OzcuNi43JnF1b3Q7IGVkaXRvcj0mcXVvdDt3d3cuZHJhdy5pbyZxdW90OyZndDsmbHQ7ZGlhZ3JhbSBpZD0mcXVvdDtiYTZlNmZlZS1hNTU4LTljODgtMjM1Ny1jMGUyZWYxZGM1OGEmcXVvdDsgbmFtZT0mcXVvdDtQYWdlLTEmcXVvdDsmZ3Q7ZGRIQkVvSWdFQURRcitHT1VFMmV6ZXJTeVVObkVsUW1aQjNFMGZyNk5EQmpMQzdBMjEyV0FVU1RlamdaMWxRWDRFSWhndm1BNkFFUkV0RjRNMDZUUEp6RThjNUJhU1QzU1F0azhpazhZcStkNUtJTkVpMkFzcklKTVFldFJXNmQrVnBtRFBSdFFBV29zR3ZEU3JHQ0xHZHFyVmZKYmVWMHY4V0xuNFVzSzk4NWlyQ1AzRmgrTHcxMDJ2ZERoQmJ2NGNJMW04L3krVzNGT1BSZlJGTkVFd05nM2FvZUVxR210NTJmemRVZC8wUS85elpDMng4RjQySTVlOXdFSDBqVEZ3PT0mbHQ7L2RpYWdyYW0mZ3Q7Jmx0Oy9teGZpbGUmZ3Q7IiBzdHlsZT0iYmFja2dyb3VuZC1jb2xvcjogcmdiKDI1NSwgMjU1LCAyNTUpOyI+PGRlZnMvPjxnIHRyYW5zZm9ybT0idHJhbnNsYXRlKDAuNSwwLjUpIj48cmVjdCB4PSIwIiB5PSIwIiB3aWR0aD0iNzAwIiBoZWlnaHQ9IjMyMCIgcng9IjQ4IiByeT0iNDgiIGZpbGwtb3BhY2l0eT0iMC42NiIgZmlsbD0iIzMyOTY2NCIgc3Ryb2tlPSJub25lIiBwb2ludGVyLWV2ZW50cz0ibm9uZSIvPjxnIHRyYW5zZm9ybT0idHJhbnNsYXRlKDYwLjUsMTAwLjUpIj48c3dpdGNoPjxmb3JlaWduT2JqZWN0IHN0eWxlPSJvdmVyZmxvdzp2aXNpYmxlOyIgcG9pbnRlci1ldmVudHM9ImFsbCIgd2lkdGg9IjU3OCIgaGVpZ2h0PSIxMTgiIHJlcXVpcmVkRmVhdHVyZXM9Imh0dHA6Ly93d3cudzMub3JnL1RSL1NWRzExL2ZlYXR1cmUjRXh0ZW5zaWJpbGl0eSI+PGRpdiB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMTk5OS94aHRtbCIgc3R5bGU9ImRpc3BsYXk6IGlubGluZS1ibG9jazsgZm9udC1zaXplOiAxMnB4OyBmb250LWZhbWlseTogSGVsdmV0aWNhOyBjb2xvcjogcmdiKDAsIDAsIDApOyBsaW5lLWhlaWdodDogMS4yOyB2ZXJ0aWNhbC1hbGlnbjogdG9wOyB3aWR0aDogNTc4cHg7IHdoaXRlLXNwYWNlOiBub3dyYXA7IHdvcmQtd3JhcDogbm9ybWFsOyB0ZXh0LWFsaWduOiBjZW50ZXI7Ij48ZGl2IHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8xOTk5L3hodG1sIiBzdHlsZT0iZGlzcGxheTppbmxpbmUtYmxvY2s7dGV4dC1hbGlnbjppbmhlcml0O3RleHQtZGVjb3JhdGlvbjppbmhlcml0OyI+PGZvbnQgY29sb3I9IiNmZmZmZmYiIHN0eWxlPSJmb250LXNpemU6IDEwMHB4Ij5FZGl0IERpYWdyYW08L2ZvbnQ+PC9kaXY+PC9kaXY+PC9mb3JlaWduT2JqZWN0Pjx0ZXh0IHg9IjI4OSIgeT0iNjUiIGZpbGw9IiMwMDAwMDAiIHRleHQtYW5jaG9yPSJtaWRkbGUiIGZvbnQtc2l6ZT0iMTJweCIgZm9udC1mYW1pbHk9IkhlbHZldGljYSI+Jmx0O2ZvbnQgY29sb3I9IiNmZmZmZmYiIHN0eWxlPSJmb250LXNpemU6IDEwMHB4IiZndDtFZGl0IERpYWdyYW0mbHQ7L2ZvbnQmZ3Q7PC90ZXh0Pjwvc3dpdGNoPjwvZz48L2c+PC9zdmc+"
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
