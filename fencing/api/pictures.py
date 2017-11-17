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

# https://stackoverflow.com/questions/8631076/what-is-the-fastest-way-to-generate-image-thumbnails-in-python
from PIL import Image

# TODO: Clean code and refactor. Maybe there is a better way to handle different file extensions?
thumbnailDir = os.path.join('static', 'images', 'thumbnails')
thumbnailPrefix = 'tbn_'
thumbnailExt = '.png'
thumbnailSize = (128, 128)
pictureDir = os.path.join('static', 'images', 'pictures')

pictureBlueprint = Blueprint('pictureBlueprint', __name__, template_folder='templates')
app_root = ''

@pictureBlueprint.route('/getPictureList/<int:project_id>', methods=['GET'])
#@login_required
#@roles_required('primary')
def getPictureList(project_id):
    """ Returns a list of pictures for a given project id"""
    if request.method == 'GET':
        pictures = dbSession.query(Picture)
        pictures = pictures.filter(Picture.project_id == project_id).order_by(desc(Picture.upload_date)).all()
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

        filename = secure_filename(picture.filename)
        filename, file_extension = os.path.splitext(filename)
        if filename != '':
            try:
                # Store filepath into the database
                newPicture = Picture(project_id = project_id,
                    file_name = filename + file_extension,
                    thumbnail_name = thumbnailPrefix + filename + thumbnailExt)
                dbSession.add(newPicture)

                # Save picture in the picture directory
                picturePath = os.path.join(app_root, pictureDir, filename + file_extension)
                print('Picture stored at: ' + picturePath + '\n')
                picture.save(picturePath)

                # Create thumbnail of picture
                thumb = Image.open(picturePath)
                thumb.thumbnail(thumbnailSize)

                background = Image.new('RGBA', thumbnailSize, (255, 255, 255, 0))
                background.paste(
                    thumb, (int((thumbnailSize[0] - thumb.size[0]) / 2),
                            int((thumbnailSize[1] - thumb.size[1]) / 2))
                )

                # Save thumbnail in the thumbnail directory
                thumbnailPath = os.path.join(app_root, thumbnailDir,
                    thumbnailPrefix + filename + thumbnailExt)
                print('Thumbnail stored at: ' + thumbnailPath + '\n')
                background.save(thumbnailPath)
                background.close()
                thumb.close()

                # Commit and return ok status
                dbSession.commit()
                return created_request("Picture was uploaded")
            except:
                return bad_request("Invalid project id or an error when saving the file has occured")
        return bad_request("No file provided")
