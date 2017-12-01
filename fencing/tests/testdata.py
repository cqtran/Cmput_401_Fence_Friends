from datetime import datetime
from database.models import Customer, Project, Company, Status, User, Quote, Picture, Material, Layout, Appearance, Style, Colour, Height, Gate
from database.db import dbSession


def companyTestData():
    newCompany1 = Company(company_name = "Fence", email = "Fence@Fence.com")
    newCompany2 = Company(company_name = "Builder", email = "Build@Build.com")
    dbSession.add(newCompany1)
    dbSession.add(newCompany2)
    dbSession.commit()

def statusTestData():
    status1 = Status(status_name = "Not Reached", status_number = 1)
    status2 = Status(status_name = "Paid", status_number = 2)
    status3 = Status(status_name = "Appraisal Booked", status_number = 3)
    dbSession.add(status1)
    dbSession.add(status2)
    dbSession.add(status3)
    dbSession.commit()

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

    newProject1 = Project(customer_id = 1, status_name = 'Not Reached', address = 'Bear St', end_date = None , note = 'A fun fencing project', project_name = "Kat's house fence", company_name = 'Fence', layout_selected = None, appearance_selected = None, project_id = 1 )
    newProject2 = Project(customer_id = 1, status_name = 'Not Reached', address = 'Grand Ave', end_date = None, note = 'Dog lives here', project_name = "Kat's second house fence", company_name = 'Fence',layout_selected = None, appearance_selected = None, project_id = 2 )
    #newProject3 = Project(customer_id = 3, status_name = 'Complete',  address = 'Park St', end_date = None, note = 'Concrete fence', project_name = "Jason's fence for company building", company_name = 'Fence', project_id = 3, layout_selected = 3, appearance_selected = 1)
    dbSession.add(newProject1)
    dbSession.add(newProject2)
    #dbSession.add(newProject3)
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

# Helper function for inserting quotes
def quoteTestData():
    newQuote = Quote(quote_id=2, project_id=1, amount=99439.12, amount_gst=100.00, amount_total=99539.12,
                     material_expense=123, material_expense_gst=52, material_expense_total=172, gst_rate=0.5)
    newQuote1 = Quote(quote_id=1, project_id=1, amount=105.12, amount_gst=10.00, amount_total=115.12,
                      material_expense=52.52, material_expense_gst=5.08, material_expense_total=57.60, gst_rate=0.5)
    newQuote2 = Quote(quote_id=3, project_id=2, amount=73.00, amount_gst=7.00, amount_total=80, material_expense=52.52,
                      material_expense_gst=5.08, material_expense_total=57.60, gst_rate=0.5)
    newQuote3 = Quote(quote_id=4, project_id=1, amount=105.12, amount_gst=10.00, amount_total=116.12,
                      material_expense=52.52, material_expense_gst=5.08, material_expense_total=57.60, gst_rate=0.5)

    dbSession.add(newQuote)
    dbSession.add(newQuote1)
    dbSession.add(newQuote2)
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


def testLayoutData():
    newLayout1 = Layout(layout_id = 1, project_id = 1, layout_name = "Layout 1", layout_info = "test")
    newLayout2 = Layout(layout_id = 2, project_id = 2, layout_name = "Layout 2", layout_info = "test")
    newLayout3 = Layout(layout_id = 3, project_id = 1, layout_name = "Layout 3", layout_info = "test")
    dbSession.add(newLayout1)
    dbSession.add(newLayout2)
    dbSession.add(newLayout3)

# Helper function for inserting quotes
def quoteTestData():
    newQuote = Quote(quote_id = 2, project_id = 1, amount = 99439.12 , amount_gst = 100.00, amount_total = 99539.12, material_expense = 123, material_expense_gst = 52, material_expense_total = 172, gst_rate = 0.5)
    newQuote1 = Quote(quote_id = 1, project_id = 1, amount = 105.12 , amount_gst = 10.00, amount_total = 115.12, material_expense = 52.52, material_expense_gst = 5.08, material_expense_total = 57.60, gst_rate = 0.5)
    newQuote2 = Quote(quote_id = 3, project_id = 1, amount = 73.00 , amount_gst = 7.00, amount_total = 80, material_expense = 52.52, material_expense_gst = 5.08, material_expense_total = 57.60, gst_rate = 0.5)
    dbSession.add(newQuote)
    dbSession.add(newQuote1)
    dbSession.add(newQuote2)
    dbSession.commit()


