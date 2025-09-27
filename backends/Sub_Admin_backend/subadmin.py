from flask import Flask, jsonify, request
from flask_cors import CORS
import mysql.connector

app = Flask(__name__)
CORS(app)

# MySQL Database Configuration
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "",
    "database": "user_data"
}

# Utility function to connect to the MySQL database
def get_db_connection():
    try:
        connection = mysql.connector.connect(**db_config)
        return connection
    except mysql.connector.Error as err:
        app.logger.error(f"Error connecting to database: {err}")
        return None

@app.route('/login', methods=['POST'])
def login_user():
    connection = get_db_connection()
    if connection is None:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = connection.cursor(dictionary=True)

        # Get data from request
        data = request.json
        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            return jsonify({"error": "Email and password are required"}), 400

        # Define possible tables for login
        login_tables = [
            "tbl_pet_hospital_login",
            "tbl_police_login",
            "tbl_hospital_login",
            "tbl_fire_station_login"
        ]

        user = None
        for table_name in login_tables:
            query = f"""
                SELECT id, email, password FROM {table_name} 
                WHERE email = %s AND password = %s
            """
            
            cursor.execute(query, (email, password))
            user = cursor.fetchone()
            
            if user:
                break  # Exit loop if a match is found

        if user:
            return jsonify({"message": "Login successful!", "table": table_name}), 200
        else:
            return jsonify({"error": "Invalid email or password"}), 401

    except mysql.connector.Error as err:
        app.logger.error(f"Database error: {err}")
        return jsonify({"error": "An error occurred while processing your request"}), 500

    except Exception as e:
        app.logger.error(f"Unexpected error: {e}")
        return jsonify({"error": "An unexpected error occurred"}), 500

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

# Route to retrieve user data
@app.route('/get_users_hospital', methods=['GET'])
def get_users_hospital():
    connection = get_db_connection()
    if connection is None:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT hospital_name,hospital_address,hospital_email,hospital_password,hospital_password,hospital_number,lat,log,link FROM tbl_hospital")
        users = cursor.fetchall()
        return jsonify({"users": users}), 200
    except mysql.connector.Error as err:
        app.logger.error(f"Error fetching users: {err}")
        return jsonify({"error": str(err)}), 500
    finally:
        cursor.close()
        connection.close()

@app.route('/add_hospital', methods=['POST'])
def add_hospital():
 
    connection = get_db_connection()
    if connection is None:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        # Extract data from the request
        data = request.json
        hospital_name = data.get('hospital_name')
        hospital_address = data.get('hospital_address')
        hospital_email = data.get('hospital_email')
        hospital_password = data.get('hospital_password')
        hospital_number = data.get('hospital_number')
        lat = data.get('lat')
        log = data.get('log')
        link = data.get('link')

        # Validate inputs
        if not hospital_name or not hospital_address or not hospital_email or not hospital_password or not lat or not log or not link or not hospital_password :
            return jsonify({"error": "All fields (hospital_name,hospital_address,hospital_email,hospital_password,lat,log,link) are required"}), 400

        # Execute INSERT query
        cursor = connection.cursor()
        query = "INSERT INTO tbl_hospital (hospital_name,hospital_address,hospital_email,hospital_password,hospital_number,lat,log,link) VALUES (%s,%s, %s,%s,%s, %s,%s, %s)"  
        cursor.execute(query, (hospital_name,hospital_address,hospital_email,hospital_password,hospital_number,lat,log,link))
        connection.commit()

        return jsonify({"message": "User added successfully!"}), 201
    except mysql.connector.Error as err:
        app.logger.error(f"Error adding user: {err}")
        return jsonify({"error": str(err)}), 500
    finally:
        if 'cursor' in locals():
            cursor.close()
        connection.close()

