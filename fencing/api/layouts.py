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

layoutBlueprint = Blueprint('layoutBlueprint', __name__, template_folder='templates')

@layoutBlueprint.route('/getLayoutList/<int:project_id>', methods=['GET'])
#@login_required
#@roles_required('primary')
def getLayoutList(project_id):
    """ Returns a list of layouts of a given project id """
    pass

@layoutBlueprint.route('/getLayout/<int:layout_id>', methods=['GET'])
#@login_required
#@roles_required('primary')
def getLayout(layout_id):
	""" Returns a layout of the given layout id """
	pass

@layoutBlueprint.route('/updateLayout/<int:layout_id>', methods=['pass'])
#@login_required
#@roles_required('primary')
def updateLayout(layout_id):
	""" Returns a layout of the given layout id """
	pass

def getLayoutHelper(project_id):
#TODO: function should be renamed in the future for clarity purposes
	layouts = dbSession.query(Layout).filter(Layout.project_id == project_id).all()
	json_response = [i.serialize for i in layouts]
	return json_response

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
    print(layout_id)
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
