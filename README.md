# 127-project  
**CMSC 127 Final Project**

## Project Overview<br/>
**studentary** is an information system designed to streamline the management of student organizations, including their events, memberships, and finances. It offers a user-friendly interface tailored to different user roles to ensure convenient and efficient access to relevant information.<br/><br/>

- **Superadmin users** have full access to the system. They can:<br/>
  - Create and delete user accounts<br/>
  - Manage all organizations<br/>
  - View and modify all data (members, fees, admins, etc.)<br/><br/>

- **Admin users** are assigned to specific organizations and can:<br/>
  - Access the Superadmin Panel<br/>
  - Add or delete organizations<br/>
  - Select an organization to view<br/>
  - Add or remove other admins<br/>
  - View all organizations<br/>
  - Create, update, and delete members and fee records<br/><br/>

- **Organization Presidents** can:<br/>
  - Access and manage only their organization<br/>
  - Create, update, and delete members and fee records within their org<br/><br/>

- **Regular Members** (non-presidents) can:<br/>
  - Only view their own organization and fee records<br/><br/>

The system is developed using **Python**, **MariaDB**, and features a modern UI using **CustomTkinter**.<br/><br/>

## Required Dependencies<br/>
- Python<br/>
- MariaDB<br/>
- MySQL<br/><br/>

## Required Python Modules<br/>
- `mariadb`<br/>
- `tkinter`<br/>
- `customtkinter`<br/><br/>

## Setup Instructions<br/>
1. Open `db_connection.py` in a code editor.<br/>
   On **line 7**, update the password field with your own MariaDB password and save the file.<br/><br/>
2. Open a terminal and run the main file:<br/>
3. Use the following credentials to log in as sample users:<br/><br/>

### Superadmin Account<br/>
- **Username**: `superadmin`<br/>
- **Password**: `password`<br/><br/>

### Admin Accounts<br/>
- `Arsolon` / `password`<br/>
- `Garcia` / `password`<br/>
- `Ignaco` / `password`<br/>
 `Peligro` / `password`<br/><br/>

### Organization President Accounts<br/>
- `lmsalazar` / `password123`<br/>
- `jcreyes` / `password123`<br/><br/>

### Member Accounts (Non-Presidents)<br/>
- (Various sample users) / `password123`<br/><br/>

 ![Image Alt](https://github.com/JIhushiru/127-project/blob/main/0712-Bad_Practices_in_Database_Design_-_Are_You_Making_These_Mistakes_Dan_Social.png?raw=true)
