-- Drop Existing Tables
DROP TABLE account;
DROP TABLE customers;

-- Create Tables
CREATE TABLE accounts (
	AcctID		INT NOT NULL AUTO_INCREMENT,
	Username	VARCHAR(20),
	Password	VARCHAR(20)
);

CREATE TABLE customers (
	CustID		INT NOT NULL AUTO_INCREMENT,
	Firstname	VARCHAR(20),
	Lastname	VARCHAR(20),
	Email		VARCHAR(50),
	Homephone	VARCHAR(20),
	Cellphone	VARCHAR(20)
);