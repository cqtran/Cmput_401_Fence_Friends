from sqlalchemy import *
from database.db import dbSession, init_db
from database.models import Project, Quote

def getProject(project_id):
    """ Returns the project of the given project id """
    project = dbSession.query(Project)
    project = project.filter(Project.project_id == project_id).all()
    json_response = [i.serialize for i in project]
    return json_response

def getCompanyProjects(companyName):
    pass

def updateProjectInfo(project_id, project_name, address, status, note):
    """ Updates the project information of a given project id """
    project = dbSession.query(Project).filter(Project.project_id == project_id).all()

    project[0].project_name = project_name
    project[0].address = address
    project[0].status = status
    project[0].note = note

    dbSession.commit()
    return True

def createProject(customerId, statusName, address, companyName, project_name):
    #Access MySQL and add in account
    newProject = Project(customer_id = customerId, address = address,
            status_name = statusName, end_date = None, note = '',
            project_name = project_name, company_name = companyName)

    dbSession.add(newProject)
    dbSession.commit()
    newQuote = Quote(project_id = newProject.project_id, quote = 0 , project_info = "data:image/png;base64,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vil3YywEIGCdAKJvPQKwHwIQMEVgQIr+xx9/HDnxs88+i/53jjnmMOVUjIUABCCQRmBAiP706dPdbbfd5q699lp30UUXNdj6la98xR188MFuu+22c8svv3xmNDz77LPuzTffdIIz55xzuqWXXrruO//617/ce++9F32utpdaaqnMNlup8NhjjzndwHTzWmSRRdzgwYNbaSb3dx544AH32muvRXYNGjTIrbLKKrm/S0UIQKAaBCot+u+884779a9/7caNG5eb9rbbbutOOeUUt9hii6V+Z8cdd3SXX3559Pm3v/1td+utt7oZZ5yxVj/r89ydaVLx/fffdyuuuKJ75plnolrjx493Y8eOLaPplu3u6MVpHAIQ6AqByor+E0884dZff3336quvtgTqiiuucFtvvXXid3/84x+7008/Pfpshx12cJdeeqn70pe+VKub9XlLHQq+9NFHH7k111zT/fOf/4w+OeOMM9z+++9fRtOpbXTDro4a0CON6ynx7LPPjp4S3333XTdy5Ei3+OKL90jv6EYaASt+q6ToS/CXW265RN8dcMABbsMNN3TzzDOP++CDD5xSMXoSSLo5KB20+eabN7Tji9/3v/99d9VVV9WJ/l577eV+//vfR9/T51deeWXdk0AZP6v+Fv0ku8uwy0IbYXzed999brXVVrNgeqVttOK3yom+cs4aAcdpjzjKJPZHHXWUW2CBBRID76abbnK77rprnfir7iOPPNKQK88SfQm+RuAa/S+77LJun332ifLgZRZEv0ya3W3rqaeecssss0ztooh+d/m3ejUrfquc6B9++OHuxBNPrPPrH//4R6c8e1Z56623opRQnDJR/T333NOde+65daKdJfpZ1ynjc0S/DIr904YV8egfup27qhW/VUr0n3vuObfEEkvUef0vf/mL22abbXJHgkZda6yxRq2+RvtTp051888/f+1viP7/0lZhWis3ZOMVwzh9+OGH3UorrWScSu+bb8VvlRL9k046yR122GG16Gkln/7FF1+47373u9ESz7jcc889UcooLlmi/9JLL0XzBSqzzjqrW3jhhVMjWsstJ0+e7C655BJ34403RnU1olhvvfXcFlts4TbbbLNoOWZYio70laaSbSq6pm5iRScPk+zu6+tz//jHP9ykSZPck08+GU1MfvWrX3Urr7yyGz58eCExU2pODO64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"
                     , note = "")
    dbSession.add(newQuote)
    dbSession.commit()

    return True

def getdrawiopic(project_id):
    #TODO: function should be renamed in the future for clarity purposes
    getpic = dbSession.query(Quote).filter(Quote.project_id == project_id).all()
    json_response = [i.serialize for i in getpic]
    return json_response

def updatedrawiopic(quote_id, quote, project_info, note):
    # ERIC PLEASE HELP
    #TODO: function should be renamed in the future for clarity purposes
    quotation = dbSession.query(Quote)
    quotation = quotation.filter(Quote.quote_id == quote_id).all()
    quotation[0].quote = quote
    quotation[0].projectinfo = projectinfo
    quotation[0].note = note
    dbSession.commit()
    return True

def savenote(note, pid):
    """Save the given note to the database"""
    #CHANGED: savenote function may be deprecated
    project = dbSession.query(Project)
    project = project.filter(Project.project_id == pid).all()
    project[0].note = note
    dbSession.commit()
    #savenoteintoserver = update(Project).where(Project.project_id == pid).values(Note = note)

    return True
