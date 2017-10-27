from sqlalchemy import *
from database.db import dbSession, init_db
from database.models import Picture
import os
from werkzeug.utils import secure_filename

def addPicture(root_path, pid, picture):
    """ Saves the image and adds the picture path to a related project """

    picturePath = os.path.join(root_path, 'database/images', secure_filename(picture.filename))

    # Save the image
    if picture.filename != '':
        print(picturePath)
        picture.save(picturePath)

        # Store filepath into the database
        #newPicture = Picture(project_id = pid, path = picturePath)
        #dbSession.add(newPicture)
        #dbSession.commit()
        return True

    return False

def getPictures(pid):
    """ Returns a list of paths to pictures to a related project """
    pictures = dbSession.query(Picture)
    pictures = pictures.filter(Picture.picture_id == pid).all()

    return pictures
