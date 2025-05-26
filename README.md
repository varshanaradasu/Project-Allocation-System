# Project-Allocation-System

### 1.PROJECT CONTENT:
The admin logs in to add employees along with their skills and ratings. The admin can also create new projects. The application then automatically matches each project to the most appropriate employee based on their skill rating. Employees log in to check their assigned project and update its status, such as "InProgress", "Completed", or "Pending". Admins can monitor each project’s current progress and status in real-time from their dashboard.

### 2.PROJECT CODE:

  The project is developed using **Python (Flask)** for the backend, **MySQL** for data storage, and **HTML/CSS with Javascript** for the frontend. The main backend logic resides in `app.py`, which contains routes for both admin and employee functionality.
Folder structure:
- `project.py` – Main application file with routes and logic
- `templates/` – HTML files (admin_dashboard.html, employee_dashboard.html, login.html)
- `static/` – CSS and JS files for styling
- `database.sql` – SQL file to create tables (employees, projects, allocations)
The system uses form inputs to collect data, stores it in MySQL, performs auto-allocation based on skills, and renders dynamic pages.

### 3.KEY TECHNOLOGIES:

- **Flask**: Backend framework for Python
- **MySQL**: To store employee, project, and allocation data
- **HTML/CSS & Javascript**: For creating the web UI
-  **CSV Export (optional)**: Used to export project allocations for records

### 4.DESCRIPTION:
This is a web application built using **Flask** and **MySQL** to automate project allocation based on employee skill ratings.  Only the **admin** can add employees, enter their skills, and create projects.  Projects are **automatically assigned** to the best-matched employee based on their skills.  Employees can **log in to view** their assigned project and **update the status** (e.g., In Progress, Completed).  The admin dashboard shows all employees, projects, allocations, and current project statuses.  Clean and separate dashboards are provided for both Admin and Employees. Future upgrades may include AI-based matching, chart visualizations, and email notifications.

### 5.OUTPUT:

  The system generates two dashboards:
- **Admin Dashboard**: Displays employee list, project list,Add user,Add project and real-time project allocations with status updates. Admins can also export data if needed.
- **Employee Dashboard**: Shows the specific project assigned to the logged-in employee and lets them update its progress.
These outputs make the system efficient for both managing and working on tasks.
![Screenshot 2025-05-26 212644](https://github.com/user-attachments/assets/cef78aae-ecea-4b2e-b4d6-31119233e8b6)
![image](https://github.com/user-attachments/assets/d21c8111-89ba-4a3c-8e80-89af0efa6151)
![image](https://github.com/user-attachments/assets/ac01a30b-aea9-4e29-bb01-ad62c20cc181)

### 6.FUTURE RESEARCH:

- Implement AI/ML algorithms to match projects based on deeper skill analysis
- Add email or SMS notifications for new allocations and deadlines
- Use data visualization tools (like Chart.js) for status graphs and progress reports
- Role-based access using Flask-Login or JWT
- Add project history, deadlines, and multi-employee assignments for scalability







