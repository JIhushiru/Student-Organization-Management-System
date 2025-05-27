DROP DATABASE IF EXISTS studorg;
CREATE DATABASE studorg;

USE studorg;

-- DDL: Table Creation
CREATE TABLE MEMBER (
mem_id INT(4) AUTO_INCREMENT PRIMARY KEY,
first_name VARCHAR(20) NOT NULL,
second_name VARCHAR(20),
surname VARCHAR(20) NOT NULL,
email VARCHAR(50) NOT NULL,
deg_prog VARCHAR(10) NOT NULL,
year_mem YEAR,
gender VARCHAR(1) NOT NULL,
batch INT(4) NOT NULL
);

CREATE TABLE ORGANIZATION (
org_id INT(4) AUTO_INCREMENT PRIMARY KEY,
org_name VARCHAR(50) NOT NULL,
type VARCHAR(20) NOT NULL
);

CREATE TABLE FEE (
fee_id INT(4) PRIMARY KEY,
mem_id INT,
org_id INT,
academic_year_issued VARCHAR(9),
semester_issued ENUM('1st', '2nd', 'Midyear'),
due_date DATE NOT NULL,
fee_type ENUM('Semestral', 'Membership'),
amount DECIMAL(10,2) NOT NULL,
status ENUM('Paid', 'Unpaid'),
date_paid DATE,
FOREIGN KEY (mem_id) REFERENCES MEMBER(mem_id),
FOREIGN KEY (org_id) REFERENCES ORGANIZATION(org_id)
);
	

CREATE TABLE SERVES (
	mem_id INT,
	org_id INT,
	role VARCHAR(50),
	status ENUM('Active', 'Inactive', 'Expelled', 'Suspended', 'Alumni'),
	committee VARCHAR(20),
	semester ENUM('1st', '2nd', 'Midyear'),
	academic_year VARCHAR(9),
	PRIMARY KEY (mem_id, org_id, academic_year, semester),
	FOREIGN KEY (mem_id) REFERENCES MEMBER(mem_id),
	FOREIGN KEY (org_id) REFERENCES ORGANIZATION(org_id)
);

CREATE TABLE userdata (
    	user_id INT AUTO_INCREMENT PRIMARY KEY,
    	username VARCHAR(50) NOT NULL UNIQUE,
    	password VARCHAR(255) NOT NULL,
   		user_type ENUM('admin', 'president', 'user'),
		mem_id INT,
		FOREIGN KEY (mem_id) REFERENCES MEMBER(mem_id)
);

SHOW tables;
 
