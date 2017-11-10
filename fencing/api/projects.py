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
    newQuote = Quote(project_id = newProject.project_id, quote = 0 , project_info = "data:image/svg+xml;base64,PCFET0NUWVBFIHN2ZyBQVUJMSUMgIi0vL1czQy8vRFREIFNWRyAxLjEvL0VOIiAiaHR0cDovL3d3dy53My5vcmcvR3JhcGhpY3MvU1ZHLzEuMS9EVEQvc3ZnMTEuZHRkIj4KPHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHhtbG5zOnhsaW5rPSJodHRwOi8vd3d3LnczLm9yZy8xOTk5L3hsaW5rIiB3aWR0aD0iMzkxcHgiIGhlaWdodD0iMTgxcHgiIHZlcnNpb249IjEuMSIgY29udGVudD0iJmx0O214ZmlsZSB1c2VyQWdlbnQ9JnF1b3Q7TW96aWxsYS81LjAgKE1hY2ludG9zaDsgSW50ZWwgTWFjIE9TIFggMTBfMTNfMSkgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgQ2hyb21lLzYxLjAuMzE2My4xMDAgU2FmYXJpLzUzNy4zNiZxdW90OyB2ZXJzaW9uPSZxdW90OzcuNi43JnF1b3Q7IGVkaXRvcj0mcXVvdDt3d3cuZHJhdy5pbyZxdW90OyZndDsmbHQ7ZGlhZ3JhbSZndDtqWk5OYzRNZ0VJWi9qY2ZPS0NRMkhoT2J0cGVlY3VpWjZxcE1VQ3hpTmYzMUJWbjhtTFF6OWFENHZQc0J1MHRBMDNwOFVheXQzbVFPSWlCaFBnYjBLU0FrVGg3TjI0S2JBN3ZrNEVDcGVPNVF0SUFML3dhRUlkS2U1OUJ0RExXVVF2TjJDelBaTkpEcERXTkt5V0ZyVmtpeHpkcXlFdTdBSldQaW5yN3pYRmVPSHZiaHdsK0JsNVhQSElXb2ZMRHNXaXJaTjVndklMU1lIaWZYek1kQys2NWl1UnhXaUo0RG1pb3B0VnZWWXdyQ2x0YVh6Zms5LzZITysxYlE2UDg0RU9md3hVUVBmc2V4TUs2blFwb0l0c0pDcWttSlAzdTdxOVBxU0FzS08zM0Q0bmxvQXp4MFUydVB4bUJQMm5IdEVaZjJlOHh6T3lhY2xZclZQclhacnN2dWJMQlNjd0l5MVJmc0NTSWpEeFhYY0dsWlp0WEJqS05obGE0RnlnVVhJcDBQUVNsSjRuaG5lS2VWdk1KdkNwWUVsSWJ4ejdKR2M3UE1IUUJaZzFZM1krSWRLUFlYNXovYTRmK3dUQk5Oa0ZYclNUb2daRGpCNVJ4NzZhSlpZQ1A5N3pJd2s3YTZsUFQ4QXc9PSZsdDsvZGlhZ3JhbSZndDsmbHQ7L214ZmlsZSZndDsiIHN0eWxlPSJiYWNrZ3JvdW5kLWNvbG9yOiByZ2IoMjU1LCAyNTUsIDI1NSk7Ij48ZGVmcy8+PGcgdHJhbnNmb3JtPSJ0cmFuc2xhdGUoMC41LDAuNSkiPjxyZWN0IHg9IjAiIHk9IjAiIHdpZHRoPSIzOTAiIGhlaWdodD0iMTgwIiByeD0iMjciIHJ5PSIyNyIgZmlsbD0iIzMyOTY2NCIgc3Ryb2tlPSIjMzI5NjY0IiBwb2ludGVyLWV2ZW50cz0ibm9uZSIvPjxnIHRyYW5zZm9ybT0idHJhbnNsYXRlKDQ3LjUsNTkuNSkiPjxzd2l0Y2g+PGZvcmVpZ25PYmplY3Qgc3R5bGU9Im92ZXJmbG93OnZpc2libGU7IiBwb2ludGVyLWV2ZW50cz0iYWxsIiB3aWR0aD0iMjk0IiBoZWlnaHQ9IjYwIiByZXF1aXJlZEZlYXR1cmVzPSJodHRwOi8vd3d3LnczLm9yZy9UUi9TVkcxMS9mZWF0dXJlI0V4dGVuc2liaWxpdHkiPjxkaXYgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzE5OTkveGh0bWwiIHN0eWxlPSJkaXNwbGF5OiBpbmxpbmUtYmxvY2s7IGZvbnQtc2l6ZTogMTJweDsgZm9udC1mYW1pbHk6IEhlbHZldGljYTsgY29sb3I6IHJnYigwLCAwLCAwKTsgbGluZS1oZWlnaHQ6IDEuMjsgdmVydGljYWwtYWxpZ246IHRvcDsgd2lkdGg6IDI5NnB4OyB3aGl0ZS1zcGFjZTogbm93cmFwOyB3b3JkLXdyYXA6IG5vcm1hbDsgdGV4dC1hbGlnbjogY2VudGVyOyI+PGRpdiB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMTk5OS94aHRtbCIgc3R5bGU9ImRpc3BsYXk6aW5saW5lLWJsb2NrO3RleHQtYWxpZ246aW5oZXJpdDt0ZXh0LWRlY29yYXRpb246aW5oZXJpdDsiPjxmb250IGNvbG9yPSIjZmZmZmZmIiBzdHlsZT0iZm9udC1zaXplOiA1MnB4Ij5BZGQgZGlhZ3JhbTwvZm9udD48L2Rpdj48L2Rpdj48L2ZvcmVpZ25PYmplY3Q+PHRleHQgeD0iMTQ3IiB5PSIzNiIgZmlsbD0iIzAwMDAwMCIgdGV4dC1hbmNob3I9Im1pZGRsZSIgZm9udC1zaXplPSIxMnB4IiBmb250LWZhbWlseT0iSGVsdmV0aWNhIj4mbHQ7Zm9udCBjb2xvcj0iI2ZmZmZmZiIgc3R5bGU9ImZvbnQtc2l6ZTogNTJweCImZ3Q7QWRkIGRpYWdyYW0mbHQ7L2ZvbnQmZ3Q7PC90ZXh0Pjwvc3dpdGNoPjwvZz48L2c+PC9zdmc+"
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
