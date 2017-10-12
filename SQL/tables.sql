-- Drop Existing Tables
DROP TABLE Quotes;
DROP TABLE Projects;
DROP TABLE Status;
DROP TABLE Customers;
DROP TABLE Accounts;
DROP TABLE Requests;
DROP TABLE Permissions;
DROP TABLE Companies;
DROP TABLE Materials;

-- Create Tables
CREATE TABLE Companies (
	Company_ID	INTEGER NOT NULL AUTO_INCREMENT,
	Name		VARCHAR(20),
	Email		VARCHAR(40),
	PRIMARY KEY (Company_ID)
);

CREATE TABLE Permissions (
	Permission_ID 	INTEGER NOT NULL,
	Permission_name	VARCHAR(20),
	PRIMARY KEY (Permission_ID)
);

CREATE TABLE Accounts (
	Account_ID	INTEGER NOT NULL AUTO_INCREMENT,
	Username	VARCHAR(20) UNIQUE,
	Password	VARCHAR(20),
	Email		VARCHAR(40),
	Company_ID	INTEGER NOT NULL,
	Permission_ID	 INTEGER NOT NULL,
	PRIMARY KEY (Account_ID),
	FOREIGN KEY (Company_ID) REFERENCES Companies(Company_ID),
	FOREIGN KEY (Permission_ID) REFERENCES Permissions(Permission_ID)
);

CREATE TABLE Requests (
	Request_ID	INTEGER NOT NULL AUTO_INCREMENT,
	Username	VARCHAR(20) UNIQUE,
	Password	VARCHAR(20),
	Email		VARCHAR(40),
	Company_ID	INTEGER NOT NULL,
	PRIMARY KEY (Request_ID),
	FOREIGN KEY (Company_ID) REFERENCES Companies(Company_ID)
);

CREATE TABLE Customers (
	Customer_ID	INTEGER NOT NULL AUTO_INCREMENT,
	First_name	VARCHAR(20),
	Last_name	VARCHAR(20),
	Email		VARCHAR(40),
	Cellphone	VARCHAR(15),
	Company_ID	INTEGER NOT NULL,
	PRIMARY KEY (Customer_ID),
	FOREIGN KEY (Company_ID) REFERENCES Companies(Company_ID)
);

CREATE TABLE Status (
	Status_ID	INTEGER NOT NULL,
	Status_name VARCHAR(30),
	PRIMARY KEY (Status_ID)
);

CREATE TABLE Projects (
	Project_ID	INTEGER NOT NULL AUTO_INCREMENT,
	Customer_ID INTEGER NOT NULL,
	Status_ID	INTEGER NOT NULL,
	Address		VARCHAR(30),
	Note		VARCHAR(250),
	Start_date	DATETIME,
	PRIMARY KEY (Project_ID),
	FOREIGN KEY (Customer_ID) REFERENCES Customers(Customer_ID),
	FOREIGN KEY (Status_ID) REFERENCES Status(Status_ID)
);

CREATE TABLE Quotes (
	Quote_ID 	INTEGER NOT NULL AUTO_INCREMENT,
	Project_ID 	INTEGER NOT NULL,
	Quote		DECIMAL,
	Project_info BLOB,
	Last_modified	DATETIME,
	PRIMARY KEY (Quote_ID),
	FOREIGN KEY (Project_ID) REFERENCES Projects(Project_ID)
);

CREATE TABLE Materials (
	Material_ID	INTEGER NOT NULL,
	Material_Name VARCHAR(40),
	COST		DECIMAL,
	PRIMARY KEY (Material_ID)	
);