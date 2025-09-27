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

def get_db_connection():
    try:
        connection = mysql.connector.connect(**db_config)
        return connection
    except mysql.connector.Error as err:
        app.logger.error(f"Error connecting to database: {err}")
        return None


#Login

@app.route('/superadmin_login', methods=['POST'])
def superadmin_login():
    data = request.json

    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400

    connection = get_db_connection()
    if connection is None:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = connection.cursor(dictionary=True)

        query = "SELECT superadmin_id, superadmin_email, superadmin_password FROM tbl_superadmin WHERE superadmin_email = %s AND superadmin_password = %s"
        cursor.execute(query, (email, password))
        admin = cursor.fetchone()

        if admin:
            return jsonify({"message": "Login successful", "superadmin_id": admin['superadmin_id']}), 200
        else:
            return jsonify({"error": "Invalid email or password"}), 401

    except mysql.connector.Error as err:
        return jsonify({"error": f"Database error: {err}"}), 500

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()



# list

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

@app.route('/get_users', methods=['GET'])
def get_users():
    connection = get_db_connection()
    if connection is None:
        return jsonify({"error": "Database connection failed"}), 500

    cursor = None
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT email, username, phone, address, dob,age,adharnumber FROM tbl_user")
        users = cursor.fetchall()
        return jsonify({"users": users}), 200
    except mysql.connector.Error as err:
        print(f"Error fetching users: {err}")
        return jsonify({"error": str(err)}), 500
    finally:
        if cursor:
            cursor.close()
        connection.close()

@app.route('/get_hospitals', methods=['GET'])
def get_hospitals():
    connection = get_db_connection()
    if connection is None:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM tbl_hospital_login")
        hospitals = cursor.fetchall()
        return jsonify(hospitals), 200
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500
    finally:
        cursor.close()
        connection.close()

@app.route('/get_firestations', methods=['GET'])
def get_firestations():
    connection = get_db_connection()
    if connection is None:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM tbl_fire_station_login")
        firestations = cursor.fetchall()
        return jsonify(firestations), 200
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500
    finally:
        cursor.close()
        connection.close()

@app.route('/get_police', methods=['GET'])
def get_police():
    connection = get_db_connection()
    if connection is None:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM tbl_police_login")
        police = cursor.fetchall()
        return jsonify(police), 200
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500
    finally:
        cursor.close()
        connection.close()

@app.route('/get_pet_hospitals', methods=['GET'])
def get_pet_hospitals():    
    connection = get_db_connection()
    if connection is None:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM tbl_pet_hospital_login")
        pet_hospitals = cursor.fetchall()
        return jsonify(pet_hospitals), 200
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500
    finally:
        cursor.close()
        connection.close()


# History
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