@app.route('/history_hospital', methods=['GET'])
def history_hospital():
    connection = get_db_connection()
    if connection is None:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = connection.cursor(dictionary=True)

        # Get email from query parameters
        email = request.args.get('hospital_email')

        if not email:
            return jsonify({"error": "Email is required to fetch user details"}), 400

        # Query to fetch all records for the given hospital_email
        query = """
        SELECT 
            p.fullname, p.dob, p.age, p.gender, p.contactNumber, p.patient_address, p.diseases, p.admitDate,p.email,
            b.dscdate AS discharge_date,  
            r.roomNumber AS room_number,  
            d.doctorName AS doctor_name,  
            d.doctorSpeciality AS doctor_speciality  
        FROM 
            tbl_hospital h
        LEFT JOIN 
            tbl_pdemo p ON p.hospital_id = h.hospital_id
        LEFT JOIN 
            tbl_bill b ON b.hospital_id = h.hospital_id AND b.patientId = p.patientId  
        LEFT JOIN 
            tbl_room r ON r.hospital_id = h.hospital_id AND r.patientId = p.patientId  
        LEFT JOIN 
            tbl_doc d ON d.hospital_id = h.hospital_id AND d.patientId = p.patientId  
        WHERE 
            h.hospital_email = %s
        """
        cursor.execute(query, (email,))
        records = cursor.fetchall()  # Fetch all records

        if records:
            # Debug: Log fetched records
            app.logger.debug(f"Fetched records: {records}")
            return jsonify({"records": records}), 200
        else:
            app.logger.debug("No records found for email: %s", email)
            return jsonify({"message": "No records found"}), 404

    except mysql.connector.Error as err:
        # Log detailed database error
        app.logger.error(f"Database error: {err}")
        return jsonify({"error": f"Database error: {err}"}), 500

    except Exception as e:
        # Log detailed unexpected error
        app.logger.error(f"Unexpected error: {e}")
        return jsonify({"error": f"Unexpected error: {e}"}), 500

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

@app.route('/get_users_pet_hospital', methods=['GET'])
def get_users_pet_hospital():
    connection = get_db_connection()
    if connection is None:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT pet_hospital_name,pet_hospital_address,pet_hospital_email,pet_hospital_password,pet_hospital_number,lat,log,link FROM tbl_pet_hospital")
        users = cursor.fetchall()
        return jsonify({"users": users}), 200
    except mysql.connector.Error as err:
        app.logger.error(f"Error fetching users: {err}")
        return jsonify({"error": str(err)}), 500
    finally:
        cursor.close()
        connection.close()

@app.route('/add_pet_hospital', methods=['POST'])
def add_pet_hospital():
 
    connection = get_db_connection()
    if connection is None:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        # Extract data from the request
        data = request.json
        pet_hospital_name = data.get('pet_hospital_name')
        pet_hospital_address = data.get('pet_hospital_address')
        pet_hospital_email = data.get('pet_hospital_email')
        pet_hospital_password = data.get('pet_hospital_password')
        pet_hospital_number = data.get('pet_hospital_number')
        lat = data.get('lat')
        log = data.get('log')
        link = data.get('link')

        # Validate inputs
        if not pet_hospital_name or not pet_hospital_address or not pet_hospital_email or not pet_hospital_password or not lat or not log or not link or not pet_hospital_password :
            return jsonify({"error": "All fields (pet_hospital_name,pet_hospital_address,pet_hospital_email,pet_hospital_password,lat,log,link) are required"}), 400

        # Execute INSERT query
        cursor = connection.cursor()
        query = "INSERT INTO tbl_pet_hospital (pet_hospital_name,pet_hospital_address,pet_hospital_email,pet_hospital_password,pet_hospital_number,lat,log,link) VALUES (%s,%s, %s,%s,%s, %s,%s, %s)"  
        cursor.execute(query, (pet_hospital_name,pet_hospital_address,pet_hospital_email,pet_hospital_password,pet_hospital_number,lat,log,link))
        connection.commit()

        return jsonify({"message": "User added successfully!"}), 201
    except mysql.connector.Error as err:
        app.logger.error(f"Error adding user: {err}")
        return jsonify({"error": str(err)}), 500
    finally:
        if 'cursor' in locals():
            cursor.close()
        connection.close()

@app.route('/history_pet_hospital', methods=['GET'])
def history_pet_hospital():
    connection = get_db_connection()
    if connection is None:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = connection.cursor(dictionary=True)

        # Get email from query parameters
        email = request.args.get('pet_hospital_email')

        if not email:
            return jsonify({"error": "Email is required to fetch user details"}), 400

        # Query to fetch all records for the given pet_hospital_email
        query = """SELECT 
    o.owner_name AS owner_name,
    o.owner_phone AS owner_contact,
    o.owner_email AS owner_email,
    p.pet_name AS pet_name,
    p.pet_species AS pet_species,
    p.pet_breed AS pet_breed,
    p.pet_age AS pet_age,
    a.appointment_date AS appointment_date,
    m.diagnosis AS medical_diagnosis,
    m.treatment AS medical_treatment,
    m.prescription AS medical_prescription,
    d.doc_name AS doctor_name,
    d.doc_specialization AS doctor_specialization
FROM 
    tbl_pet_hospital h
LEFT JOIN 
    tbl_pets p ON p.pet_hospital_id = h.pet_hospital_id
LEFT JOIN 
    tbl_owner o ON o.owner_id = p.owner_id
LEFT JOIN 
    tbl_appointments a ON a.pet_id = p.pet_id AND a.pet_hospital_id = h.pet_hospital_id
LEFT JOIN 
    tbl_medical_records m ON m.appointment_id = a.appointment_id AND m.pet_hospital_id = h.pet_hospital_id
LEFT JOIN 
    tbl_doctor d ON d.doc_id = a.doc_id AND d.pet_hospital_id = h.pet_hospital_id
WHERE 
    h.pet_hospital_email = %s;
"""

        cursor.execute(query, (email,))
        records = cursor.fetchall()  # Fetch all records

        if records:
            # Debug: Log fetched records
            app.logger.debug(f"Fetched records: {records}")
            return jsonify({"records": records}), 200
        else:
            app.logger.debug("No records found for email: %s", email)
            return jsonify({"message": "No records found"}), 404

    except mysql.connector.Error as err:
        # Log detailed database error
        app.logger.error(f"Database error: {err}")
        return jsonify({"error": f"Database error: {err}"}), 500

    except Exception as e:
        # Log detailed unexpected error
        app.logger.error(f"Unexpected error: {e}")
        return jsonify({"error": f"Unexpected error: {e}"}), 500

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


