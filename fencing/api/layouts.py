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
import math

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

@layoutBlueprint.route('/getMaterialAmounts/', methods = ['GET'])
@login_required
@roles_required('primary')
def getMaterialAmounts():
    if request.method == 'GET':
        layout_id = request.args.get('layout_id')
        layout = dbSession.query(Layout).filter(Layout.layout_id == layout_id).one()
        if layout is None:
            return bad_request('Layout does not exist')
        return jsonify(getMaterialAmount(layout))
    return bad_request('Request is not a GET request')

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

def getMaterialAmount(layout):
    parsed = DiagramParser.parse(layout.layout_info)
    print(parsed)

    num_t_post, num_corner_post, num_line_post, num_end_post, num_gate_posts, num_steel_post = posts(parsed)
    print('\n')
    num_caps = num_steel_post
    num_collars = num_steel_post * 2

    num_small_sections, num_medium_sections, num_big_sections, num_sections = sections(parsed)
    num_uchannel = num_sections * 2
    num_metal_uchannel = num_medium_sections + num_big_sections
    num_rails = num_sections * 2
    num_panels = panels(parsed)

    num_hinges, num_latches, num_Lsteel = gates(parsed)

    print('\nSteel')
    print('Metal Post: ',num_steel_post)
    print('Metal U-Channel: ', num_metal_uchannel)
    print('Metal L-Steel', num_Lsteel)
    print('\nPlastic Posts')
    print('Plastic T-Post', num_t_post)
    print('Plastic Corner-Post', num_corner_post)
    print('Plastic Line-Post', num_line_post)
    print('Plastic End-Post', num_end_post)
    print('Plastic Gate-Post', num_gate_posts)
    print('\nPlastic')
    print('Plastic Rails', num_rails)
    print('Plastic U-Channel',num_uchannel)
    print('Plastic T&G (Panels)',num_panels)
    print('Plastic Collars', num_collars)
    print('Plastic Caps',num_caps)
    print('\nGate')
    print('Hinges',num_hinges)
    print('Latches',num_latches)

    return {
            'metal_post'            : num_steel_post,
            'metal_u_channel'       : num_metal_uchannel,
            'metal_lsteel'          : num_Lsteel,
            'plastic_t_post'        : num_t_post,
            'plastic_corner_post'   : num_corner_post,
            'plastic_line_post'     : num_line_post,
            'plastic_end_post'      : num_end_post,
            'plastic_gate_posts'    : num_gate_posts,
            'plastic_rail'          : num_rails,
            'plastic_u_channel'     : num_uchannel,
            'plastic_panel'         : num_panels,
            'plastic_collar'        : num_collars,
            'plastic_cap'           : num_caps,
            'gate_hinge'            : num_hinges,
            'gate_latch'            : num_latches
        }

def posts(parsed):
    num_t_post = 0
    num_corner_post = 0
    num_line_post = 0
    num_end_post = 0
    num_gate_posts = 0
    for post in parsed.posts():
        if not post.isRemoval:
            if post.postType == 'tPost':
                num_t_post += 1
            if post.postType == 'cornerPost':
                num_corner_post += 1
            if post.postType == 'endPost':
                num_end_post += 1
            if post.postType == 'gatePost':
                num_gate_posts += 1

    for fence in parsed.fences:
        if not fence.isRemoval:
            if (fence.length/12) % 8 == 0:
                num_line_post += (fence.length/12) // 8 - 1
            else:
                num_line_post += (fence.length/12) // 8
    num_steel_post = num_t_post + num_corner_post + num_line_post + num_end_post + num_gate_posts
    return num_t_post, num_corner_post, num_line_post, num_end_post, num_gate_posts, num_steel_post

def sections(parsed):
    num_small_sections = 0
    num_medium_sections = 0
    num_big_sections = 0
    for fence in parsed.fences:
        if not fence.isRemoval:
            num_big_sections += (fence.length/12) // 8
            if (fence.length/12) % 8 < 6 and (fence.length/12) % 8 > 0:
                num_small_sections += 1
            if (fence.length/12) % 8 > 6:
                num_medium_sections += 1
    num_sections = num_small_sections + num_medium_sections + num_big_sections
    return num_small_sections, num_medium_sections, num_big_sections, num_sections

def panels(parsed):
    num_panels = 0
    for fence in parsed.fences:
        num_panels += math.ceil(fence.length/12)
    return num_panels

def gates(parsed):
    num_hinges = 0
    num_latches = 0
    num_Lsteel = 0
    for gate in parsed.gates:
        if not gate.isRemoval:
            num_Lsteel += 1
            num_latches += 1
            if gate.isDouble:
                num_hinges += 2
            else:
                num_hinges += 1
    return num_hinges, num_latches, num_Lsteel
