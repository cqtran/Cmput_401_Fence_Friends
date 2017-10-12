-- Clear Existing Data
source tables.sql;

-- Test Data 1
INSERT INTO Companies (Name, Email) VALUES ('CavalryFence', 'CavalryFence@CavalryFence.com');
INSERT INTO Companies (Name, Email) VALUES ('test2', 'test2@test.com');

INSERT INTO Permissions (Permission_ID, Permission_name) VALUES (0, 'Admin');
INSERT INTO Permissions (Permission_ID, Permission_name) VALUES (1, 'Employee');

INSERT INTO Accounts (Username, Password, Email, Company_ID, Permission_ID) VALUES ('Admin', 'Admin', 'Admin@CavalryFence.com', 1 , 0);
INSERT INTO Accounts (Username, Password, Email, Company_ID, Permission_ID) VALUES ('John', 'Doe', 'JDoe@CavalryFence.com', 1 , 1);
INSERT INTO Accounts (Username, Password, Email, Company_ID, Permission_ID) VALUES ('johnny', 'hoe', 'test@test.com', 2, 0);
INSERT INTO Accounts (Username, Password, Email, Company_ID, Permission_ID) VALUES ('Adam', 'Smith', 'ASmith@CavalryFence.com', 2, 1);

INSERT INTO Customers (First_name, Last_name, Email, Cellphone, Company_ID) VALUES ('Customer1', 'Cust1', 'Cust1@email.com', '111-CELL-111', 1);
INSERT INTO Customers (First_name, Last_name, Email, Cellphone, Company_ID) VALUES ('Customer2', 'Cust2', 'Cust2@email.com', '222-CELL-222', 1);
INSERT INTO Customers (First_name, Last_name, Email, Cellphone, Company_ID) VALUES ('Customer3', 'Cust3', 'Cust3@email.com', '333-CELL-333', 2);
INSERT INTO Customers (First_name, Last_name, Email, Cellphone, Company_ID) VALUES ('Customer4', 'Cust4', 'Cust4@email.com', '444-CELL-444', 2);

INSERT INTO Status (Status_ID, Status_name) VALUES (0, 'Not Reached');
INSERT INTO Status (Status_ID, Status_name) VALUES (1, 'Appraisal Booked');
INSERT INTO Status (Status_ID, Status_name) VALUES (2, 'Waiting for Appraisal');
INSERT INTO Status (Status_ID, Status_name) VALUES (3, 'Appraised');
INSERT INTO Status (Status_ID, Status_name) VALUES (4, 'Quote Sent');
INSERT INTO Status (Status_ID, Status_name) VALUES (5, 'Waiting for Alberta1Call');
INSERT INTO Status (Status_ID, Status_name) VALUES (6, 'Installation Pending');
INSERT INTO Status (Status_ID, Status_name) VALUES (7, 'Installing');
INSERT INTO Status (Status_ID, Status_name) VALUES (8, 'Paid');
INSERT INTO Status (Status_ID, Status_name) VALUES (9, 'No Longer Interested');

INSERT INTO Projects (Customer_ID, Status_ID, Address, Note, Start_date) VALUES (1, 1, 'Customer1 St', 'Customer is nice', NOW());
INSERT INTO Projects (Customer_ID, Status_ID, Address, Note, Start_date) VALUES (1, 8, 'Customer1 Ave', 'Project Done', NOW());
INSERT INTO Projects (Customer_ID, Status_ID, Address, Note, Start_date) VALUES (2, 3, 'Customer2 Lane', 'Good food', NOW());
INSERT INTO Projects (Customer_ID, Status_ID, Address, Note, Start_date) VALUES (3, 5, 'Customer3 Ave', '', NOW());