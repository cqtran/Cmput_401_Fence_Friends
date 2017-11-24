from sqlalchemy import *
from database.db import dbSession
from database.models import Project, Layout, Appearance
from flask.json import jsonify
import json
from flask import Blueprint, request
from flask_security.core import current_user
from flask_security import login_required
from flask_security.decorators import roles_required
from api.errors import bad_request
from diagram.DiagramParser import DiagramParser

layoutBlueprint = Blueprint('layoutBlueprint', __name__, template_folder='templates')

@layoutBlueprint.route('/saveLayoutName/', methods=['POST'])
@login_required
@roles_required('primary')
def saveLayoutName():
    """ Update a layout's name """
    layout_id = request.json['layoutId']
    layout_name = request.json['name']
    layout = dbSession.query(Layout).filter(Layout.layout_id == layout_id).one()
    layout.layout_name = layout_name
    dbSession.commit()
    return "{}"

@layoutBlueprint.route('/removeLayout/', methods = ['POST'])
@login_required
@roles_required('primary')
def removeLayout():
    project_id = request.args.get('proj_id')
    layout_id = request.json['layoutId']
    removeLayout(layout_id)
    return "{}"

@layoutBlueprint.route('/saveDiagram/', methods = ['POST'])
@login_required
@roles_required('primary')
def saveDiagram():
    # parse draw io image and get coordinates and measurements
    project_id = request.args.get('proj_id')

    layout_id = None

    if 'layoutId' in request.json:
        layout_id = request.json['layoutId']

    layout_name = request.json['name']
    image = request.json['image']
    parsed = DiagramParser.parse(image)

    # If the layout already exists and the diagram is empty, do not update it
    # (tell the client to refresh the page instead to get back the old diagram)
    if layout_id is not None:
        if parsed is None:
            updateLayoutName(layout_id, layout_name)
            return '{"reload":1}'

        if parsed.empty:
            updateLayoutName(layout_id, layout_name)
            return '{"reload":1}'

    layout_id = updateLayoutInfo(project_id = project_id,
        layout_id = layout_id, layout_name = layout_name,
        layout_info = image)

    if "saveSelection" in request.json:
        project = dbSession.query(Project).filter(
            Project.project_id == project_id).one()
        project.layout_selected = layout_id
        dbSession.commit()

    return jsonify({"layoutId": layout_id,
        "displayStrings": parsed.displayStrings()})
def getLayouts(project_id):
#TODO: function should be renamed in the future for clarity purposes
    layouts = dbSession.query(Layout).filter(Layout.project_id == project_id).all()
    return layouts

def updateLayoutName(layout_id, layout_name):
    layout = dbSession.query(Layout).filter(Layout.layout_id == layout_id).one()
    layout.layout_name = layout_name
    dbSession.commit()

def updateLayoutInfo(project_id, layout_name, layout_info, layout_id = None):
    # ERIC PLEASE HELP
    #TODO: function should be renamed in the future for clarity purposes
    if layout_id is None:
        layout = createLayout(project_id)
    else:
        layout = dbSession.query(Layout)
        layout = layout.filter(Layout.layout_id == layout_id).one()

    layout.layout_name = layout_name
    layout.layout_info = layout_info
    layout_id = layout.layout_id
    dbSession.commit()
    return layout_id

def removeLayout(layout_id):
    dbSession.query(Layout).filter(Layout.layout_id == layout_id).delete()
    dbSession.commit()