@app.route('/history_user', methods=['GET'])
def history_user():
    connection = get_db_connection()
    if connection is None:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = connection.cursor(dictionary=True)

        # Get email from query parameters
        email = request.args.get('email')

        if not email:
            return jsonify({"error": "Email is required to fetch user details"}), 400

        # Query to fetch all records for the given user email
        query = """
        SELECT 
            username, dob, age, phone, address,adharnumber
        FROM 
            tbl_user 
            where
            email = %s
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

@app.route('/bill_details', methods=['GET'])
def bill_details():
    connection = get_db_connection()
    if connection is None:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = connection.cursor(dictionary=True)

        # Get all records from tbl_user_bill
        query = "SELECT * FROM tbl_user_bill"
        cursor.execute(query)
        records = cursor.fetchall()

        if records:
            app.logger.debug(f"Fetched records: {records}")
            return jsonify({"records": records}), 200
        else:
            app.logger.debug("No records found")
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


# Update Modules 
@app.route('/update_user', methods=['POST'])
def update_user():
    data = request.get_json()

    email = data.get("email")
    username = data.get("username")
    address = data.get("address")
    phone = data.get("number")
    age = data.get("age")
    dob = data.get("dob")

    if not email:
        return jsonify({"error": "Email is required to update user"}), 400

    connection = get_db_connection()
    if connection is None:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = connection.cursor()
        update_query = """
            UPDATE tbl_user
            SET username = %s,
                address = %s,
                phone = %s,
                age = %s,
                dob = %s
            WHERE email = %s
        """
        values = (username, address, phone, age, dob, email)
        cursor.execute(update_query, values)
        connection.commit()

        if cursor.rowcount == 0:
            return jsonify({"message": "No user found with this email"}), 404

        return jsonify({"message": "User updated successfully"}), 200

    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        return jsonify({"error": str(err)}), 500
    finally:
        cursor.close()
        connection.close()

@app.route('/update_hospital_login', methods=['POST'])
def update_hospital_login():
    data = request.get_json()

    email = data.get("email")
    modulename = data.get("modulename")


    if not email:
        return jsonify({"error": "Email is required to update user"}), 400

    connection = get_db_connection()
    if connection is None:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = connection.cursor()
        update_query = """
            UPDATE tbl_hospital_login
            SET modulename = %s
            WHERE email = %s
        """
        values = (modulename, email)
        cursor.execute(update_query, values)
        connection.commit()

        if cursor.rowcount == 0:
            return jsonify({"message": "No user found with this email"}), 404

        return jsonify({"message": "User updated successfully"}), 200

    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        return jsonify({"error": str(err)}), 500
    finally:
        cursor.close()
        connection.close()

@app.route('/update_pet_hospital_login', methods=['POST'])
def update_pet_hospital_login():
    data = request.get_json()

    email = data.get("email")
    modulename = data.get("modulename")

    if not email:
        return jsonify({"error": "Email is required to update user"}), 400

    connection = get_db_connection()
    if connection is None:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = connection.cursor()
        update_query = """
            UPDATE tbl_pet_hospital_login
            SET modulename = %s
            WHERE email = %s
        """
        values = (modulename, email)
        cursor.execute(update_query, values)
        connection.commit()

        if cursor.rowcount == 0:
            return jsonify({"message": "No user found with this email"}), 404

        return jsonify({"message": "User updated successfully"}), 200

    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        return jsonify({"error": str(err)}), 500
    finally:
        cursor.close()
        connection.close()


@app.route('/update_fire_station_login', methods=['POST'])
def update_fire_station_login():
    data = request.get_json()

    email = data.get("email")
    modulename = data.get("modulename")

    if not email:
        return jsonify({"error": "Email is required to update user"}), 400

    connection = get_db_connection()
    if connection is None:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = connection.cursor()
        update_query = """
            UPDATE tbl_fire_station_login
            SET modulename = %s
            WHERE email = %s
        """
        values = (modulename, email)
        cursor.execute(update_query, values)
        connection.commit()

        if cursor.rowcount == 0:
            return jsonify({"message": "No user found with this email"}), 404

        return jsonify({"message": "User updated successfully"}), 200

    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        return jsonify({"error": str(err)}), 500
    finally:
        cursor.close()
        connection.close()

@app.route('/update_police_station_login', methods=['POST'])
def update_police_station_login():
    data = request.get_json()

    email = data.get("email")
    modulename = data.get("modulename")

    if not email:
        return jsonify({"error": "Email is required to update user"}), 400

    connection = get_db_connection()
    if connection is None:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = connection.cursor()
        update_query = """
            UPDATE tbl_police_login
            SET modulename = %s
            WHERE email = %s
        """
        values = (modulename, email)
        cursor.execute(update_query, values)
        connection.commit()

        if cursor.rowcount == 0:
            return jsonify({"message": "No user found with this email"}), 404

        return jsonify({"message": "User updated successfully"}), 200

    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        return jsonify({"error": str(err)}), 500
    finally:
        cursor.close()
        connection.close()


@app.route('/update_hospital', methods=['POST'])
def update_hospital():
    data = request.get_json()

    email = data.get("hospital_email")
    username = data.get("hospital_name")
    address = data.get("hospital_address")
    phone = data.get("hospital_number")
  

    if not email:
        return jsonify({"error": "Email is required to update Hospital"}), 400

    connection = get_db_connection()
    if connection is None:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = connection.cursor()
        update_query = """
            UPDATE tbl_hospital
            SET hospital_name = %s,
                hospital_address = %s,
                hospital_number = %s
            WHERE hospital_email = %s
        """
        values = (username, address, phone, email)
        cursor.execute(update_query, values)
        connection.commit()

        if cursor.rowcount == 0:
            return jsonify({"message": "No Hospital found with this email"}), 404

        return jsonify({"message": "Hospital updated successfully"}), 200

    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        return jsonify({"error": str(err)}), 500
    finally:
        cursor.close()
        connection.close()

@app.route('/update_pet_hospital', methods=['POST'])
def update_pet_hospital():
    data = request.get_json()

    email = data.get("pet_hospital_email")
    username = data.get("pet_hospital_name")
    address = data.get("pet_hospital_address")
    phone = data.get("pet_hospital_number")
  

    if not email:
        return jsonify({"error": "Email is required to update Pet Hospital"}), 400

    connection = get_db_connection()
    if connection is None:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = connection.cursor()
        update_query = """
            UPDATE tbl_pet_hospital
            SET pet_hospital_name = %s,
                pet_hospital_address = %s,
                pet_hospital_number = %s
            WHERE pet_hospital_email = %s
        """
        values = (username, address, phone, email)
        cursor.execute(update_query, values)
        connection.commit()

        if cursor.rowcount == 0:
            return jsonify({"message": "No Pet Hospital found with this email"}), 404

        return jsonify({"message": "Pet Hospital updated successfully"}), 200

    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        return jsonify({"error": str(err)}), 500
    finally:
        cursor.close()
        connection.close()

@app.route('/update_fire_station', methods=['POST'])
def update_fire_station():
    data = request.get_json()

    email = data.get("fire_station_email")
    username = data.get("fire_station_name")
    address = data.get("fire_station_address")
    phone = data.get("fire_station_number")
  

    if not email:
        return jsonify({"error": "Email is required to update Fire Station"}), 400

    connection = get_db_connection()
    if connection is None:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = connection.cursor()
        update_query = """
            UPDATE tbl_fire_station
            SET fire_station_name = %s,
                fire_station_address = %s,
                fire_station_number = %s
            WHERE fire_station_email = %s
        """
        values = (username, address, phone, email)
        cursor.execute(update_query, values)
        connection.commit()

        if cursor.rowcount == 0:
            return jsonify({"message": "No Fire Station found with this email"}), 404

        return jsonify({"message": "Fire Station updated successfully"}), 200

    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        return jsonify({"error": str(err)}), 500
    finally:
        cursor.close()
        connection.close()

@app.route('/update_police_station', methods=['POST'])
def update_police_station():
    data = request.get_json()

    email = data.get("police_station_email")
    name = data.get("police_station_name")
    address = data.get("police_station_address")
    phone = data.get("police_station_number")

    if not email:
        return jsonify({"error": "Email is required to update Police Station"}), 400

    connection = get_db_connection()
    if connection is None:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = connection.cursor()
        update_query = """
            UPDATE tbl_police_station
            SET police_station_name = %s,
                police_station_address = %s,
                police_station_number = %s
            WHERE police_station_email = %s
        """
        values = (name, address, phone, email)
        cursor.execute(update_query, values)
        connection.commit()

        if cursor.rowcount == 0:
            return jsonify({"message": "No Police Station found with this email"}), 404

        return jsonify({"message": "Police Station updated successfully"}), 200

    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        return jsonify({"error": str(err)}), 500

    finally:
        cursor.close()
        connection.close()


# delete Modules
@app.route('/delete_user', methods=['POST'])
def delete_user():
    data = request.get_json()

    email = data.get("email")

    if not email:
        return jsonify({"error": "Email is required to delete user"}), 400

    connection = get_db_connection()
    if connection is None:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = connection.cursor()
        delete_query = """
            DELETE FROM tbl_user 
            WHERE email = %s
        """
        values = (email,)  # Tuple must have a trailing comma
        cursor.execute(delete_query, values)
        connection.commit()

        if cursor.rowcount == 0:
            return jsonify({"message": "No user found with this email"}), 404

        return jsonify({"message": "User deleted successfully"}), 200

    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        return jsonify({"error": str(err)}), 500

    finally:
        cursor.close()
        connection.close()

@app.route('/delete_hospital_login', methods=['POST'])
def delete_hospital_login():
    data = request.get_json()

    email = data.get("email")

    if not email:
        return jsonify({"error": "Hospital email is required"}), 400

    connection = get_db_connection()
    if connection is None:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = connection.cursor()

        # Delete query
        delete_query = """
            DELETE FROM tbl_hospital_login
            WHERE email = %s
        """
        cursor.execute(delete_query, (email,))
        connection.commit()

        if cursor.rowcount == 0:
            return jsonify({"message": "No hospital found with this email"}), 404

        return jsonify({"message": "Hospital user deleted successfully"}), 200

    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        return jsonify({"error": f"Database error: {err}"}), 500

    finally:
        cursor.close()
        connection.close()

@app.route('/delete_pet_hospital_login', methods=['POST'])
def delete_pet_hospital_login():
    data = request.get_json()

    email = data.get("email")

    if not email:
        return jsonify({"error": "Pet hospital email is required"}), 400

    connection = get_db_connection()
    if connection is None:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = connection.cursor()

        # Delete query
        delete_query = """
            DELETE FROM tbl_pet_hospital_login
            WHERE email = %s
        """
        cursor.execute(delete_query, (email,))
        connection.commit()

        if cursor.rowcount == 0:
            return jsonify({"message": "No pet hospital found with this email"}), 404

        return jsonify({"message": "Pet hospital user deleted successfully"}), 200

    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        return jsonify({"error": f"Database error: {err}"}), 500

    finally:
        cursor.close()
        connection.close()

@app.route('/delete_fire_station_login', methods=['POST'])
def delete_fire_station_login():
    data = request.get_json()

    email = data.get("email")

    if not email:
        return jsonify({"error": "Fire station email is required"}), 400

    connection = get_db_connection()
    if connection is None:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = connection.cursor()

        delete_query = """
            DELETE FROM tbl_fire_station_login
            WHERE email = %s
        """
        cursor.execute(delete_query, (email,))
        connection.commit()

        if cursor.rowcount == 0:
            return jsonify({"message": "No fire station found with this email"}), 404

        return jsonify({"message": "Fire station user deleted successfully"}), 200

    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        return jsonify({"error": f"Database error: {err}"}), 500

    finally:
        cursor.close()
        connection.close()

@app.route('/delete_police_station_login', methods=['POST'])
def delete_police_station_login():
    data = request.get_json()

    email = data.get("email")

    if not email:
        return jsonify({"error": "Police station email is required"}), 400

    connection = get_db_connection()
    if connection is None:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = connection.cursor()

        delete_query = """
            DELETE FROM tbl_police_login
            WHERE email  = %s
        """
        cursor.execute(delete_query, (email,))
        connection.commit()

        if cursor.rowcount == 0:
            return jsonify({"message": "No police station found with this email"}), 404

        return jsonify({"message": "Police station user deleted successfully"}), 200

    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        return jsonify({"error": f"Database error: {err}"}), 500

    finally:
        cursor.close()
        connection.close()

@app.route('/delete_hospital', methods=['POST'])
def delete_hospital():
    data = request.get_json()

    email = data.get("hospital_email")

    if not email:
        return jsonify({"error": "Email is required to delete user"}), 400

    connection = get_db_connection()
    if connection is None:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = connection.cursor()
        delete_query = """
            DELETE FROM tbl_hospital 
            WHERE hospital_email = %s
        """
        values = (email,)  # Tuple must have a trailing comma
        cursor.execute(delete_query, values)
        connection.commit()

        if cursor.rowcount == 0:
            return jsonify({"message": "No Hospital found with this email"}), 404

        return jsonify({"message": "Hospital deleted successfully"}), 200

    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        return jsonify({"error": str(err)}), 500

    finally:
        cursor.close()
        connection.close()

@app.route('/delete_pet_hospital', methods=['POST'])
def delete_pet_hospital():
    data = request.get_json()

    email = data.get("pet_hospital_email")

    if not email:
        return jsonify({"error": "Email is required to delete user"}), 400

    connection = get_db_connection()
    if connection is None:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = connection.cursor()
        delete_query = """
            DELETE FROM tbl_pet_hospital 
            WHERE pet_hospital_email = %s
        """
        values = (email,)  # Tuple must have a trailing comma
        cursor.execute(delete_query, values)
        connection.commit()

        if cursor.rowcount == 0:
            return jsonify({"message": "No Hospital found with this email"}), 404

        return jsonify({"message": "Hospital deleted successfully"}), 200

    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        return jsonify({"error": str(err)}), 500

    finally:
        cursor.close()
        connection.close()

@app.route('/delete_fire_station', methods=['POST'])
def delete_fire_station():
    data = request.get_json()

    email = data.get("fire_station_email")

    if not email:
        return jsonify({"error": "Email is required to delete user"}), 400

    connection = get_db_connection()
    if connection is None:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = connection.cursor()
        delete_query = """
            DELETE FROM tbl_fire_station 
            WHERE fire_station_email = %s
        """
        values = (email,)  # Tuple must have a trailing comma
        cursor.execute(delete_query, values)
        connection.commit()

        if cursor.rowcount == 0:
            return jsonify({"message": "No Hospital found with this email"}), 404

        return jsonify({"message": "Hospital deleted successfully"}), 200

    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        return jsonify({"error": str(err)}), 500

    finally:
        cursor.close()
        connection.close()

@app.route('/delete_police_station', methods=['POST'])
def delete_police_station():
    data = request.get_json()

    email = data.get("police_station_email")

    if not email:
        return jsonify({"error": "Email is required to delete user"}), 400

    connection = get_db_connection()
    if connection is None:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = connection.cursor()
        delete_query = """
            DELETE FROM  tbl_police_station 
            WHERE police_station_email = %s
        """
        values = (email,)  # Tuple must have a trailing comma
        cursor.execute(delete_query, values)
        connection.commit()

        if cursor.rowcount == 0:
            return jsonify({"message": "No Hospital found with this email"}), 404

        return jsonify({"message": "Hospital deleted successfully"}), 200

    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        return jsonify({"error": str(err)}), 500

    finally:
        cursor.close()
        connection.close()

# Delete Modules Data
@app.route('/delete_hospital_data', methods=['POST'])
def delete_hospital_data():
    data = request.get_json()
    email = data.get('email')

    if not email:
        return jsonify({"error": "Email is required"}), 400

    connection = get_db_connection()
    if connection is None:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = connection.cursor()

        delete_query = """
            DELETE d, r, s, b, p
            FROM tbl_pdemo p
            JOIN tbl_hospital h ON p.hospital_id = h.hospital_id
            LEFT JOIN tbl_doc d ON d.patientId = p.patientId AND d.hospital_id = h.hospital_id
            LEFT JOIN tbl_room r ON r.patientId = p.patientId AND r.hospital_id = h.hospital_id
            LEFT JOIN tbl_staff s ON s.patientId = p.patientId AND s.hospital_id = h.hospital_id
            LEFT JOIN tbl_bill b ON b.patientId = p.patientId AND b.hospital_id = h.hospital_id
            WHERE p.email = %s
        """

        cursor.execute(delete_query, (email,))
        connection.commit()

        if cursor.rowcount == 0:
            return jsonify({"message": "No data found for the provided email."}), 404

        return jsonify({"message": "Hospital data and related records deleted successfully."}), 200

    except mysql.connector.Error as err:
        print(f"Database Error: {err}")
        return jsonify({"error": str(err)}), 500
    finally:
        cursor.close()
        connection.close()

@app.route('/delete_pet_hospital_data', methods=['POST'])
def delete_pet_hospital_data():
    data = request.get_json()
    owner_email = data.get('owner_email')

    if not owner_email:
        return jsonify({"error": "Owner email is required"}), 400

    connection = get_db_connection()
    if connection is None:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = connection.cursor()

        delete_query = """
            DELETE m, a, d, p, o
            FROM tbl_owner o
            LEFT JOIN tbl_pets p ON o.owner_id = p.owner_id
            LEFT JOIN tbl_pet_hospital ph ON p.pet_hospital_id = ph.pet_hospital_id
            LEFT JOIN tbl_appointments a ON a.pet_id = p.pet_id AND a.pet_hospital_id = ph.pet_hospital_id
            LEFT JOIN tbl_medical_records m ON m.appointment_id = a.appointment_id AND m.pet_hospital_id = ph.pet_hospital_id
            LEFT JOIN tbl_doctor d ON d.doc_id = a.doc_id AND d.pet_hospital_id = ph.pet_hospital_id
            WHERE o.owner_email = %s
        """

        cursor.execute(delete_query, (owner_email,))
        connection.commit()

        if cursor.rowcount == 0:
            return jsonify({"message": "No data found for the provided owner email."}), 404

        return jsonify({"message": "Records deleted successfully for the provided owner email and associated hospital."}), 200

    except mysql.connector.Error as err:
        print(f"Database Error: {err}")
        return jsonify({"error": str(err)}), 500

    finally:
        cursor.close()
        connection.close()

@app.route('/delete_police_station_data', methods=['POST'])
def delete_police_station_data():
    data = request.get_json()
    user_email = data.get('user_email')

    if not user_email:
        return jsonify({"error": "User email is required"}), 400

    connection = get_db_connection()
    if connection is None:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = connection.cursor()

        delete_query = """
            DELETE e, o, cr, a, c
            FROM tbl_cases c
            LEFT JOIN tbl_police_station ps ON c.police_station_id = ps.police_station_id
            LEFT JOIN tbl_arrests a ON c.case_id = a.case_id
            LEFT JOIN tbl_criminals cr ON a.criminal_id = cr.criminal_id
            LEFT JOIN tbl_officers o ON a.officer_id = o.officer_id
            LEFT JOIN tbl_evidence e ON c.case_id = e.case_id
            WHERE c.user_email = %s
        """

        cursor.execute(delete_query, (user_email,))
        connection.commit()

        if cursor.rowcount == 0:
            return jsonify({"message": "No data found for the provided user email."}), 404

        return jsonify({"message": "Records deleted successfully for the provided user email."}), 200

    except mysql.connector.Error as err:
        print(f"Database Error: {err}")
        return jsonify({"error": str(err)}), 500
    finally:
        cursor.close()
        connection.close()

@app.route('/delete_fire_station_data', methods=['POST'])
def delete_fire_station_data():
    data = request.get_json()
    complain_mail = data.get('complain_mail')  

    if not complain_mail:
        return jsonify({"error": "Complain email is required"}), 400

    connection = get_db_connection()
    if connection is None:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = connection.cursor()

        delete_query = """
            DELETE em, eq, ff, i, d
            FROM tbl_fire_station fs
            LEFT JOIN tbl_dispatches d ON fs.fire_station_id = d.fire_station_id
            LEFT JOIN tbl_incidents i ON d.incident_id = i.incident_id
            LEFT JOIN tbl_firefighters ff ON d.firefighter_id = ff.firefighter_id
            LEFT JOIN tbl_equipment eq ON fs.fire_station_id = eq.fire_station_id
            LEFT JOIN tbl_equipment_maintenance em ON eq.equipment_id = em.equipment_id
            WHERE i.complain_mail = %s
        """

        cursor.execute(delete_query, (complain_mail,))
        connection.commit()

        if cursor.rowcount == 0:
            return jsonify({"message": "No data found for the provided complain email."}), 404

        return jsonify({"message": "Fire station data and related records deleted successfully."}), 200

    except mysql.connector.Error as err:
        print(f"Database Error: {err}")
        return jsonify({"error": str(err)}), 500

    finally:
        cursor.close()
        connection.close()

# Update Modules Data

@app.route('/update_hospital_history', methods=['PUT'])
def update_hospital_history():
    connection = get_db_connection()
    if connection is None:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = connection.cursor()
        data = request.get_json()

        # Required fields (roomNumber removed)
        required_fields = [
            'email', 'fullname', 'contactNumber',
            'patient_address', 'diseases', 'age', 'gender'
        ]
        if not all(field in data for field in required_fields):
            return jsonify({"error": "Missing required fields"}), 400

        # Update query with JOIN to tbl_hospital (for hospital_id match)
        update_query = """
        UPDATE tbl_pdemo p
        JOIN tbl_hospital h ON h.hospital_id = p.hospital_id
        SET 
            p.fullname = %s,
            p.contactNumber = %s,
            p.patient_address = %s,
            p.diseases = %s,
            p.age = %s,
            p.gender = %s
        WHERE 
            p.email = %s;
        """

        cursor.execute(update_query, (
            data['fullname'],
            data['contactNumber'],
            data['patient_address'],
            data['diseases'],
            data['age'],
            data['gender'],
            data['email']
        ))

        connection.commit()

        if cursor.rowcount > 0:
            return jsonify({"message": "Record updated successfully"}), 200
        else:
            return jsonify({"message": "No matching record found"}), 404

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

@app.route('/update_fire_station_history', methods=['PUT'])
def update_fire_station_history():
    connection = get_db_connection()
    if connection is None:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = connection.cursor()
        data = request.get_json()

        # Required fields
        required_fields = [
            'complain_mail',
            'firefighter_name',
            'firefighter_rank',
            'firefighter_badge_number'
        ]
        if not all(field in data for field in required_fields):
            return jsonify({"error": "Missing required fields"}), 400

        # Update query using complain_mail to join to incident, dispatches, and firefighter
        update_query = """
        UPDATE tbl_firefighters ff
        JOIN tbl_dispatches d ON ff.firefighter_id = d.firefighter_id
        JOIN tbl_incidents i ON d.incident_id = i.incident_id
        SET 
            ff.firefighter_name = %s,
            ff.firefighter_rank = %s,
            ff.firefighter_badge_number = %s
        WHERE 
            i.complain_mail = %s;
        """

        cursor.execute(update_query, (
            data['firefighter_name'],
            data['firefighter_rank'],
            data['firefighter_badge_number'],
            data['complain_mail']
        ))

        connection.commit()

        if cursor.rowcount > 0:
            return jsonify({"message": "Firefighter record updated successfully"}), 200
        else:
            return jsonify({"message": "No matching firefighter record found for this complain_mail"}), 404

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

@app.route('/update_police_station_history', methods=['PUT'])
def update_police_station_history():
    connection = get_db_connection()
    if connection is None:
        return jsonify({"error": "Database connection failed"}), 500

    data = request.get_json()
    user_email = data.get("user_email")
    officer_name = data.get("officer_name")
    officer_rank = data.get("officer_rank")
    officer_badge_number = data.get("officer_badge_number")

    if not user_email:
        return jsonify({"error": "User email is required to update history"}), 400

    try:
        cursor = connection.cursor()

        # Update officer info for the user's police station case history
        update_query = """
        UPDATE tbl_officers o
        JOIN tbl_arrests a ON o.officer_id = a.officer_id
        JOIN tbl_cases c ON a.case_id = c.case_id
        SET o.officer_name = %s,
            o.officer_rank = %s,
            o.officer_badge_number = %s
        WHERE c.user_email = %s
        """
        cursor.execute(update_query, (
            officer_name,
            officer_rank,
            officer_badge_number,
            user_email
        ))
        connection.commit()

        if cursor.rowcount > 0:
            return jsonify({"message": "✅ Officer history updated successfully"}), 200
        else:
            return jsonify({"message": "⚠️ No matching record found for the given user_email"}), 404

    except mysql.connector.Error as db_err:
        app.logger.error(f"Database error: {db_err}")
        return jsonify({"error": f"Database error: {db_err}"}), 500

    except Exception as err:
        app.logger.error(f"Unexpected error: {err}")
        return jsonify({"error": f"Unexpected error: {err}"}), 500

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

@app.route('/update_pet_owner_info', methods=['PUT'])
def update_pet_owner_info():
    data = request.get_json()
    connection = get_db_connection()

    if connection is None:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = connection.cursor()

        owner_email = data.get("owner_email")

        if not owner_email:
            return jsonify({"error": "owner_email is required"}), 400

        # New update values
        owner_name = data.get("owner_name")
        owner_phone = data.get("owner_phone")
        new_owner_email = data.get("new_owner_email") or owner_email

        pet_name = data.get("pet_name")
        pet_species = data.get("pet_species")
        pet_breed = data.get("pet_breed")
        pet_age = data.get("pet_age")

        # Update owner info where pet_hospital_id matches internally
        update_owner_query = """
            UPDATE tbl_owner o
            JOIN tbl_pets p ON o.owner_id = p.owner_id
            JOIN tbl_pet_hospital h ON h.pet_hospital_id = p.pet_hospital_id
            SET o.owner_name = %s,
                o.owner_phone = %s,
            WHERE o.owner_email = %s
        """
        cursor.execute(update_owner_query, (owner_name, owner_phone, new_owner_email, owner_email))

        # Update pet info for same owner and linked pet_hospital
        update_pet_query = """
            UPDATE tbl_pets p
            JOIN tbl_owner o ON p.owner_id = o.owner_id
            JOIN tbl_pet_hospital h ON h.pet_hospital_id = p.pet_hospital_id
            SET p.pet_name = %s,
                p.pet_species = %s,
                p.pet_breed = %s,
                p.pet_age = %s
            WHERE o.owner_email = %s
        """
        cursor.execute(update_pet_query, (
            pet_name,
            pet_species,
            pet_breed,
            pet_age,
            new_owner_email
        ))

        connection.commit()
        return jsonify({"message": "✅ Owner and Pet information updated successfully"}), 200

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

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)