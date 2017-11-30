from datetime import datetime
from database.models import Customer, Project, Company, Status, User, Quote, Picture, Material, Layout
from database.db import dbSession

def companyTestData():
    newCompany1 = Company(company_name = "Fence", email = "Fence@Fence.com")
    newCompany2 = Company(company_name = "Builder", email = "Build@Build.com")
    dbSession.add(newCompany1)
    dbSession.add(newCompany2)
    dbSession.commit()

def statusTestData():
    status1 = Status(status_name = "Not Reached", status_number = 1)
    status2 = Status(status_name = "In Progress", status_number = 2)
    status3 = Status(status_name = "Complete", status_number = 3)
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
    newProject1 = Project(customer_id = 1, status_name = 'Not Reached', address = 'Bear St', end_date = None, note = 'A fun fencing project', project_name = "Kat's house fence", company_name = 'Fence', project_id = 1, layout_selected = 1, appearance_selected = 1)
    newProject2 = Project(customer_id = 1, status_name = 'Not Reached', address = 'Grand Ave', end_date = None, note = 'Dog lives here', project_name = "Kat's second house fence", company_name = 'Fence', project_id = 2, layout_selected = 2, appearance_selected = 1)
    newProject3 = Project(customer_id = 3, status_name = 'Complete',  address = 'Park St', end_date = None, note = 'Concrete fence', project_name = "Jason's fence for company building", company_name = 'Fence', project_id = 3, layout_selected = 3, appearance_selected = 1)
    dbSession.add(newProject1)
    dbSession.add(newProject2)
    dbSession.add(newProject3)
    dbSession.commit()

def testLayoutData():
    newLayout1 = Layout(layout_id = 1, project_id = 1, layout_name = "Layout 1", layout_info = "TEXT")
    newLayout2 = Layout(layout_id = 2, project_id = 2, layout_name = "Test 2", layout_info = "TEXT")
    newLayout3 = Layout(layout_id = 3, project_id = 3, layout_name = "Test 3", layout_info = "TEXT")
    dbSession.add(newLayout1)
    dbSession.add(newLayout2)
    dbSession.add(newLayout3)
    dbSession.commit()

# Helper function for inserting user test data
def userTestData():
    newUser = User(id = 1, email = "Fern@Fencing.com", username = "KatUser", password = "password", company_name = "Fence", active = True)
    newUser1 = User(id = 2, email = "Bob@Builder.com", username = "aUser", password = "password", company_name = "Builder", active = True)
    newUser2 = User(id = 3, email = "Fae@Fencing.com", username = "aUser", password = "password", company_name = "Fence", active = False)
    newUser3 = User(id = 4, email = "Bill@Builder.com", username = "aUser", password = "password", company_name = "Builder", active = False)
    dbSession.add(newUser)
    dbSession.add(newUser1)
    dbSession.add(newUser2)
    dbSession.add(newUser3)
    dbSession.commit()

# Helper function for inserting quotes
def quoteTestData():
    newQuote = Quote(quote_id=2, project_id=1, amount=99439.12, amount_gst=100.00, amount_total=99539.12,
                     material_expense=123, material_expense_gst=52, material_expense_total=172, gst_rate=0.5)
    newQuote1 = Quote(quote_id=1, project_id=1, amount=105.12, amount_gst=10.00, amount_total=115.12,
                      material_expense=52.52, material_expense_gst=5.08, material_expense_total=57.60, gst_rate=0.5)
    newQuote2 = Quote(quote_id=3, project_id=1, amount=73.00, amount_gst=7.00, amount_total=80, material_expense=52.52,
                      material_expense_gst=5.08, material_expense_total=57.60, gst_rate=0.5)

    dbSession.add(newQuote)
    dbSession.add(newQuote1)
    dbSession.add(newQuote2)
    dbSession.commit()

# Helper function for inserting pictures
def pictureTestData():
    newPic = Picture(picture_id = 1, file_name = "garden.jpg", thumbnail_name = "thumbnail_garden.png", project_id = 1)
    newPic1 = Picture(picture_id = 2, file_name = "corner.jpg", thumbnail_name = "thumbnail_corner.png", project_id = 1)
    newPic2 = Picture(picture_id = 3, file_name = "backyard.png", thumbnail_name = "thumbnail_backyard.png", project_id = 2)
    dbSession.add(newPic)
    dbSession.add(newPic1)
    dbSession.add(newPic2)
    dbSession.commit()
