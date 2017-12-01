from datetime import datetime
from database.models import Customer, Project, Company, Status, User, Quote, Picture, Material, Layout, Appearance
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

    #appearance = Appearance(appearance_name = 'yes', project_id = 1, panel_gap = 0.5, height = 0.5, appearance_id = 1 )
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
    newQuote2 = Quote(quote_id=3, project_id=1, amount=73.00, amount_gst=7.00, amount_total=80, material_expense=52.52,
                      material_expense_gst=5.08, material_expense_total=57.60, gst_rate=0.5)

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

'''
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
    newLayout1 = Layout(layout_id = 1, project_id = 1, layout_name = "Layout 1", layout_info = "data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHhtbG5zOnhsaW5rPSJodHRwOi8vd3d3LnczLm9yZy8xOTk5L3hsaW5rIiB3aWR0aD0iNzAxcHgiIGhlaWdodD0iMzIxcHgiIHZlcnNpb249IjEuMSIgY29udGVudD0iJmx0O214ZmlsZSB1c2VyQWdlbnQ9JnF1b3Q7TW96aWxsYS81LjAgKE1hY2ludG9zaDsgSW50ZWwgTWFjIE9TIFggMTBfMTNfMSkgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgQ2hyb21lLzYxLjAuMzE2My4xMDAgU2FmYXJpLzUzNy4zNiZxdW90OyB2ZXJzaW9uPSZxdW90OzcuNi43JnF1b3Q7IGVkaXRvcj0mcXVvdDt3d3cuZHJhdy5pbyZxdW90OyZndDsmbHQ7ZGlhZ3JhbSBpZD0mcXVvdDtiYTZlNmZlZS1hNTU4LTljODgtMjM1Ny1jMGUyZWYxZGM1OGEmcXVvdDsgbmFtZT0mcXVvdDtQYWdlLTEmcXVvdDsmZ3Q7ZFpIQkVvSWdFSWFmaGp0QkY4OW1kZW5rb1RNQkFoTzZEdUpvUFgwYWxKSEZoZDN2LzNlWFdSRE42L0hnV0t0UElLUkZCSXNSMFIwaVpKTmxtK21heVMyU0xhR0JLR2RFWUhnQnBibkxhQ1NSOWtiSUxqRjZBT3RORzJFY3dLRnBKUGVKa1RrSFExcGJnUlZKWGN1VVhJR1NNN3VtWnlPOERwUmdqQmZoS0kzUy9sdTVNSDVWRHZvbURrU0VWczhUNUpxOW1rVi9wNW1BNFFQUkF0SGNBZmdRMVdNdTdiemRkRy83UCtyNzRVNDIva2ZCRkN5OXB5VDVRbG84QUE9PSZsdDsvZGlhZ3JhbSZndDsmbHQ7L214ZmlsZSZndDsiIHN0eWxlPSJiYWNrZ3JvdW5kLWNvbG9yOiByZ2IoMjU1LCAyNTUsIDI1NSk7Ij48ZGVmcy8+PGcgdHJhbnNmb3JtPSJ0cmFuc2xhdGUoMC41LDAuNSkiPjxyZWN0IHg9IjAiIHk9IjAiIHdpZHRoPSI3MDAiIGhlaWdodD0iMzIwIiByeD0iNDgiIHJ5PSI0OCIgZmlsbC1vcGFjaXR5PSIwLjY2IiBmaWxsPSIjMzI5NjY0IiBzdHJva2U9Im5vbmUiIHBvaW50ZXItZXZlbnRzPSJub25lIi8+PGcgdHJhbnNmb3JtPSJ0cmFuc2xhdGUoNjAuNSwxMDAuNSkiPjxzd2l0Y2g+PGZvcmVpZ25PYmplY3Qgc3R5bGU9Im92ZXJmbG93OnZpc2libGU7IiBwb2ludGVyLWV2ZW50cz0iYWxsIiB3aWR0aD0iNTc4IiBoZWlnaHQ9IjExOCIgcmVxdWlyZWRGZWF0dXJlcz0iaHR0cDovL3d3dy53My5vcmcvVFIvU1ZHMTEvZmVhdHVyZSNFeHRlbnNpYmlsaXR5Ij48ZGl2IHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8xOTk5L3hodG1sIiBzdHlsZT0iZGlzcGxheTogaW5saW5lLWJsb2NrOyBmb250LXNpemU6IDEycHg7IGZvbnQtZmFtaWx5OiBIZWx2ZXRpY2E7IGNvbG9yOiByZ2IoMCwgMCwgMCk7IGxpbmUtaGVpZ2h0OiAxLjI7IHZlcnRpY2FsLWFsaWduOiB0b3A7IHdpZHRoOiA1NzhweDsgd2hpdGUtc3BhY2U6IG5vd3JhcDsgd29yZC13cmFwOiBub3JtYWw7IHRleHQtYWxpZ246IGNlbnRlcjsiPjxkaXYgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzE5OTkveGh0bWwiIHN0eWxlPSJkaXNwbGF5OmlubGluZS1ibG9jazt0ZXh0LWFsaWduOmluaGVyaXQ7dGV4dC1kZWNvcmF0aW9uOmluaGVyaXQ7Ij48Zm9udCBjb2xvcj0iI2ZmZmZmZiIgc3R5bGU9ImZvbnQtc2l6ZTogMTAwcHgiPkVkaXQgRGlhZ3JhbTwvZm9udD48L2Rpdj48L2Rpdj48L2ZvcmVpZ25PYmplY3Q+PHRleHQgeD0iMjg5IiB5PSI2NSIgZmlsbD0iIzAwMDAwMCIgdGV4dC1hbmNob3I9Im1pZGRsZSIgZm9udC1zaXplPSIxMnB4IiBmb250LWZhbWlseT0iSGVsdmV0aWNhIj4mbHQ7Zm9udCBjb2xvcj0iI2ZmZmZmZiIgc3R5bGU9ImZvbnQtc2l6ZTogMTAwcHgiJmd0O0VkaXQgRGlhZ3JhbSZsdDsvZm9udCZndDs8L3RleHQ+PC9zd2l0Y2g+PC9nPjwvZz48L3N2Zz4=")
    newLayout2 = Layout(layout_id = 2, project_id = 2, layout_name = "Layout 2", layout_info = "data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHhtbG5zOnhsaW5rPSJodHRwOi8vd3d3LnczLm9yZy8xOTk5L3hsaW5rIiB3aWR0aD0iNzAxcHgiIGhlaWdodD0iMzIxcHgiIHZlcnNpb249IjEuMSIgY29udGVudD0iJmx0O214ZmlsZSB1c2VyQWdlbnQ9JnF1b3Q7TW96aWxsYS81LjAgKE1hY2ludG9zaDsgSW50ZWwgTWFjIE9TIFggMTBfMTNfMSkgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgQ2hyb21lLzYxLjAuMzE2My4xMDAgU2FmYXJpLzUzNy4zNiZxdW90OyB2ZXJzaW9uPSZxdW90OzcuNi43JnF1b3Q7IGVkaXRvcj0mcXVvdDt3d3cuZHJhdy5pbyZxdW90OyZndDsmbHQ7ZGlhZ3JhbSBpZD0mcXVvdDtiYTZlNmZlZS1hNTU4LTljODgtMjM1Ny1jMGUyZWYxZGM1OGEmcXVvdDsgbmFtZT0mcXVvdDtQYWdlLTEmcXVvdDsmZ3Q7ZFpIQkVvSWdFSWFmaGp0QkY4OW1kZW5rb1RNQkFoTzZEdUpvUFgwYWxKSEZoZDN2LzNlWFdSRE42L0hnV0t0UElLUkZCSXNSMFIwaVpKTmxtK21heVMyU0xhR0JLR2RFWUhnQnBibkxhQ1NSOWtiSUxqRjZBT3RORzJFY3dLRnBKUGVKa1RrSFExcGJnUlZKWGN1VVhJR1NNN3VtWnlPOERwUmdqQmZoS0kzUy9sdTVNSDVWRHZvbURrU0VWczhUNUpxOW1rVi9wNW1BNFFQUkF0SGNBZmdRMVdNdTdiemRkRy83UCtyNzRVNDIva2ZCRkN5OXB5VDVRbG84QUE9PSZsdDsvZGlhZ3JhbSZndDsmbHQ7L214ZmlsZSZndDsiIHN0eWxlPSJiYWNrZ3JvdW5kLWNvbG9yOiByZ2IoMjU1LCAyNTUsIDI1NSk7Ij48ZGVmcy8+PGcgdHJhbnNmb3JtPSJ0cmFuc2xhdGUoMC41LDAuNSkiPjxyZWN0IHg9IjAiIHk9IjAiIHdpZHRoPSI3MDAiIGhlaWdodD0iMzIwIiByeD0iNDgiIHJ5PSI0OCIgZmlsbC1vcGFjaXR5PSIwLjY2IiBmaWxsPSIjMzI5NjY0IiBzdHJva2U9Im5vbmUiIHBvaW50ZXItZXZlbnRzPSJub25lIi8+PGcgdHJhbnNmb3JtPSJ0cmFuc2xhdGUoNjAuNSwxMDAuNSkiPjxzd2l0Y2g+PGZvcmVpZ25PYmplY3Qgc3R5bGU9Im92ZXJmbG93OnZpc2libGU7IiBwb2ludGVyLWV2ZW50cz0iYWxsIiB3aWR0aD0iNTc4IiBoZWlnaHQ9IjExOCIgcmVxdWlyZWRGZWF0dXJlcz0iaHR0cDovL3d3dy53My5vcmcvVFIvU1ZHMTEvZmVhdHVyZSNFeHRlbnNpYmlsaXR5Ij48ZGl2IHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8xOTk5L3hodG1sIiBzdHlsZT0iZGlzcGxheTogaW5saW5lLWJsb2NrOyBmb250LXNpemU6IDEycHg7IGZvbnQtZmFtaWx5OiBIZWx2ZXRpY2E7IGNvbG9yOiByZ2IoMCwgMCwgMCk7IGxpbmUtaGVpZ2h0OiAxLjI7IHZlcnRpY2FsLWFsaWduOiB0b3A7IHdpZHRoOiA1NzhweDsgd2hpdGUtc3BhY2U6IG5vd3JhcDsgd29yZC13cmFwOiBub3JtYWw7IHRleHQtYWxpZ246IGNlbnRlcjsiPjxkaXYgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzE5OTkveGh0bWwiIHN0eWxlPSJkaXNwbGF5OmlubGluZS1ibG9jazt0ZXh0LWFsaWduOmluaGVyaXQ7dGV4dC1kZWNvcmF0aW9uOmluaGVyaXQ7Ij48Zm9udCBjb2xvcj0iI2ZmZmZmZiIgc3R5bGU9ImZvbnQtc2l6ZTogMTAwcHgiPkVkaXQgRGlhZ3JhbTwvZm9udD48L2Rpdj48L2Rpdj48L2ZvcmVpZ25PYmplY3Q+PHRleHQgeD0iMjg5IiB5PSI2NSIgZmlsbD0iIzAwMDAwMCIgdGV4dC1hbmNob3I9Im1pZGRsZSIgZm9udC1zaXplPSIxMnB4IiBmb250LWZhbWlseT0iSGVsdmV0aWNhIj4mbHQ7Zm9udCBjb2xvcj0iI2ZmZmZmZiIgc3R5bGU9ImZvbnQtc2l6ZTogMTAwcHgiJmd0O0VkaXQgRGlhZ3JhbSZsdDsvZm9udCZndDs8L3RleHQ+PC9zd2l0Y2g+PC9nPjwvZz48L3N2Zz4=")
    newLayout3 = Layout(layout_id = 3, project_id = 3, layout_name = "Layout 3", layout_info = "data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHhtbG5zOnhsaW5rPSJodHRwOi8vd3d3LnczLm9yZy8xOTk5L3hsaW5rIiB3aWR0aD0iNzAxcHgiIGhlaWdodD0iMzIxcHgiIHZlcnNpb249IjEuMSIgY29udGVudD0iJmx0O214ZmlsZSB1c2VyQWdlbnQ9JnF1b3Q7TW96aWxsYS81LjAgKE1hY2ludG9zaDsgSW50ZWwgTWFjIE9TIFggMTBfMTNfMSkgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgQ2hyb21lLzYxLjAuMzE2My4xMDAgU2FmYXJpLzUzNy4zNiZxdW90OyB2ZXJzaW9uPSZxdW90OzcuNi43JnF1b3Q7IGVkaXRvcj0mcXVvdDt3d3cuZHJhdy5pbyZxdW90OyZndDsmbHQ7ZGlhZ3JhbSBpZD0mcXVvdDtiYTZlNmZlZS1hNTU4LTljODgtMjM1Ny1jMGUyZWYxZGM1OGEmcXVvdDsgbmFtZT0mcXVvdDtQYWdlLTEmcXVvdDsmZ3Q7ZFpIQkVvSWdFSWFmaGp0QkY4OW1kZW5rb1RNQkFoTzZEdUpvUFgwYWxKSEZoZDN2LzNlWFdSRE42L0hnV0t0UElLUkZCSXNSMFIwaVpKTmxtK21heVMyU0xhR0JLR2RFWUhnQnBibkxhQ1NSOWtiSUxqRjZBT3RORzJFY3dLRnBKUGVKa1RrSFExcGJnUlZKWGN1VVhJR1NNN3VtWnlPOERwUmdqQmZoS0kzUy9sdTVNSDVWRHZvbURrU0VWczhUNUpxOW1rVi9wNW1BNFFQUkF0SGNBZmdRMVdNdTdiemRkRy83UCtyNzRVNDIva2ZCRkN5OXB5VDVRbG84QUE9PSZsdDsvZGlhZ3JhbSZndDsmbHQ7L214ZmlsZSZndDsiIHN0eWxlPSJiYWNrZ3JvdW5kLWNvbG9yOiByZ2IoMjU1LCAyNTUsIDI1NSk7Ij48ZGVmcy8+PGcgdHJhbnNmb3JtPSJ0cmFuc2xhdGUoMC41LDAuNSkiPjxyZWN0IHg9IjAiIHk9IjAiIHdpZHRoPSI3MDAiIGhlaWdodD0iMzIwIiByeD0iNDgiIHJ5PSI0OCIgZmlsbC1vcGFjaXR5PSIwLjY2IiBmaWxsPSIjMzI5NjY0IiBzdHJva2U9Im5vbmUiIHBvaW50ZXItZXZlbnRzPSJub25lIi8+PGcgdHJhbnNmb3JtPSJ0cmFuc2xhdGUoNjAuNSwxMDAuNSkiPjxzd2l0Y2g+PGZvcmVpZ25PYmplY3Qgc3R5bGU9Im92ZXJmbG93OnZpc2libGU7IiBwb2ludGVyLWV2ZW50cz0iYWxsIiB3aWR0aD0iNTc4IiBoZWlnaHQ9IjExOCIgcmVxdWlyZWRGZWF0dXJlcz0iaHR0cDovL3d3dy53My5vcmcvVFIvU1ZHMTEvZmVhdHVyZSNFeHRlbnNpYmlsaXR5Ij48ZGl2IHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8xOTk5L3hodG1sIiBzdHlsZT0iZGlzcGxheTogaW5saW5lLWJsb2NrOyBmb250LXNpemU6IDEycHg7IGZvbnQtZmFtaWx5OiBIZWx2ZXRpY2E7IGNvbG9yOiByZ2IoMCwgMCwgMCk7IGxpbmUtaGVpZ2h0OiAxLjI7IHZlcnRpY2FsLWFsaWduOiB0b3A7IHdpZHRoOiA1NzhweDsgd2hpdGUtc3BhY2U6IG5vd3JhcDsgd29yZC13cmFwOiBub3JtYWw7IHRleHQtYWxpZ246IGNlbnRlcjsiPjxkaXYgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzE5OTkveGh0bWwiIHN0eWxlPSJkaXNwbGF5OmlubGluZS1ibG9jazt0ZXh0LWFsaWduOmluaGVyaXQ7dGV4dC1kZWNvcmF0aW9uOmluaGVyaXQ7Ij48Zm9udCBjb2xvcj0iI2ZmZmZmZiIgc3R5bGU9ImZvbnQtc2l6ZTogMTAwcHgiPkVkaXQgRGlhZ3JhbTwvZm9udD48L2Rpdj48L2Rpdj48L2ZvcmVpZ25PYmplY3Q+PHRleHQgeD0iMjg5IiB5PSI2NSIgZmlsbD0iIzAwMDAwMCIgdGV4dC1hbmNob3I9Im1pZGRsZSIgZm9udC1zaXplPSIxMnB4IiBmb250LWZhbWlseT0iSGVsdmV0aWNhIj4mbHQ7Zm9udCBjb2xvcj0iI2ZmZmZmZiIgc3R5bGU9ImZvbnQtc2l6ZTogMTAwcHgiJmd0O0VkaXQgRGlhZ3JhbSZsdDsvZm9udCZndDs8L3RleHQ+PC9zd2l0Y2g+PC9nPjwvZz48L3N2Zz4=")
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


'''