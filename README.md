# Employee-Management-System
Technologies Used

Backend: Flask (Python), MySQL
Frontend: HTML, CSS, JavaScript, Axios

Backend (app.py)
The backend of the application is built using Flask, a popular Python web framework. It provides the following functionality:

Database Connection: The DatabaseManager class handles the connection to the MySQL database, including creating the server connection, creating a new database, connecting to an existing database, executing queries, and fetching data.
API Endpoints:

get_employees: Retrieves all employees from the database and returns them as a JSON response.
add_employee: Adds a new employee to the database based on the data provided in the request body.
update_employee: Updates an existing employee in the database based on the employee ID and the data provided in the request body.
delete_employee: Deletes an employee from the database based on the employee ID.



The backend also includes an initialize_database function that creates the necessary database and table if they don't already exist.
Frontend (index.html, app.js, styles.css)
The frontend of the application is built using HTML, CSS, and JavaScript. It includes the following features:

Add Employee Form: Allows the user to input an employee's first name, last name, hire date, gender, and birth date, and submit the form to add a new employee.
Edit Employee Popup: Displays a modal popup window that allows the user to edit an existing employee's information. The popup is triggered by clicking the "Edit" button on the employee list.
Employee List: Displays a table of all employees, including their employee ID, first name, last name, hire date, gender, and birth date. The employee list is populated by making a GET request to the backend's /api/employees endpoint.
Delete Employee: Allows the user to delete an employee by clicking the "Delete" button on the employee list. The delete operation is performed by making a DELETE request to the backend's /api/employees/{emp_no} endpoint.
Styling: The application uses CSS to provide a clean and responsive user interface, including styles for the forms, tables, buttons, and popup modal.