def testMaterialData():

    newMaterial1 = Material(material_name = 'WPR6C* Pocket Rail 1.5"x 71.5" Clay' , my_price = 18.37, pieces_in_bundle = 144, category = "Privacy Fence Rails",
                           note = "Clay", company_name = "Fence", material_id = 1)
    newMaterial2 = Material(material_name = "875U.16A .875x16' U Channel Almond" , my_price = 13.16, pieces_in_bundle = 36, category = "U-Channel (Plastic)",
                           note = "Almond", company_name = "Fence", material_id = 2)
    newMaterial3 = Material(material_name = 'APSB4 4 x 1-7/8" Post Collar Adapter" 2pc', my_price = 4.75, pieces_in_bundle = 150, category = "Collars",
                           note = "Adapter", company_name = "Fence", material_id = 3)
    newMaterial4 = Material(material_name = 'HSSDR36 36 Stainless Steel Drop Rod Black', my_price = 37.98, pieces_in_bundle = 6, category = "Gate Hardware",
                           note = "Stainless Steel", company_name = "Fence", material_id = 4)
    newMaterial5 = Material(material_name = 'GAAKA Gate Assembly Kit -Almond ', my_price = 7.00, pieces_in_bundle = 1, category = "Gates",
                           note = "issa gate", company_name = "Fence", material_id = 5)
    newMaterial6 = Material(material_name = 'ABLOCK THE BLOCK" Vinyl post pounding block"', my_price = 52.50, pieces_in_bundle = 1, category = "Accessories",
                           note = "Its a pounding block", company_name = "Fence", material_id = 6)
    newMaterial7 = Material(material_name = 'Cap235FA 2x3.5" Flat Cap Almond', my_price = 1.13, pieces_in_bundle = 100, category = "Caps",
                           note = "cappa", company_name = "Fence", material_id = 7)
    newMaterial8 = Material(material_name = 'W55.A* 5x5"x54" Post Almond', my_price = 19.36, pieces_in_bundle = 72, category = "Ranch Rail",
                           note = "ranch sauce", company_name = "Fence", material_id = 8)


    dbSession.add(newMaterial1)
    dbSession.add(newMaterial2)
    dbSession.add(newMaterial3)
    dbSession.add(newMaterial4)
    dbSession.add(newMaterial5)
    dbSession.add(newMaterial6)
    dbSession.add(newMaterial7)
    dbSession.add(newMaterial8)
    dbSession.commit()

def testEstimateData():

    # STYLE, COLOUR, HEIGHT, GATE

    newStyle = Style(style = "Full Privacy", value = 40, company_name = None, style_id = 1 )
    newColor = Colour(colour = "White", value = 0, company_name = None, colour_id = 1)
    newHeight = Height(height = "6", value = 0, company_name = None, height_id = 1)
    newGate = Gate(gate = "Man gate 4'", value = 550, company_name = None, gate_id = 1)

    newStyle1 = Style(style = "Picket Top", value = 44, company_name = None, style_id = 2 )
    newColor1 = Colour(colour = "Almond (Tan)", value = 4, company_name = None, colour_id = 2)
    newHeight1 = Height(height = "5", value = -3, company_name = None, height_id = 2)
    newGate1 = Gate(gate = "RV gate 12'", value = 1300, company_name = None, gate_id = 2)

    newStyle2 = Style(style = "Lattice Top", value = 44, company_name = None, style_id = 3 )
    newColor2 = Colour(colour = "Clay", value = 8, company_name = None, colour_id = 3)
    newHeight2 = Height(height = "4", value = -3, company_name = None, height_id = 3)

    newStyle3 = Style(style = "Picket Fence", value = 40, company_name = None, style_id = 4 )
    newColor3 = Colour(colour = "Pebblestone", value = 4, company_name = None, colour_id = 4)
    newHeight3 = Height(height = "3", value = -6, company_name = None, height_id = 4)

    dbSession.add(newStyle)
    dbSession.add(newColor)
    dbSession.add(newHeight)
    dbSession.add(newGate)

    dbSession.add(newStyle1)
    dbSession.add(newColor1)
    dbSession.add(newHeight1)
    dbSession.add(newGate1)

    dbSession.add(newStyle2)
    dbSession.add(newColor2)
    dbSession.add(newHeight2)

    dbSession.add(newStyle3)
    dbSession.add(newColor3)
    dbSession.add(newHeight3)

    dbSession.commit()

def testAppearanceData():

    appearance = Appearance(appearance_name = 'Appearance', project_id = 1, panel_gap = 0.5, height = 0.5, appearance_id = 1 )
    appearance1 = Appearance(appearance_name='Appearance1', project_id=1, panel_gap=0.6, height=6, appearance_id=2)
    appearance2 = Appearance(appearance_name='Appearance2', project_id=1, panel_gap=0.7, height=9, appearance_id=3)
    appearance3 = Appearance(appearance_name = 'Appearance3', project_id = 2, panel_gap = 0.8, height = 12, appearance_id = 4 )
    appearance4 = Appearance(appearance_name = 'Appearance4', project_id = 2, panel_gap = 0.9, height = 13, appearance_id = 5 )

    dbSession.add(appearance)
    dbSession.add(appearance1)
    dbSession.add(appearance2)
    dbSession.add(appearance3)
    dbSession.add(appearance4)

    dbSession.commit()


