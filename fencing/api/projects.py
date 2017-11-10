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

        if customer_id is not None:
           projectList = projectList.filter(Project.customer_id == customer_id)
        
        status = request.args.get('status')

        if status is None or status == "All" or status == "None":
            projectList = projectList.filter(Customer.customer_id == Project.customer_id).order_by(desc(Project.start_date)).all()
        
        else:
            projectList = projectList.filter(Customer.customer_id == Project.customer_id).filter(Project.status_name == status)\
            .order_by(desc(Project.start_date)).all()

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
    newQuote = Quote(project_id = newProject.project_id, quote = 0 , project_info = "data:image/svg+xml;base64,PCFET0NUWVBFIHN2ZyBQVUJMSUMgIi0vL1czQy8vRFREIFNWRyAxLjEvL0VOIiAiaHR0cDovL3d3dy53My5vcmcvR3JhcGhpY3MvU1ZHLzEuMS9EVEQvc3ZnMTEuZHRkIj4KPHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHhtbG5zOnhsaW5rPSJodHRwOi8vd3d3LnczLm9yZy8xOTk5L3hsaW5rIiB3aWR0aD0iMzkxcHgiIGhlaWdodD0iMTgxcHgiIHZlcnNpb249IjEuMSIgY29udGVudD0iJmx0O214ZmlsZSB1c2VyQWdlbnQ9JnF1b3Q7TW96aWxsYS81LjAgKE1hY2ludG9zaDsgSW50ZWwgTWFjIE9TIFggMTBfMTNfMSkgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgQ2hyb21lLzYxLjAuMzE2My4xMDAgU2FmYXJpLzUzNy4zNiZxdW90OyB2ZXJzaW9uPSZxdW90OzcuNi43JnF1b3Q7IGVkaXRvcj0mcXVvdDt3d3cuZHJhdy5pbyZxdW90OyZndDsmbHQ7ZGlhZ3JhbSZndDtqWk5OYzRNZ0VJWi9qY2ZPS0VTVEhCT1R0cGVlY3VpWnlxcE1VQ3hpTlAzMUJRRS9KczFNUFNnKzczN0E3aExndEJyZUpHbktEMEdCQnlpa1E0QlBBVUxiYUt2ZkJ0d3RpT085QllWazFLSm9CaGYyQXc2R2puYU1RcnN5VkVKd3habzF6RVJkUTZaV2pFZ3ArclZaTHZnNmEwTUtlQUNYalBCSCtzbW9LaTNkeGVITTM0RVZwYzhjaFU3NUl0bTFrS0tyWGI0QTRYeDhyRndSSDh2WnR5V2hvbDhnZkE1d0tvVlFkbFVOS1hCVFdsODI2L2Y2UkozMkxhRlcvM0ZBMXVGR2VBZCt4d25YcnNkYzZBaW13bHpJVVVtK083T3I0K0pJTXdwYmRYZkY4OUFFZUduSDFoNjBRWXlhWWVtUkZPWjdvTlNNQ1NPRkpKVlByYmRyczFzYlY2a3BBUnJyQytZRWtaYjdraW00TkNRemFxL0hVYk5TVmR6Sk9lTThuUTZCTWRvbnlVYnpWa2x4aGI4VW9XTXhaU1kzU2FiME41QUtocWRWanFiZTZTc0JvZ0lsNzlyRU8yRFhibmNkb28zNzcrZmh3bnZIeXVWZzdSd2ticUNMS2ZiY1ZMMXdmZlcvOC95TTJ1S080dk12Jmx0Oy9kaWFncmFtJmd0OyZsdDsvbXhmaWxlJmd0OyIgc3R5bGU9ImJhY2tncm91bmQtY29sb3I6IHJnYigyNTUsIDI1NSwgMjU1KTsiPjxkZWZzLz48ZyB0cmFuc2Zvcm09InRyYW5zbGF0ZSgwLjUsMC41KSI+PHJlY3QgeD0iMCIgeT0iMCIgd2lkdGg9IjM5MCIgaGVpZ2h0PSIxODAiIHJ4PSIyNyIgcnk9IjI3IiBmaWxsLW9wYWNpdHk9IjAuNjYiIGZpbGw9IiMzMjk2NjQiIHN0cm9rZT0iIzMyOTY2NCIgc3Ryb2tlLW9wYWNpdHk9IjAuNjYiIHBvaW50ZXItZXZlbnRzPSJub25lIi8+PGcgdHJhbnNmb3JtPSJ0cmFuc2xhdGUoNDcuNSw1OS41KSI+PHN3aXRjaD48Zm9yZWlnbk9iamVjdCBzdHlsZT0ib3ZlcmZsb3c6dmlzaWJsZTsiIHBvaW50ZXItZXZlbnRzPSJhbGwiIHdpZHRoPSIyOTQiIGhlaWdodD0iNjAiIHJlcXVpcmVkRmVhdHVyZXM9Imh0dHA6Ly93d3cudzMub3JnL1RSL1NWRzExL2ZlYXR1cmUjRXh0ZW5zaWJpbGl0eSI+PGRpdiB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMTk5OS94aHRtbCIgc3R5bGU9ImRpc3BsYXk6IGlubGluZS1ibG9jazsgZm9udC1zaXplOiAxMnB4OyBmb250LWZhbWlseTogSGVsdmV0aWNhOyBjb2xvcjogcmdiKDAsIDAsIDApOyBsaW5lLWhlaWdodDogMS4yOyB2ZXJ0aWNhbC1hbGlnbjogdG9wOyB3aWR0aDogMjk2cHg7IHdoaXRlLXNwYWNlOiBub3dyYXA7IHdvcmQtd3JhcDogbm9ybWFsOyB0ZXh0LWFsaWduOiBjZW50ZXI7Ij48ZGl2IHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8xOTk5L3hodG1sIiBzdHlsZT0iZGlzcGxheTppbmxpbmUtYmxvY2s7dGV4dC1hbGlnbjppbmhlcml0O3RleHQtZGVjb3JhdGlvbjppbmhlcml0OyI+PGZvbnQgY29sb3I9IiNmZmZmZmYiIHN0eWxlPSJmb250LXNpemU6IDUycHgiPkFkZCBkaWFncmFtPC9mb250PjwvZGl2PjwvZGl2PjwvZm9yZWlnbk9iamVjdD48dGV4dCB4PSIxNDciIHk9IjM2IiBmaWxsPSIjMDAwMDAwIiB0ZXh0LWFuY2hvcj0ibWlkZGxlIiBmb250LXNpemU9IjEycHgiIGZvbnQtZmFtaWx5PSJIZWx2ZXRpY2EiPiZsdDtmb250IGNvbG9yPSIjZmZmZmZmIiBzdHlsZT0iZm9udC1zaXplOiA1MnB4IiZndDtBZGQgZGlhZ3JhbSZsdDsvZm9udCZndDs8L3RleHQ+PC9zd2l0Y2g+PC9nPjwvZz48L3N2Zz4="
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