-- Insert members (5x expanded with random data)
INSERT INTO MEMBER VALUES
(1001, 'Juan', 'Carlos', 'Reyes', 'jcreyes@up.edu.ph', 'BSCS', 2022, 'M', 2020),
(1002, 'Maria', 'Isabella', 'Santos', 'misantos@up.edu.ph', 'BSSTAT', 2023, 'F', 2021),
(1003, 'Jose', 'Antonio', 'Cruz', 'jacruz@up.edu.ph', 'BSAMAT', 2022, 'M', 2021),
(1004, 'Mark', 'Gabriel', 'Lopez', 'mglopez@up.edu.ph', 'BSSTAT', 2021, 'M', 2021),
(1005, 'Ana', 'Louise', 'Torres', 'altorres@up.edu.ph', 'BSBIO', 2024, 'F', 2023),
(1006, 'Paula', 'Denise', 'Garcia', 'pdgarcia@up.edu.ph', 'BSCS', 2023, 'F', 2021),
(1007, 'Andrea', 'Nicole', 'Dela Cruz', 'andelacruz@up.edu.ph', 'BSCS', 2024, 'F', 2024),
(1008, 'Carlos', 'Miguel', 'Fernandez', 'cmfernandez@up.edu.ph', 'BSBIO', 2023, 'M', 2022),
(1009, 'Miguel', 'Luis', 'Domingo', 'mldomingo@up.edu.ph', 'BSAMAT', 2022, 'M', 2021),
(1010, 'Patricia', 'Anne', 'Mendoza', 'pamendoza@up.edu.ph', 'BSSTAT', 2022, 'F', 2022),
(1011, 'Patricia', 'Anne', 'Mendoza', 'pamendoza@up.edu.ph', 'BSSTAT', 2022, 'F', 2022),
(1012, 'Elena', 'Sofia', 'Vargas', 'esvargas@up.edu.ph', 'BSE', 2023, 'F', 2021),
(1013, 'Leonardo', 'Martinez', 'Salazar', 'lmsalazar@up.edu.ph', 'BSME', 2024, 'M', 2023),
(1014, 'Isabella', 'Fernanda', 'Jimenez', 'ifjimenez@up.edu.ph', 'BSCS', 2025, 'F', 2024),
(1015, 'Diego', 'Luis', 'Pena', 'dlpena@up.edu.ph', 'BSENG', 2022, 'M', 2021),
(1016, 'Sofia', 'Andrea', 'Gonzalez', 'sagonzalez@up.edu.ph', 'BSCHE', 2023, 'F', 2022),
(1017, 'Marco', 'Antonio', 'Hernandez', 'mahernandez@up.edu.ph', 'BSPHYS', 2024, 'M', 2023),
(1018, 'Victoria', 'Elena', 'Lopez', 'velopez@up.edu.ph', 'BSCOM', 2025, 'F', 2024),
(1019, 'Alejandro', 'Jose', 'Rodriguez', 'ajr@up.edu.ph', 'BSCIV', 2023, 'M', 2021),
(1020, 'Gabriela', 'Ana', 'Martinez', 'gamartinez@up.edu.ph', 'BSSTAT', 2023, 'F', 2022),
(1021, 'John', 'Michael', 'Del Rosario', 'jmrosario@up.edu.ph', 'BSCS', 2021, 'M', 2020),
(1022, 'Christine', 'Mae', 'Lim', 'clim@up.edu.ph', 'BSSTAT', 2023, 'F', 2021),
(1023, 'Nathan', 'Lee', 'Tan', 'nltan@up.edu.ph', 'BSAMAT', 2024, 'M', 2022),
(1024, 'Clarisse', 'Joy', 'Yu', 'cjy@up.edu.ph', 'BSBIO', 2022, 'F', 2020),
(1025, 'Emmanuel', 'Paul', 'Zamora', 'epzamora@up.edu.ph', 'BSME', 2025, 'M', 2024),
(1026, 'Raquel', 'Marie', 'Soriano', 'rmsoriano@up.edu.ph', 'BSCS', 2022, 'F', 2021),
(1027, 'Darren', 'Victor', 'Chua', 'dvchua@up.edu.ph', 'BSCHE', 2023, 'M', 2022),
(1028, 'Louise', 'Andrea', 'Uy', 'lauy@up.edu.ph', 'BSSTAT', 2024, 'F', 2023),
(1029, 'Hannah', 'Ruth', 'Bautista', 'hrbautista@up.edu.ph', 'BSBIO', 2025, 'F', 2024),
(1030, 'Noel', 'James', 'Flores', 'njflores@up.edu.ph', 'BSAMAT', 2021, 'M', 2020);


-- Insert organizations (5x expanded with random data)
INSERT INTO ORGANIZATION VALUES
(1, 'Computer Science Organization', 'Academic'),
(2, 'Statistics Organization', 'Academic'),
(3, 'Biology Organization', 'Academic'),
(4, 'Applied Math Organization', 'Academic'),
(5, 'FRA Club', 'Socio-Civic'),
(6, 'Basketball Club', 'Sports'),
(7, 'Engineering Organization', 'Academic'),
(8, 'Chemistry Organization', 'Academic'),
(9, 'Volleyball Club', 'Sports'),
(10, 'Mathematics Organization', 'Academic'),
(11, 'Philosophical Organization', 'Academic'),
(12, 'Table Tennis Club', 'Sports'),
(13, 'Hockey Club', 'Sports'),
(14, 'Physics Organization', 'Academic'),
(15, 'Science Organization', 'Academic'),
(16, 'Football Club', 'Sports'),
(17, 'Forestry Organization', 'Academic'),
(18, 'DevComm Organization', 'Academic'),
(19, 'Sungka Club', 'Sports');