def createLayout(project_id):
    # TODO: This should be in layouts API
    newLayout = Layout(project_id = project_id, layout_name = "Layout 1", layout_info = "data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHhtbG5zOnhsaW5rPSJodHRwOi8vd3d3LnczLm9yZy8xOTk5L3hsaW5rIiB3aWR0aD0iNzAxcHgiIGhlaWdodD0iMzIxcHgiIHZlcnNpb249IjEuMSIgY29udGVudD0iJmx0O214ZmlsZSB1c2VyQWdlbnQ9JnF1b3Q7TW96aWxsYS81LjAgKE1hY2ludG9zaDsgSW50ZWwgTWFjIE9TIFggMTBfMTNfMSkgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgQ2hyb21lLzYxLjAuMzE2My4xMDAgU2FmYXJpLzUzNy4zNiZxdW90OyB2ZXJzaW9uPSZxdW90OzcuNi43JnF1b3Q7IGVkaXRvcj0mcXVvdDt3d3cuZHJhdy5pbyZxdW90OyZndDsmbHQ7ZGlhZ3JhbSBpZD0mcXVvdDtiYTZlNmZlZS1hNTU4LTljODgtMjM1Ny1jMGUyZWYxZGM1OGEmcXVvdDsgbmFtZT0mcXVvdDtQYWdlLTEmcXVvdDsmZ3Q7ZFpIQkVvSWdFSWFmaGp0QkY4OW1kZW5rb1RNQkFoTzZEdUpvUFgwYWxKSEZoZDN2LzNlWFdSRE42L0hnV0t0UElLUkZCSXNSMFIwaVpKTmxtK21heVMyU0xhR0JLR2RFWUhnQnBibkxhQ1NSOWtiSUxqRjZBT3RORzJFY3dLRnBKUGVKa1RrSFExcGJnUlZKWGN1VVhJR1NNN3VtWnlPOERwUmdqQmZoS0kzUy9sdTVNSDVWRHZvbURrU0VWczhUNUpxOW1rVi9wNW1BNFFQUkF0SGNBZmdRMVdNdTdiemRkRy83UCtyNzRVNDIva2ZCRkN5OXB5VDVRbG84QUE9PSZsdDsvZGlhZ3JhbSZndDsmbHQ7L214ZmlsZSZndDsiIHN0eWxlPSJiYWNrZ3JvdW5kLWNvbG9yOiByZ2IoMjU1LCAyNTUsIDI1NSk7Ij48ZGVmcy8+PGcgdHJhbnNmb3JtPSJ0cmFuc2xhdGUoMC41LDAuNSkiPjxyZWN0IHg9IjAiIHk9IjAiIHdpZHRoPSI3MDAiIGhlaWdodD0iMzIwIiByeD0iNDgiIHJ5PSI0OCIgZmlsbC1vcGFjaXR5PSIwLjY2IiBmaWxsPSIjMzI5NjY0IiBzdHJva2U9Im5vbmUiIHBvaW50ZXItZXZlbnRzPSJub25lIi8+PGcgdHJhbnNmb3JtPSJ0cmFuc2xhdGUoNjAuNSwxMDAuNSkiPjxzd2l0Y2g+PGZvcmVpZ25PYmplY3Qgc3R5bGU9Im92ZXJmbG93OnZpc2libGU7IiBwb2ludGVyLWV2ZW50cz0iYWxsIiB3aWR0aD0iNTc4IiBoZWlnaHQ9IjExOCIgcmVxdWlyZWRGZWF0dXJlcz0iaHR0cDovL3d3dy53My5vcmcvVFIvU1ZHMTEvZmVhdHVyZSNFeHRlbnNpYmlsaXR5Ij48ZGl2IHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8xOTk5L3hodG1sIiBzdHlsZT0iZGlzcGxheTogaW5saW5lLWJsb2NrOyBmb250LXNpemU6IDEycHg7IGZvbnQtZmFtaWx5OiBIZWx2ZXRpY2E7IGNvbG9yOiByZ2IoMCwgMCwgMCk7IGxpbmUtaGVpZ2h0OiAxLjI7IHZlcnRpY2FsLWFsaWduOiB0b3A7IHdpZHRoOiA1NzhweDsgd2hpdGUtc3BhY2U6IG5vd3JhcDsgd29yZC13cmFwOiBub3JtYWw7IHRleHQtYWxpZ246IGNlbnRlcjsiPjxkaXYgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzE5OTkveGh0bWwiIHN0eWxlPSJkaXNwbGF5OmlubGluZS1ibG9jazt0ZXh0LWFsaWduOmluaGVyaXQ7dGV4dC1kZWNvcmF0aW9uOmluaGVyaXQ7Ij48Zm9udCBjb2xvcj0iI2ZmZmZmZiIgc3R5bGU9ImZvbnQtc2l6ZTogMTAwcHgiPkVkaXQgRGlhZ3JhbTwvZm9udD48L2Rpdj48L2Rpdj48L2ZvcmVpZ25PYmplY3Q+PHRleHQgeD0iMjg5IiB5PSI2NSIgZmlsbD0iIzAwMDAwMCIgdGV4dC1hbmNob3I9Im1pZGRsZSIgZm9udC1zaXplPSIxMnB4IiBmb250LWZhbWlseT0iSGVsdmV0aWNhIj4mbHQ7Zm9udCBjb2xvcj0iI2ZmZmZmZiIgc3R5bGU9ImZvbnQtc2l6ZTogMTAwcHgiJmd0O0VkaXQgRGlhZ3JhbSZsdDsvZm9udCZndDs8L3RleHQ+PC9zd2l0Y2g+PC9nPjwvZz48L3N2Zz4=")
    dbSession.add(newLayout)
    dbSession.commit()
    return newLayout
