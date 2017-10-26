from sqlalchemy import *
from database.db import dbSession, init_db
from database.models import Picture

def addPicture(pid, image):
    """ Adds a new picture to a related project """
    newPicture = Picture(project_id = pid, image = image)

    dbSession.add(newPicture)
    dbSession.commit()

    return True

def getPictures(pid):
    """ Returns a list of pictures to a related project """
    pictures = dbSession.query(Picture)
    pictures = pictures.filter(Picture.picture_id == pid).all()

    return pictures
