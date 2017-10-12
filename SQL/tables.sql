-- Drop Existing Tables
DROP TABLE Projects;
DROP TABLE Status;
DROP TABLE Customers;
DROP TABLE Accounts;
DROP TABLE Requests;
DROP TABLE Companies;
DROP TABLE Materials;

-- Create Tables
CREATE TABLE Companies (
	Company_ID	INTEGER NOT NULL,
	Name		VARCHAR(20),
	Password	VARCHAR(20),
	Email		VARCHAR(40),
	PRIMARY KEY (Company_ID)
);

CREATE TABLE Accounts (
	Account_ID	INTEGER NOT NULL AUTO_INCREMENT,
	Username	VARCHAR(20) UNIQUE,
	Password	VARCHAR(20),
	Email		VARCHAR(40),
	Company_ID	INTEGER,
	PRIMARY KEY (Account_ID),
	FOREIGN KEY (Company_ID) REFERENCES Companies(Company_ID)
);

CREATE TABLE Requests (
	Request_ID	INTEGER NOT NULL AUTO_INCREMENT,
	Username	VARCHAR(20) UNIQUE,
	Password	VARCHAR(20),
	Email		VARCHAR(40),
	Company_ID	INTEGER,
	PRIMARY KEY (Request_ID),
	FOREIGN KEY (Company_ID) REFERENCES Companies(Company_ID)
);

CREATE TABLE Customers (
	Customer_ID	INTEGER NOT NULL AUTO_INCREMENT,
	First_name	VARCHAR(20),
	Last_name	VARCHAR(20),
	Email		VARCHAR(40),
	Homephone	VARCHAR(10),
	Cellphone	VARCHAR(10),
	Company_ID	INTEGER,
	PRIMARY KEY (Customer_ID),
	FOREIGN KEY (Company_ID) REFERENCES Companies(Company_ID)
);

CREATE TABLE Status (
	Status_ID	INTEGER NOT NULL,
	Status_name VARCHAR(20),
	PRIMARY KEY (Status_ID)
);

CREATE TABLE Projects (
	Project_ID	INTEGER NOT NULL AUTO_INCREMENT,
	Customer_ID INTEGER,
	Status_ID	INTEGER,
	Project_info BLOB,
	Quote		DECIMAL,
	Note		VARCHAR(250),
	Start_date	DATETIME,
	Last_modified	DATETIME,
	PRIMARY KEY (Project_ID),
	FOREIGN KEY (Customer_ID) REFERENCES Customers(Customer_ID),
	FOREIGN KEY (Status_ID) REFERENCES Status(Status_ID)
);

CREATE TABLE Materials (
	Material_ID	INTEGER NOT NULL,
	Material_Name VARCHAR(40),
	COST		DECIMAL
);