from sqlalchemy import *
from database.db import dbSession, init_db
from database.models import Picture
import os
from werkzeug.utils import secure_filename

directory = 'static/images'

def addPicture(root_path, pid, picture):
    """ Saves the image and adds the picture name to a related project """
    filename = secure_filename(picture.filename)
    absolutePath = os.path.join(root_path, directory, filename)

    # Save the image
    if picture.filename != '':
        print('File stored at: ' + absolutePath + '\n')
        picture.save(absolutePath)

        # Store filepath into the database
        newPicture = Picture(project_id = pid, path = filename)
        dbSession.add(newPicture)
        dbSession.commit()
        return True

    return False

def getPictures(pid):
    """ Returns a list of picture names to a related project """
    pictures = dbSession.query(Picture)
    pictures = pictures.filter(Picture.picture_id == pid).all()

    return pictures
