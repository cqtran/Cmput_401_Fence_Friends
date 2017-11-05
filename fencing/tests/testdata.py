from database.models import Customer, Project, Company, Status
from database.db import dbSession

def companyTestData():
    newCompany1 = Company(company_name = "Fence", email = "Fence@Fence.com")
    newCompany2 = Company(company_name = "Builder", email = "Build@Build.com")
    dbSession.add(newCompany1)
    dbSession.add(newCompany2)
    dbSession.commit()

def statusTestData():
    status1 = Status(status_name = "Not Reached")
    dbSession.add(status1)
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
    newProject1 = Project(1, 'Not Reached', 'Bear St', None, 'A fun fencing project', "Kat's house fence", 'Fence')
    newProject2 = Project(1, 'Not Reached', 'Grand Ave', None, 'Dog lives here', "Kat's second house fence", 'Fence')
    dbSession.add(newProject1)
    dbSession.add(newProject2)
    dbSession.commit()
