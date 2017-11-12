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
from api.errors import *
# May be required in the future for thumbnail creation
# https://stackoverflow.com/questions/8631076/what-is-the-fastest-way-to-generate-image-thumbnails-in-python
#from PIL import Image

directory = os.path.join('static', 'images')

pictureBlueprint = Blueprint('pictureBlueprint', __name__, template_folder='templates')
app_root = ''

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

@pictureBlueprint.route('/uploadPicture/', methods = ['POST'])
#@login_required
#@roles_required('primary')
def uploadPicture():
    """ Saves the image and adds the picture name to a related project """
    if request.method == 'POST':
        project_id = request.form['proj_id']
        picture = request.files['picture']

        # Store the picture in the database
        # TODO: Create and save a thumbnail for each picture
        filename = secure_filename(picture.filename)

        if picture.filename != '':
            try:
                absolutePath = os.path.join(app_root, directory, filename)
                # Store filepath into the database
                newPicture = Picture(project_id = project_id, file_name = filename)
                dbSession.add(newPicture)
                dbSession.commit()

                print('File stored at: ' + absolutePath + '\n')
                picture.save(absolutePath)

                return created_request("Picture was uploaded")
            except:
                return bad_request("Invalid project id")
        return bad_request("No file provided")
