from datetime import datetime
from database.models import Customer, Project, Company, Status, User, Quote
from database.db import dbSession

def companyTestData():
    newCompany1 = Company(company_name = "Fence", email = "Fence@Fence.com")
    newCompany2 = Company(company_name = "Builder", email = "Build@Build.com")
    dbSession.add(newCompany1)
    dbSession.add(newCompany2)
    dbSession.commit()

def statusTestData():
    status1 = Status(status_name = "Not Reached")
    status2 = Status(status_name = "In Progress")
    status3 = Status(status_name = "Complete")
    dbSession.add(status1)
    dbSession.add(status2)
    dbSession.add(status3)
    dbSession.commit()

# Helper function for inserting customer test data
def customerTestData():
    newCustomer1 = Customer(customer_id = 1, first_name = 'Kat', email = 'Kat@gmail.com', cellphone = '541-689-4681', company_name = 'Fence')
    newCustomer2 = Customer(customer_id = 2, first_name = 'Davis', email = 'Davis@gmail.com', cellphone = '761-158-2113', company_name = 'Builder')
    newCustomer3 = Customer(customer_id = 3, first_name = 'Jason', email = 'Jason@gmail.com', cellphone = '688-946-8781', company_name = 'Fence')
    dbSession.add(newCustomer1)
    dbSession.add(newCustomer2)
    dbSession.add(newCustomer3)
    dbSession.commit()

# Helper function for inserting project test data
def projectTestData():
    newProject1 = Project(customer_id = 1, status_name = 'Not Reached', address = 'Bear St', end_date = None, note = 'A fun fencing project', project_name = "Kat's house fence", company_name = 'Fence', project_id = 1)
    newProject2 = Project(customer_id = 1, status_name = 'Not Reached', address = 'Grand Ave', end_date = None, note = 'Dog lives here', project_name = "Kat's second house fence", company_name = 'Fence', project_id = 2)
    newProject3 = Project(customer_id = 3, status_name = 'Complete',  address = 'Park St', end_date = None, note = 'Concrete fence', project_name = "Jason's fence for company building", company_name = 'Fence', project_id = 3)
    dbSession.add(newProject1)
    dbSession.add(newProject2)
    dbSession.add(newProject3)
    dbSession.commit()

# Helper function for inserting user test data
def userTestData():
    newUser = User(id = 1, email = "abc@abc.com", username = "KatUser", password = "password", company_name = "Fence", active = True)
    newUser1 = User(id = 2, email = "abc1@abc.com", username = "aUser", password = "password", company_name = "Fence", active = True)
    newUser2 = User(id = 3, email = "abc2@abc.com", username = "aUser", password = "password", company_name = "Fence", active = True)
    dbSession.add(newUser)
    dbSession.add(newUser1)
    dbSession.add(newUser2)
    dbSession.commit()

def quoteTestData():
    newQuote = Quote(quote_id = 1, project_id = 1, quote = 1500, project_info ='image1', note='noteeeeeeeeeee' )
    newQuote1 = Quote(quote_id = 2, project_id = 1, quote = 1700, project_info ='image1', note='This is note the same')
    newQuote2 = Quote(quote_id = 3, project_id = 2, quote = 2500, project_info ='image1', note='noteeeeeeeeeee')    
    dbSession.add(newQuote)
    dbSession.add(newQuote1)
    dbSession.add(newQuote2)
    dbSession.commit()
