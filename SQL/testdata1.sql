-- Test Data 1
INSERT INTO Companies (Name, Email) VALUES ('CavalryFence', 'CavalryFence@CavalryFence.com');
INSERT INTO Companies (Name, Email) VALUES ('test2', 'test2@test.com');

INSERT INTO Permissions (Permission_ID, Permission_name) VALUES (0, 'Admin');
INSERT INTO Permissions (Permission_ID, Permission_name) VALUES (1, 'Employee');

INSERT INTO Accounts (Username, Password, Email, Company_ID, Permission_ID) VALUES ('Admin', 'Admin', 'Admin@CavalryFence.com', 1 , 0);
INSERT INTO Accounts (Username, Password, Email, Company_ID, Permission_ID) VALUES ('John', 'Doe', 'JDoe@CavalryFence.com', 1 , 1);
INSERT INTO Accounts (Username, Password, Email, Company_ID, Permission_ID) VALUES ('johnny', 'hoe', 'test@test.com', 2, 0);
INSERT INTO Accounts (Username, Password, Email, Company_ID, Permission_ID) VALUES ('Adam', 'Smith', 'ASmith@CavalryFence.com', 2, 1);

INSERT INTO Customers (First_name, Last_name, Email, Homephone, Cellphone, Company_ID) VALUES ('Customer1', 'Cust1', 'Cust1@email.com', '111-1111-111', '111-CELL-111', 1);
INSERT INTO Customers (First_name, Last_name, Email, Homephone, Cellphone, Company_ID) VALUES ('Customer2', 'Cust2', 'Cust2@email.com', '222-2222-222', '222-CELL-222', 1);
INSERT INTO Customers (First_name, Last_name, Email, Homephone, Cellphone, Company_ID) VALUES ('Customer3', 'Cust3', 'Cust3@email.com', '333-3333-333', '333-CELL-333', 2);
INSERT INTO Customers (First_name, Last_name, Email, Homephone, Cellphone, Company_ID) VALUES ('Customer3', 'Cust4', 'Cust4@email.com', '444-4444-444', '444-CELL-444', 2);