# Route to retrieve user data
@app.route('/get_users_fire_station', methods=['GET'])
def get_users_fire_station():
    connection = get_db_connection()
    if connection is None:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT fire_station_name,fire_station_address,fire_station_email,fire_station_password,fire_station_number,lat,log,link FROM tbl_fire_station")
        users = cursor.fetchall()
        return jsonify({"users": users}), 200
    except mysql.connector.Error as err:
        app.logger.error(f"Error fetching users: {err}")
        return jsonify({"error": str(err)}), 500
    finally:
        cursor.close()
        connection.close()

@app.route('/add_fire_station', methods=['POST'])
def add_fire_station():
 
    connection = get_db_connection()
    if connection is None:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        # Extract data from the request
        data = request.json
        fire_station_name = data.get('fire_station_name')
        fire_station_address = data.get('fire_station_address')
        fire_station_email = data.get('fire_station_email')
        fire_station_password = data.get('fire_station_password')
        fire_station_number = data.get('fire_station_number')
        lat = data.get('lat')
        log = data.get('log')
        link = data.get('link')

        # Validate inputs
        if not fire_station_name or not fire_station_address or not fire_station_email or not fire_station_password or not lat or not log or not link or not fire_station_password :
            return jsonify({"error": "All fields (fire_station_name,fire_station_address,fire_station_email,fire_station_password,lat,log,link) are required"}), 400

        # Execute INSERT query
        cursor = connection.cursor()
        query = "INSERT INTO tbl_fire_station (fire_station_name,fire_station_address,fire_station_email,fire_station_password,fire_station_number,lat,log,link) VALUES (%s,%s, %s,%s,%s, %s,%s, %s)"  
        cursor.execute(query, (fire_station_name,fire_station_address,fire_station_email,fire_station_password,fire_station_number,lat,log,link))
        connection.commit()

        return jsonify({"message": "User added successfully!"}), 201
    except mysql.connector.Error as err:
        app.logger.error(f"Error adding user: {err}")
        return jsonify({"error": str(err)}), 500
    finally:
        if 'cursor' in locals():
            cursor.close()
        connection.close()

@app.route('/history_fire_station', methods=['GET'])
def history_fire_station():
    connection = get_db_connection()
    if connection is None:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = connection.cursor(dictionary=True)

        email = request.args.get('fire_station_email')
        if not email:
            return jsonify({"error": "Email is required to fetch user details"}), 400

        query = """
            SELECT 
                d.dispatch_time, 
                d.arrival_time, 
                d.return_time, 
                i.incident_description, 
                i.incident_type, 
                i.incident_location, 
                i.complain_mail,
                i.incident_date_reported, 
                ff.firefighter_name, 
                ff.firefighter_rank, 
                ff.firefighter_badge_number, 
                eq.equipment_name, 
                eq.equipment_type, 
                eq.equipment_status, 
                em.maintenance_date, 
                em.maintenance_performed_by, 
                em.maintenance_notes
            FROM 
                tbl_fire_station fs
            LEFT JOIN 
                tbl_dispatches d ON fs.fire_station_id = d.fire_station_id
            LEFT JOIN 
                tbl_incidents i ON d.incident_id = i.incident_id
            LEFT JOIN 
                tbl_firefighters ff ON d.firefighter_id = ff.firefighter_id
            LEFT JOIN 
                tbl_equipment eq ON fs.fire_station_id = eq.fire_station_id
            LEFT JOIN 
                tbl_equipment_maintenance em ON eq.equipment_id = em.equipment_id
            WHERE 
                fs.fire_station_email = %s
        """

        cursor.execute(query, (email,))
        records = cursor.fetchall()

        if records:
            app.logger.debug(f"Fetched records: {records}")
            return jsonify({"records": records}), 200
        else:
            app.logger.debug("No records found for email: %s", email)
            return jsonify({"message": "No records found"}), 404

    except mysql.connector.Error as err:
        app.logger.error(f"Database error: {err}")
        return jsonify({"error": f"Database error: {err}"}), 500

    except Exception as e:
        app.logger.error(f"Unexpected error: {e}")
        return jsonify({"error": f"Unexpected error: {e}"}), 500

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


