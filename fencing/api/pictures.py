from sqlalchemy import *
from database.db import dbSession, init_db
from database.models import Picture
import os
from werkzeug.utils import secure_filename

from flask import Blueprint, request
from flask.json import jsonify
from flask_security.core import current_user
from flask_security import login_required
from flask_security.decorators import roles_required
from api.errors import bad_request

directory = os.path.join('static', 'images')

pictureBlueprint = Blueprint('pictureBlueprint', __name__, template_folder='templates')

@pictureBlueprint.route('/getPictureList/<int:project_id>', methods=['GET'])
#@login_required
#@roles_required('primary')
def getPictureList(project_id):
    """ Returns a list of pictures for a given project id"""
    if request.method == 'GET':
        pictures = dbSession.query(Picture)
        pictures = pictures.filter(Picture.project_id == project_id).all()
        if len(pictures) == 0:
            return bad_request("No pictures were found for this project")
        return jsonify(pictures)

def addPicture(root_path, pid, picture):
    """ Saves the image and adds the picture name to a related project """
    filename = secure_filename(picture.filename)
    absolutePath = os.path.join(root_path, directory, filename)

    # Save the image
    if picture.filename != '':
        print('File stored at: ' + absolutePath + '\n')
        picture.save(absolutePath)

        # Store filepath into the database
        newPicture = Picture(project_id = pid, file_name = filename)
        dbSession.add(newPicture)
        dbSession.commit()
        return True

    return False
