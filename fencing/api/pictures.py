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
import uuid
# https://stackoverflow.com/questions/8631076/what-is-the-fastest-way-to-generate-image-thumbnails-in-python
from PIL import Image


"""Api for picture handling and uploading"""


# TODO: Clean code and refactor. Maybe there is a better way to handle different file extensions?
thumbnailDir = os.path.join('static', 'images', 'thumbnails')
thumbnailPrefix = 'tbn_'
thumbnailExt = '.png'
thumbnailSize = (128, 128)
pictureDir = os.path.join('static', 'images', 'pictures')

pictureBlueprint = Blueprint('pictureBlueprint', __name__, template_folder='templates')
app_root = ''

@pictureBlueprint.route('/getPictureList/<int:project_id>', methods=['GET'])
@login_required
@roles_required('primary')
def getPictureList(project_id):
    """ Returns a list of pictures for a given project id"""
    if request.method == 'GET':
        pictures = dbSession.query(Picture)
        pictures = pictures.filter(Picture.project_id == project_id).order_by(desc(Picture.upload_date)).all()
        if len(pictures) == 0:
            return bad_request("No pictures were found for this project")
        return jsonify(pictures)

@pictureBlueprint.route('/uploadPicture/', methods = ['POST'])
@login_required
@roles_required('primary')
def uploadPicture():
    """ Saves the image and adds the picture name to a related project """
    if request.method == 'POST':
        project_id = request.form['proj_id']
        picture = request.files['picture']
        # Parse file type and file name
        filename = secure_filename(picture.filename)
        filename, file_extension = os.path.splitext(filename)
        if filename != '':
            # Generate a unique file name to store the file
            filename = str(uuid.uuid4())
            try:
                # Store filepath into the database
                newPicture = Picture(project_id = project_id,
                    file_name = filename + file_extension,
                    thumbnail_name = thumbnailPrefix + filename + thumbnailExt)
                dbSession.add(newPicture)

                # Save picture in the picture directory
                picturePath = os.path.join(app_root, pictureDir, filename + file_extension)
                picture.save(picturePath)

                # Create thumbnail of picture
                thumb = Image.open(picturePath)

                # Source: javiergodinez.blogspot.ca/2008/03/square-thumbnail-with-python-image.html
                width, height = thumb.size

                if width > height:
                   delta = width - height
                   left = int(delta/2)
                   upper = 0
                   right = height + left
                   lower = height
                else:
                   delta = height - width
                   left = 0
                   upper = int(delta/2)
                   right = width
                   lower = width + upper

                thumb = thumb.crop((left, upper, right, lower))
                thumb.thumbnail(thumbnailSize, Image.ANTIALIAS)

                # Save thumbnail in the thumbnail directory
                thumbnailPath = os.path.join(app_root, thumbnailDir,
                    thumbnailPrefix + filename + thumbnailExt)
                thumb.save(thumbnailPath)
                thumb.close()

                # Commit and return ok status
                dbSession.commit()
                return created_request("Picture was uploaded")
            except:
                return bad_request("Invalid project id or an error when saving the file has occured")
        return bad_request("No file provided")

@pictureBlueprint.route('/deletePicture/', methods = ['DELETE'])
@login_required
@roles_required('primary')
def deletePicture():
    """Deletes picture when user presses button"""
    if request.method == 'DELETE':
        # Grab arguments
        filename = request.args.get('picName')
        project_id = request.args.get('proj_id')
        if filename != '':
            # Query and find the picture in the database
            picToDelete = dbSession.query(Picture).filter(Picture.project_id == project_id)
            picToDelete = picToDelete.filter(Picture.file_name == filename)

            picFilenames = picToDelete.all()
            if len(picFilenames) == 0:
                return bad_request("Invalid picture name or project id")

            # Delete picture and thumbnail files
            deleteImageHelper(picFilenames[0].file_name)
            deleteImageHelper(picFilenames[0].thumbnail_name)

            # Remove picture from database
            picToDelete.delete()
            dbSession.commit()
        return "{}"

def deleteImageHelper(image_filename):
    """ Deletes the given image of the filename. It will change directory
     depending on if the filename has the thumbnail prefix or not"""
    directory = ""
    if image_filename.startswith(thumbnailPrefix):
        # filename is a thumbnail
        directory = thumbnailDir
    else:
        # filename is a picture
        directory = pictureDir
    try:
        # remove the file if it exists
        filePath = os.path.join(app_root, directory, image_filename)
        os.remove(filePath)
    except:
        print('Could not delete image at: ' + filePath)
    return