-- Insert SERVES 
INSERT INTO SERVES VALUES
(1001, 1, 'President', 'Active', 'Executive', '1st', '2024-2025'),
(1030, 13, 'Member', 'Active', 'Publications', '1st', '2024-2025'),
(1002, 2, 'Member', 'Inactive', 'Publications', '2nd', '2024-2025'),
(1003, 4, NULL, 'Expelled', NULL, '2nd', '2024-2025'),
(1004, 5, 'Treasurer', 'Active', 'Executive', '1st', '2024-2025'),
(1005, 3, 'Member', 'Active', 'Legislative', '1st', '2024-2025'),
(1006, 6, 'Vice President', 'Active', 'Executive', '1st', '2024-2025'),
(1007, 1, 'Member', 'Inactive', 'Finance', '2nd', '2024-2025'),
(1008, 5, NULL, 'Expelled', NULL, '2nd', '2024-2025'),
(1009, 6, 'Secretary', 'Active', 'Executive', '1st', '2024-2025'),
(1010, 2, NULL, 'Alumni', NULL, '2nd', '2024-2025'),
(1011, 1, 'Member', 'Active', 'External Affairs', '2nd', '2024-2025'),
(1012, 7, 'Member', 'Active', 'Events', '1st', '2024-2025'),
(1013, 8, 'President', 'Active', 'Executive', '1st', '2024-2025'),
(1014, 9, NULL, 'Alumni', NULL, '2nd', '2024-2025'),
(1015, 10, 'Vice President', 'Active', 'Executive', '2nd', '2024-2025'),
(1016, 11, 'Secretary', 'Active', 'Publications', '1st', '2024-2025'),
(1017, 12, 'Member', 'Inactive', 'Membership', '2nd', '2024-2025'),
(1018, 5, 'Member', 'Active', 'Finance', '1st', '2024-2025'),
(1019, 7, NULL, 'Suspended', NULL, '2nd', '2024-2025'),
(1020, 8, NULL, 'Expelled', NULL, '1st', '2024-2025'),
(1021, 1, 'Member', 'Active', 'Finance', '2nd', '2023-2024'),
(1022, 2, NULL, 'Alumni', NULL, '1st', '2023-2024'),
(1023, 4, 'Vice President', 'Active', 'Executive', '1st', '2024-2025'),
(1024, 3, 'Member', 'Active', 'Membership', '2nd', '2023-2024'),
(1025, 7, 'Secretary', 'Active', 'Executive', '2nd', '2024-2025'),
(1026, 1, 'Treasurer', 'Active', 'Executive', '1st', '2023-2024'),
(1027, 8, 'Member', 'Active', 'Publications', '1st', '2024-2025'),
(1028, 2, 'Member', 'Inactive', 'Finance', '2nd', '2023-2024'),
(1029, 3, NULL, 'Alumni', NULL, '2nd', '2024-2025'),
(1030, 4, 'Member', 'Inactive', 'Legislative', '1st', '2023-2024');


-- Insert FEE
INSERT INTO FEE VALUES
(101, 1001, 1, '2024-2025', '2nd', '2025-01-01', 'Membership', 200.00, 'Paid', '2025-04-01'),
(102, 1002, 2, '2024-2025', '2nd', '2025-01-01', 'Semestral', 150.00, 'Paid', '2025-04-10'),
(103, 1010, 2, '2024-2025', '2nd', '2025-01-01', 'Semestral', 150.00, 'Unpaid', '2024-12-20'),
(104, 1002, 2, '2024-2025', '2nd', '2025-01-01', 'Semestral', 150.00, 'Paid', '2025-04-10'),
(105, 1005, 3, '2024-2025', '1st', '2024-12-16', 'Semestral', 150.00, 'Paid', '2024-12-20'),
(106, 1005, 3, '2024-2025', '2nd', '2025-03-01', 'Membership', 200.00, 'Unpaid', NULL),
(107, 1003, 4, '2024-2025', '2nd', '2025-01-01', 'Semestral', 150.00, 'Paid', '2024-11-30'),
(108, 1004, 5, '2024-2025', '1st', '2024-12-16', 'Semestral', 150.00, 'Unpaid', NULL),
(109, 1008, 5, '2024-2025', '1st', '2024-12-16', 'Semestral', 150.00, 'Paid', '2025-02-02'),
(110, 1009, 6, '2024-2025', '1st', '2024-12-16', 'Semestral', 150.00, 'Paid', '2025-02-28'),
(111, 1006, 6, '2024-2025', '2nd', '2025-03-01', 'Membership', 200.00, 'Paid', '2025-03-01'),
(112, 1007, 1, '2024-2025', '1st', '2025-03-01', 'Membership', 200.00, 'Paid', '2024-12-12'),
(113, 1010, 2, '2024-2025', '1st', '2025-03-01', 'Membership', 200.00, 'Unpaid', '2024-12-12'),
(114, 1011, 1, '2024-2025', '1st', '2025-03-01', 'Membership', 200.00, 'Unpaid', '2024-12-12'),
(115, 1012, 7, '2024-2025', '1st', '2024-12-01', 'Membership', 200.00, 'Paid', '2025-01-15'),
(116, 1013, 8, '2024-2025', '2nd', '2025-02-15', 'Semestral', 150.00, 'Paid', '2025-04-20'),
(117, 1014, 9, '2024-2025', '2nd', '2025-03-10', 'Semestral', 150.00, 'Unpaid', NULL),
(118, 1015, 10, '2024-2025', '1st', '2025-01-01', 'Semestral', 150.00, 'Paid', '2025-03-10'),
(119, 1016, 11, '2024-2025', '1st', '2025-02-01', 'Membership', 200.00, 'Paid', '2025-02-15'),
(120, 1027, 8, '2024-2025', '1st', '2024-08-01', 'Semestral', 150.00, 'Paid', '2024-08-05'),
(121, 1028, 2, '2023-2024', '2nd', '2024-01-20', 'Semestral', 150.00, 'Paid', '2024-02-01'),
(122, 1029, 3, '2024-2025', '2nd', '2025-02-15', 'Membership', 200.00, 'Unpaid', NULL),
(123, 1030, 4, '2023-2024', '1st', '2023-07-20', 'Membership', 200.00, 'Paid', '2023-07-25'),
(124, 1030, 13, '2024-2025', '2nd', '2025-01-01', 'Membership', 200.00, 'Unpaid', '2025-04-01');

