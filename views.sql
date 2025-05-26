-- 2. View members for a given organization with unpaid membership fees or dues for a given semester and academic year.
CREATE VIEW Unpaid AS
SELECT org_name, mem_id, surname, first_name, second_name,
       fee_type, amount, academic_year_issued, semester_issued, due_date
FROM FEE
NATURAL JOIN MEMBER
NATURAL JOIN ORGANIZATION
WHERE status = 'Unpaid' and fee_type = "Membership";

-- 3. View a member’s unpaid membership fees or dues for all their organizations (Member’s POV).
SELECT org_name, fee_type, amount, due_date
FROM Unpaid
WHERE surname = 'Mendoza';

-- 4. View all executive committee members of a given organization for a given academic year.
CREATE VIEW Exec AS
SELECT *
FROM MEMBER 
NATURAL JOIN SERVES
NATURAL JOIN ORGANIZATION
WHERE committee = 'Executive';

-- 5. View all Presidents (or any other role) of a given organization for every academic year in reverse chronological order.
CREATE VIEW RolesPerYear AS
SELECT org_name, surname, first_name, second_name, mem_id, role, academic_year, semester
FROM SERVES
NATURAL JOIN MEMBER
NATURAL JOIN ORGANIZATION
ORDER BY org_id, academic_year DESC;

-- 6. View all late payments made by all members of a given organization for a given semester and academic year.
CREATE VIEW LatePayments AS
SELECT org_name, mem_id, surname, first_name, second_name,
       fee_type, amount, academic_year_issued, semester_issued, due_date, date_paid
FROM FEE
NATURAL JOIN MEMBER
NATURAL JOIN ORGANIZATION
WHERE date_paid > due_date;

-- 7. View the percentage of active vs inactive members of a given organization for the last n semesters.
CREATE VIEW Percentage AS
SELECT org_id, org_name, semester, academic_year,
       COUNT(*) AS num_members,
       SUM(CASE WHEN status = 'Active' THEN 1 ELSE 0 END) AS active_members,
       CONCAT(ROUND(SUM(CASE WHEN status = 'Active' THEN 1 ELSE 0 END) * 100.00 / COUNT(*), 2),"%") AS active_percentage
FROM SERVES
NATURAL JOIN ORGANIZATION
GROUP BY org_id, org_name, semester, academic_year;

-- 8. View all alumni members of a given organization as of a given date.
-- Assuming 'Alumni' status is recorded in SERVES table.
CREATE VIEW Alumni AS
SELECT *
FROM SERVES
NATURAL JOIN MEMBER
NATURAL JOIN ORGANIZATION
WHERE status = 'Alumni';

-- 9. View the total amount of unpaid and paid fees or dues of a given organization as of a given date.
CREATE VIEW OrgFeesSummary AS
SELECT org_name, 
       SUM(CASE WHEN status = 'Paid' THEN amount ELSE 0 END) AS total_paid,
       SUM(CASE WHEN status = 'Unpaid' THEN amount ELSE 0 END) AS total_unpaid,
       date_paid
FROM FEE
NATURAL JOIN ORGANIZATION
GROUP BY org_name, date_paid
ORDER BY org_name, date_paid;

-- 10. View the member/s with the highest debt of a given organization for a given semester.
CREATE VIEW HighestDebt AS
SELECT org_name, mem_id, surname, first_name, second_name,
       semester_issued, academic_year_issued,
       SUM(CASE WHEN status = 'Unpaid' THEN amount ELSE 0 END) AS total_unpaid
FROM FEE
NATURAL JOIN MEMBER
NATURAL JOIN ORGANIZATION
GROUP BY org_name, mem_id, semester_issued, academic_year_issued
HAVING total_unpaid > 0
ORDER BY org_name, semester_issued, total_unpaid DESC;