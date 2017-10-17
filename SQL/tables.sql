-- Drop Existing Tables
DROP TABLE IF EXISTS quote;
DROP TABLE IF EXISTS project;
DROP TABLE IF EXISTS status;
DROP TABLE IF EXISTS customer;
DROP TABLE IF EXISTS roles_users;
DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS role;
DROP TABLE IF EXISTS company;
DROP TABLE IF EXISTS material;

-- Create Tables
CREATE TABLE company (
	company_id	INTEGER AUTO_INCREMENT,
	name		VARCHAR(255),
	email		VARCHAR(255) UNIQUE,
	PRIMARY KEY (company_id)
);

CREATE TABLE role (
	id 			INTEGER NOT NULL,
	name 		VARCHAR(80) UNIQUE,
	description	VARCHAR(255),
	PRIMARY KEY (id)
);

CREATE TABLE user (
	id			INTEGER,
	email		VARCHAR(255) UNIQUE,
	username	VARCHAR(255),
	password	VARCHAR(255),
	last_login_at	DATETIME,
    current_login_at DATETIME,
    last_login_ip 	VARCHAR(100),
    current_login_ip VARCHAR(100),
    login_count INTEGER,
    active 		BOOLEAN,
    confirmed_at DATETIME,
	company_id		INTEGER NOT NULL,
	PRIMARY KEY (id),
	FOREIGN KEY (company_id) REFERENCES company(company_id)
);

CREATE TABLE roles_users (
	id				INTEGER,
	user_id 		INTEGER,
	role_id			INTEGER,
	PRIMARY KEY (id),
	FOREIGN KEY (user_id) REFERENCES user(id),
	FOREIGN KEY (role_id) REFERENCES role(id)
);


CREATE TABLE customer (
	customer_id	INTEGER NOT NULL AUTO_INCREMENT,
	first_name	VARCHAR(255),
	last_name	VARCHAR(255),
	email		VARCHAR(255) UNIQUE,
	cellphone	VARCHAR(20),
	company_id	INTEGER NOT NULL,
	PRIMARY KEY (customer_id),
	FOREIGN KEY (company_id) REFERENCES company(company_id)
);

CREATE TABLE status (
	status_id	INTEGER AUTO_INCREMENT,
	status_name VARCHAR(100),
	PRIMARY KEY (status_id)
);

CREATE TABLE project (
	project_id	INTEGER NOT NULL AUTO_INCREMENT,
	customer_id INTEGER NOT NULL,
	status_id	INTEGER NOT NULL,
	address		VARCHAR(100),
	start_date	DATETIME,
	end_date 	DATETIME,
	PRIMARY KEY (project_id),
	FOREIGN KEY (customer_id) REFERENCES customer(customer_id),
	FOREIGN KEY (status_id) REFERENCES status(status_id)
);

CREATE TABLE quote (
	quote_id 	INTEGER NOT NULL AUTO_INCREMENT,
	project_id 	INTEGER NOT NULL,
	quote		DECIMAL,
	project_info BLOB,
	note		VARCHAR(250),
	last_modified	DATETIME,
	PRIMARY KEY (quote_id),
	FOREIGN KEY (project_id) REFERENCES project(project_id)
);

CREATE TABLE material (
	material_id	INTEGER NOT NULL,
	material_name VARCHAR(255),
	cost		DECIMAL,
	PRIMARY KEY (material_id)	
);