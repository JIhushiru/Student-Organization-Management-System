DROP DATABASE IF EXISTS studorg;
CREATE DATABASE studorg;

USE studorg;

-- DDL: Table Creation
CREATE TABLE MEMBER (
mem_id INT(4) PRIMARY KEY,
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
org_id INT(4) PRIMARY KEY,
org_name VARCHAR(20) NOT NULL,
type VARCHAR(20) NOT NULL
);

CREATE TABLE FEE (
fee_id INT(4) PRIMARY KEY,
mem_id INT,
org_id INT,
academic_year_issued VARCHAR(9),
semester_issued ENUM('1st', '2nd', 'Midyear'),
due_date DATE NOT NULL,
fee_type VARCHAR(50) NOT NULL,
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
status VARCHAR(10),
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
   		user_type ENUM('admin', 'president') NOT NULL,
		organization VARCHAR(50)
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
(1020, 'Gabriela', 'Ana', 'Martinez', 'gamartinez@up.edu.ph', 'BSSTAT', 2023, 'F', 2022);

-- Insert organizations (5x expanded with random data)
INSERT INTO ORGANIZATION VALUES
(1, 'CMCS_ORG', 'Academic'),
(2, 'STAT_ORG', 'Academic'),
(3, 'BIO_ORG', 'Academic'),
(4, 'AMAT_ORG', 'Academic'),
(5, 'SOCIO_ORG', 'Socio-Civic'),
(6, 'VARSI_ORG', 'Varsitarian'),
(7, 'ENGG_ORG', 'Academic'),
(8, 'CHEM_ORG', 'Academic'),
(9, 'LAW_ORG', 'Academic'),
(10, 'MATH_ORG', 'Academic'),
(11, 'LIT_ORG', 'Cultural'),
(12, 'MED_ORG', 'Academic');

-- Insert SERVES (5x expanded with random data)
INSERT INTO SERVES VALUES
(1001, 1, 'President', 'Active', 'Executive', '1st', '2024-2025'),
(1002, 2, 'Member', 'Inactive', 'Publications', '2nd', '2024-2025'),
(1003, 4, 'Member', 'Active', 'Membership', '2nd', '2024-2025'),
(1004, 5, 'Treasurer', 'Active', 'Executive', '1st', '2024-2025'),
(1005, 3, 'Member', 'Active', 'Legislative', '1st', '2024-2025'),
(1006, 6, 'Vice President', 'Active', 'Executive', '1st', '2024-2025'),
(1007, 1, 'Member', 'Inactive', 'Finance', '2nd', '2024-2025'),
(1008, 5, 'Member', 'Inactive', 'Publications', '2nd', '2024-2025'),
(1009, 6, 'Secretary', 'Active', 'Executive', '1st', '2024-2025'),
(1010, 2, 'Member', 'Active', 'External Affairs', '2nd', '2024-2025'),
(1011, 1, 'Member', 'Active', 'External Affairs', '2nd', '2024-2025'),
(1012, 7, 'Member', 'Active', 'Events', '1st', '2024-2025'),
(1013, 8, 'President', 'Active', 'Executive', '1st', '2024-2025'),
(1014, 9, 'Member', 'Inactive', 'Public Relations', '2nd', '2024-2025'),
(1015, 10, 'Vice President', 'Active', 'Executive', '2nd', '2024-2025'),
(1016, 11, 'Secretary', 'Active', 'Publications', '1st', '2024-2025'),
(1017, 12, 'Member', 'Inactive', 'Membership', '2nd', '2024-2025'),
(1018, 5, 'Member', 'Active', 'Finance', '1st', '2024-2025'),
(1019, 7, 'Treasurer', 'Active', 'Executive', '2nd', '2024-2025'),
(1020, 8, 'Member', 'Active', 'External Affairs', '1st', '2024-2025');

-- Insert FEE (5x expanded with random data)
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
-- Additional fees for new members
(115, 1012, 7, '2024-2025', '1st', '2024-12-01', 'Membership', 200.00, 'Paid', '2025-01-15'),
(116, 1013, 8, '2024-2025', '2nd', '2025-02-15', 'Semestral', 150.00, 'Paid', '2025-04-20'),
(117, 1014, 9, '2024-2025', '2nd', '2025-03-10', 'Semestral', 150.00, 'Unpaid', NULL),
(118, 1015, 10, '2024-2025', '1st', '2025-01-01', 'Semestral', 150.00, 'Paid', '2025-03-10'),
(119, 1016, 11, '2024-2025', '1st', '2025-02-01', 'Membership', 200.00, 'Paid', '2025-02-15'),
(120, 1017, 12, '2024-2025', '2nd', '2025-03-01', 'Membership', 200.00, 'Paid', '2025-03-05');



INSERT INTO userdata (username, password, user_type, organization) VALUES
('superadmin', '$2b$12$AHxFKMjQBZscM2gl1Resvepco341TN2Q9WztlNcvx0bO2MryKEnmm', 'admin', NULL),
('pres', '$2b$12$l.vNxZkiIMlA4zoPrB5YIeo05H54Yj2EFOArknAhy6vZV8YyDPe6e', 'president', 'STAT_ORG');