@app.route('/get_users_police_station', methods=['GET'])
def get_users_police_station():
    connection = get_db_connection()
    if connection is None:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT police_station_name,police_station_address,police_station_email,police_station_password,police_station_number,lat,log,link FROM tbl_police_station")
        users = cursor.fetchall()
        return jsonify({"users": users}), 200
    except mysql.connector.Error as err:
        app.logger.error(f"Error fetching users: {err}")
        return jsonify({"error": str(err)}), 500
    finally:
        cursor.close()
        connection.close()

@app.route('/add_police_station', methods=['POST'])
def add_police_station():
 
    connection = get_db_connection()
    if connection is None:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        # Extract data from the request
        data = request.json
        police_station_name = data.get('police_station_name')
        police_station_address = data.get('police_station_address')
        police_station_email = data.get('police_station_email')
        police_station_password = data.get('police_station_password')
        police_station_number = data.get('police_station_number')
        lat = data.get('lat')
        log = data.get('log')
        link = data.get('link')

        # Validate inputs
        if not police_station_name or not police_station_address or not police_station_email or not police_station_password or not lat or not log or not link or not police_station_password :
            return jsonify({"error": "All fields (police_station_name,police_station_address,police_station_email,police_station_password,lat,log,link) are required"}), 400

        # Execute INSERT query
        cursor = connection.cursor()
        query = "INSERT INTO tbl_police_station (police_station_name,police_station_address,police_station_email,police_station_password,police_station_number,lat,log,link) VALUES (%s,%s, %s,%s,%s, %s,%s, %s)"  
        cursor.execute(query, (police_station_name,police_station_address,police_station_email,police_station_password,police_station_number,lat,log,link))
        connection.commit()

        return jsonify({"message": "User added successfully!"}), 201
    except mysql.connector.Error as err:
        app.logger.error(f"Error adding user: {err}")
        return jsonify({"error": str(err)}), 500
    finally:
        if 'cursor' in locals():
            cursor.close()
        connection.close()

@app.route('/history_police_station', methods=['GET'])
def history_police_station():
    # Get database connection
    connection = get_db_connection()
    if connection is None:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = connection.cursor(dictionary=True)

        # Get email from query parameters
        email = request.args.get('police_station_email')
        if not email:
            return jsonify({"error": "Email is required to fetch police station history"}), 400

        # Query to fetch all records for the given police_station_email
        query = """
        SELECT 
            c.user_email,
            c.case_number, 
            c.case_title, 
            c.case_description, 
            cr.criminal_name, 
            cr.dob AS criminal_dob, 
            cr.criminal_address, 
            o.officer_name, 
            o.officer_rank, 
            o.officer_badge_number, 
            e.evidence_description, 
            e.date_collected, 
            e.location_found
        FROM 
            tbl_police_station ps
        LEFT JOIN 
            tbl_cases c ON ps.police_station_id = c.police_station_id
        LEFT JOIN 
            tbl_arrests a ON c.case_id = a.case_id
        LEFT JOIN 
            tbl_criminals cr ON a.criminal_id = cr.criminal_id
        LEFT JOIN 
            tbl_officers o ON a.officer_id = o.officer_id
        LEFT JOIN 
            tbl_evidence e ON c.case_id = e.case_id
        WHERE 
            ps.police_station_email = %s;
        """
        cursor.execute(query, (email,))
        records = cursor.fetchall()  # Fetch all records

        if records:
            # Log fetched records for debugging
            app.logger.debug(f"Fetched records for email {email}: {records}")
            return jsonify({"records": records}), 200
        else:
            # Log if no records are found
            app.logger.debug(f"No records found for email: {email}")
            return jsonify({"message": "No records found"}), 404

    except mysql.connector.Error as db_err:
        # Log detailed database error
        app.logger.error(f"Database error: {db_err}")
        return jsonify({"error": f"Database error: {db_err}"}), 500

    except Exception as err:
        # Log detailed unexpected error
        app.logger.error(f"Unexpected error: {err}")
        return jsonify({"error": f"Unexpected error: {err}"}), 500

    finally:
        # Ensure resources are closed properly
        if cursor:
            cursor.close()
        if connection:
            connection.close()


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)