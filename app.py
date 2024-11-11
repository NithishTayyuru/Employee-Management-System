# app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)
CORS(app)

class DatabaseManager:
    def __init__(self, host, user, password, database=None):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None

    def create_server_connection(self):
        """Create a connection to the MySQL server"""
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                passwd=self.password
            )
            if self.connection.is_connected():
                print("MySQL Database connection successful")
                return True
        except Error as err:
            print(f"Error: '{err}' - Failed to connect to MySQL server")
            return False

    def create_database(self, db_name):
        """Create a new database"""
        if not self.connection:
            print("No connection established")
            return False
        
        cursor = self.connection.cursor()
        try:
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
            self.connection.commit()
            print(f"Database '{db_name}' created successfully")
            return True
        except Error as err:
            print(f"Error creating database: {err}")
            return False
        finally:
            cursor.close()

    def connect_to_database(self, db_name):
        """Connect to a specific database"""
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                passwd=self.password,
                database=db_name
            )
            if self.connection.is_connected():
                print(f"Connected to database '{db_name}' successfully")
                return True
        except Error as err:
            print(f"Error connecting to database: {err}")
            return False

    def execute_query(self, query, params=None):
        """Execute a query (CREATE, INSERT, UPDATE, DELETE)"""
        if not self.connection:
            print("No database connection")
            return False

        cursor = self.connection.cursor()
        try:
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            self.connection.commit()
            return True
        except Error as err:
            print(f"Error executing query: {err}")
            return False
        finally:
            cursor.close()

    def fetch_all(self, query, params=None):
        """Fetch all results from a SELECT query"""
        if not self.connection:
            print("No database connection")
            return None

        cursor = self.connection.cursor(dictionary=True)
        try:
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            return cursor.fetchall()
        except Error as err:
            print(f"Error fetching data: {err}")
            return None
        finally:
            cursor.close()

# Initialize database manager
db_manager = DatabaseManager(
    host="localhost",
    user="root",
    password="A7824@irala"  
)

# Create database and tables if they don't exist
def initialize_database():
    db_manager.create_server_connection()
    db_manager.create_database('company')
    db_manager.connect_to_database('company')
    
    create_table_query = """
    CREATE TABLE IF NOT EXISTS employees (
        emp_no INT AUTO_INCREMENT,
        first_name VARCHAR(15) NOT NULL,
        last_name VARCHAR(15) NOT NULL,
        hire_date VARCHAR(15) NOT NULL,
        gender ENUM('M', 'F') NOT NULL,
        birth_date VARCHAR(15) NOT NULL,
        PRIMARY KEY (emp_no)
    )
    """
    db_manager.execute_query(create_table_query)

initialize_database()

@app.route('/api/employees', methods=['GET'])
def get_employees():
    query = "SELECT * FROM employees"
    employees = db_manager.fetch_all(query)
    return jsonify(employees if employees else [])

@app.route('/api/employees', methods=['POST'])
def add_employee():
    data = request.json
    query = """
    INSERT INTO employees (first_name, last_name, hire_date, gender, birth_date)
    VALUES (%s, %s, %s, %s, %s)
    """
    params = (
        data['first_name'],
        data['last_name'],
        data['hire_date'],
        data['gender'],
        data['birth_date']
    )
    
    if db_manager.execute_query(query, params):
        return jsonify({"message": "Employee added successfully"}), 201
    return jsonify({"error": "Failed to add employee"}), 400

@app.route('/api/employees/<int:emp_no>', methods=['PUT'])
def update_employee(emp_no):
    data = request.json
    query = """
    UPDATE employees
    SET first_name = %s, last_name = %s, hire_date = %s, gender = %s, birth_date = %s
    WHERE emp_no = %s
    """
    params = (
        data['first_name'],
        data['last_name'],
        data['hire_date'],
        data['gender'],
        data['birth_date'],
        emp_no
    )
    
    if db_manager.execute_query(query, params):
        return jsonify({"message": "Employee updated successfully"})
    return jsonify({"error": "Failed to update employee"}), 400

@app.route('/api/employees/<int:emp_no>', methods=['DELETE'])
def delete_employee(emp_no):
    query = "DELETE FROM employees WHERE emp_no = %s"
    if db_manager.execute_query(query, (emp_no,)):
        return jsonify({"message": "Employee deleted successfully"})
    return jsonify({"error": "Failed to delete employee"}), 400

if __name__ == '__main__':
    app.run(debug=True)