-- INSERT INTO userdata (username, password, user_type, organization, mem_id) VALUES
-- ('superadmin', '$2b$12$AHxFKMjQBZscM2gl1Resvepco341TN2Q9WztlNcvx0bO2MryKEnmm', 'admin', NULL, NULL),
-- ('pres', '$2b$12$l.vNxZkiIMlA4zoPrB5YIeo05H54Yj2EFOArknAhy6vZV8YyDPe6e', 'president', 'Statistics Organization', NULL),
-- ('jcreyes', '$2b$12$EqJnuqGobSjXEuPkOKHFDOhIpiWId0BPPkgrid/hNrlbnixhQ.6dS', 'member', 'Computer Science Organization',NULL);
INSERT INTO userdata (username, password, user_type, mem_id) VALUES
('superadmin', '$2b$12$AHxFKMjQBZscM2gl1Resvepco341TN2Q9WztlNcvx0bO2MryKEnmm', 'admin', NULL),
('Arsolon', '$2b$12$AHxFKMjQBZscM2gl1Resvepco341TN2Q9WztlNcvx0bO2MryKEnmm', 'admin', NULL),
('Garcia', '$2b$12$AHxFKMjQBZscM2gl1Resvepco341TN2Q9WztlNcvx0bO2MryKEnmm', 'admin', NULL),
('Ignaco', '$2b$12$AHxFKMjQBZscM2gl1Resvepco341TN2Q9WztlNcvx0bO2MryKEnmm', 'admin', NULL),
('Peligro', '$2b$12$AHxFKMjQBZscM2gl1Resvepco341TN2Q9WztlNcvx0bO2MryKEnmm', 'admin', NULL),
('jcreyes', '$2b$12$EqJnuqGobSjXEuPkOKHFDOhIpiWId0BPPkgrid/hNrlbnixhQ.6dS', 'president', 1001), -- President
('misantos', '$2b$12$EqJnuqGobSjXEuPkOKHFDOhIpiWId0BPPkgrid/hNrlbnixhQ.6dS', 'user', 1002),
('jacruz', '$2b$12$EqJnuqGobSjXEuPkOKHFDOhIpiWId0BPPkgrid/hNrlbnixhQ.6dS', 'user', 1003),
('mglopez', '$2b$12$EqJnuqGobSjXEuPkOKHFDOhIpiWId0BPPkgrid/hNrlbnixhQ.6dS', 'user', 1004),
('altorres', '$2b$12$EqJnuqGobSjXEuPkOKHFDOhIpiWId0BPPkgrid/hNrlbnixhQ.6dS', 'user', 1005),
('pdgarcia', '$2b$12$EqJnuqGobSjXEuPkOKHFDOhIpiWId0BPPkgrid/hNrlbnixhQ.6dS', 'user', 1006),
('andelacruz', '$2b$12$EqJnuqGobSjXEuPkOKHFDOhIpiWId0BPPkgrid/hNrlbnixhQ.6dS', 'user', 1007),
('cmfernandez', '$2b$12$EqJnuqGobSjXEuPkOKHFDOhIpiWId0BPPkgrid/hNrlbnixhQ.6dS', 'user', 1008),
('mldomingo', '$2b$12$EqJnuqGobSjXEuPkOKHFDOhIpiWId0BPPkgrid/hNrlbnixhQ.6dS', 'user', 1009),
('pamendoza', '$2b$12$EqJnuqGobSjXEuPkOKHFDOhIpiWId0BPPkgrid/hNrlbnixhQ.6dS', 'user', 1010),
('pamendoza1', '$2b$12$EqJnuqGobSjXEuPkOKHFDOhIpiWId0BPPkgrid/hNrlbnixhQ.6dS', 'user', 1011),
('esvargas', '$2b$12$EqJnuqGobSjXEuPkOKHFDOhIpiWId0BPPkgrid/hNrlbnixhQ.6dS', 'user', 1012),
('lmsalazar', '$2b$12$EqJnuqGobSjXEuPkOKHFDOhIpiWId0BPPkgrid/hNrlbnixhQ.6dS', 'president', 1013), -- President
('ifjimenez', '$2b$12$EqJnuqGobSjXEuPkOKHFDOhIpiWId0BPPkgrid/hNrlbnixhQ.6dS', 'user', 1014),
('dlpena', '$2b$12$EqJnuqGobSjXEuPkOKHFDOhIpiWId0BPPkgrid/hNrlbnixhQ.6dS', 'user', 1015),
('sagonzalez', '$2b$12$EqJnuqGobSjXEuPkOKHFDOhIpiWId0BPPkgrid/hNrlbnixhQ.6dS', 'user', 1016),
('mahernandez', '$2b$12$EqJnuqGobSjXEuPkOKHFDOhIpiWId0BPPkgrid/hNrlbnixhQ.6dS', 'user', 1017),
('velopez', '$2b$12$EqJnuqGobSjXEuPkOKHFDOhIpiWId0BPPkgrid/hNrlbnixhQ.6dS', 'user', 1018),
('ajr', '$2b$12$EqJnuqGobSjXEuPkOKHFDOhIpiWId0BPPkgrid/hNrlbnixhQ.6dS', 'user', 1019),
('gamartinez', '$2b$12$EqJnuqGobSjXEuPkOKHFDOhIpiWId0BPPkgrid/hNrlbnixhQ.6dS', 'user', 1020),
('jmrosario', '$2b$12$EqJnuqGobSjXEuPkOKHFDOhIpiWId0BPPkgrid/hNrlbnixhQ.6dS', 'user', 1021),
('clim', '$2b$12$EqJnuqGobSjXEuPkOKHFDOhIpiWId0BPPkgrid/hNrlbnixhQ.6dS', 'user', 1022),
('nltan', '$2b$12$EqJnuqGobSjXEuPkOKHFDOhIpiWId0BPPkgrid/hNrlbnixhQ.6dS', 'user', 1023),
('cjy', '$2b$12$EqJnuqGobSjXEuPkOKHFDOhIpiWId0BPPkgrid/hNrlbnixhQ.6dS', 'user', 1024),
('epzamora', '$2b$12$EqJnuqGobSjXEuPkOKHFDOhIpiWId0BPPkgrid/hNrlbnixhQ.6dS', 'user', 1025),
('rmsoriano', '$2b$12$EqJnuqGobSjXEuPkOKHFDOhIpiWId0BPPkgrid/hNrlbnixhQ.6dS', 'user', 1026),
('dvchua', '$2b$12$EqJnuqGobSjXEuPkOKHFDOhIpiWId0BPPkgrid/hNrlbnixhQ.6dS', 'user', 1027),
('lauy', '$2b$12$EqJnuqGobSjXEuPkOKHFDOhIpiWId0BPPkgrid/hNrlbnixhQ.6dS', 'user', 1028),
('hrbautista', '$2b$12$EqJnuqGobSjXEuPkOKHFDOhIpiWId0BPPkgrid/hNrlbnixhQ.6dS', 'user', 1029),
('njflores', '$2b$12$EqJnuqGobSjXEuPkOKHFDOhIpiWId0BPPkgrid/hNrlbnixhQ.6dS', 'user', 1030);
-- INSERT INTO userdata (username, password, user_type, organization, mem_id) VALUES
-- ('superadmin', '$2b$12$AHxFKMjQBZscM2gl1Resvepco341TN2Q9WztlNcvx0bO2MryKEnmm', 'admin', NULL, NULL),
-- ('pres', '$2b$12$l.vNxZkiIMlA4zoPrB5YIeo05H54Yj2EFOArknAhy6vZV8YyDPe6e', 'president', 'Statistics Organization', NULL),
-- ('member', '$2b$12$2NliramtyErVkEl5jnCD4u6WHDXh4nooBhcdqpJqVq9WdYw23ADlC', 'member', 'Computer Science Organization', 1001);

