-- Clear Existing Data
-- source tables.sql;
alter database testdata;
-- use testdata.sql;

-- Test Data 1
-- Company added on startup
-- INSERT INTO Companies (Name, Email) VALUES ('Fence', 'null@null.null');

-- User
INSERT INTO user (id, email, username, password, company_name, active) VALUES 
				 (1, 'test@test.null', 'test', 'password', 'Fence', 1);
-- Role User?
INSERT INTO roles_users (id, user_id, role_id) VALUES (1, 1, 2);
