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
    newLayout = Layout(project_id = project_id, layout_name = "Layout 1", layout_info = "data:image/svg+xml;base64,PCFET0NUWVBFIHN2ZyBQVUJMSUMgIi0vL1czQy8vRFREIFNWRyAxLjEvL0VOIiAiaHR0cDovL3d3dy53My5vcmcvR3JhcGhpY3MvU1ZHLzEuMS9EVEQvc3ZnMTEuZHRkIj4KPHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHhtbG5zOnhsaW5rPSJodHRwOi8vd3d3LnczLm9yZy8xOTk5L3hsaW5rIiB3aWR0aD0iNzAxcHgiIGhlaWdodD0iMzIxcHgiIHZlcnNpb249IjEuMSIgY29udGVudD0iJmx0O214ZmlsZSB1c2VyQWdlbnQ9JnF1b3Q7TW96aWxsYS81LjAgKE1hY2ludG9zaDsgSW50ZWwgTWFjIE9TIFggMTBfMTNfMSkgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgQ2hyb21lLzYxLjAuMzE2My4xMDAgU2FmYXJpLzUzNy4zNiZxdW90OyB2ZXJzaW9uPSZxdW90OzcuNi43JnF1b3Q7IGVkaXRvcj0mcXVvdDt3d3cuZHJhdy5pbyZxdW90OyZndDsmbHQ7ZGlhZ3JhbSBpZD0mcXVvdDtiYTZlNmZlZS1hNTU4LTljODgtMjM1Ny1jMGUyZWYxZGM1OGEmcXVvdDsgbmFtZT0mcXVvdDtQYWdlLTEmcXVvdDsmZ3Q7ZGRIQkVvSWdFQURRcitHT1VFMmV6ZXJTeVVObkVsUW1aQjNFMGZyNk5EQmpMQzdBMjEyV0FVU1RlamdaMWxRWDRFSWhndm1BNkFFUkV0RjRNMDZUUEp6RThjNUJhU1QzU1F0azhpazhZcStkNUtJTkVpMkFzcklKTVFldFJXNmQrVnBtRFBSdFFBV29zR3ZEU3JHQ0xHZHFyVmZKYmVWMHY4V0xuNFVzSzk4NWlyQ1AzRmgrTHcxMDJ2ZERoQmJ2NGNJMW04L3krVzNGT1BSZlJGTkVFd05nM2FvZUVxR210NTJmemRVZC8wUS85elpDMng4RjQySTVlOXdFSDBqVEZ3PT0mbHQ7L2RpYWdyYW0mZ3Q7Jmx0Oy9teGZpbGUmZ3Q7IiBzdHlsZT0iYmFja2dyb3VuZC1jb2xvcjogcmdiKDI1NSwgMjU1LCAyNTUpOyI+PGRlZnMvPjxnIHRyYW5zZm9ybT0idHJhbnNsYXRlKDAuNSwwLjUpIj48cmVjdCB4PSIwIiB5PSIwIiB3aWR0aD0iNzAwIiBoZWlnaHQ9IjMyMCIgcng9IjQ4IiByeT0iNDgiIGZpbGwtb3BhY2l0eT0iMC42NiIgZmlsbD0iIzMyOTY2NCIgc3Ryb2tlPSJub25lIiBwb2ludGVyLWV2ZW50cz0ibm9uZSIvPjxnIHRyYW5zZm9ybT0idHJhbnNsYXRlKDYwLjUsMTAwLjUpIj48c3dpdGNoPjxmb3JlaWduT2JqZWN0IHN0eWxlPSJvdmVyZmxvdzp2aXNpYmxlOyIgcG9pbnRlci1ldmVudHM9ImFsbCIgd2lkdGg9IjU3OCIgaGVpZ2h0PSIxMTgiIHJlcXVpcmVkRmVhdHVyZXM9Imh0dHA6Ly93d3cudzMub3JnL1RSL1NWRzExL2ZlYXR1cmUjRXh0ZW5zaWJpbGl0eSI+PGRpdiB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMTk5OS94aHRtbCIgc3R5bGU9ImRpc3BsYXk6IGlubGluZS1ibG9jazsgZm9udC1zaXplOiAxMnB4OyBmb250LWZhbWlseTogSGVsdmV0aWNhOyBjb2xvcjogcmdiKDAsIDAsIDApOyBsaW5lLWhlaWdodDogMS4yOyB2ZXJ0aWNhbC1hbGlnbjogdG9wOyB3aWR0aDogNTc4cHg7IHdoaXRlLXNwYWNlOiBub3dyYXA7IHdvcmQtd3JhcDogbm9ybWFsOyB0ZXh0LWFsaWduOiBjZW50ZXI7Ij48ZGl2IHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8xOTk5L3hodG1sIiBzdHlsZT0iZGlzcGxheTppbmxpbmUtYmxvY2s7dGV4dC1hbGlnbjppbmhlcml0O3RleHQtZGVjb3JhdGlvbjppbmhlcml0OyI+PGZvbnQgY29sb3I9IiNmZmZmZmYiIHN0eWxlPSJmb250LXNpemU6IDEwMHB4Ij5FZGl0IERpYWdyYW08L2ZvbnQ+PC9kaXY+PC9kaXY+PC9mb3JlaWduT2JqZWN0Pjx0ZXh0IHg9IjI4OSIgeT0iNjUiIGZpbGw9IiMwMDAwMDAiIHRleHQtYW5jaG9yPSJtaWRkbGUiIGZvbnQtc2l6ZT0iMTJweCIgZm9udC1mYW1pbHk9IkhlbHZldGljYSI+Jmx0O2ZvbnQgY29sb3I9IiNmZmZmZmYiIHN0eWxlPSJmb250LXNpemU6IDEwMHB4IiZndDtFZGl0IERpYWdyYW0mbHQ7L2ZvbnQmZ3Q7PC90ZXh0Pjwvc3dpdGNoPjwvZz48L2c+PC9zdmc+")
    dbSession.add(newLayout)
    dbSession.commit()
    return newLayout
