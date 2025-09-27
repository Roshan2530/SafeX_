from http.client import HTTPException
import uuid
from flask import Flask, jsonify, request
from flask_cors import CORS
import mysql.connector
import time
import os
import base64
import random
import smtplib
from werkzeug.utils import secure_filename

app = Flask(__name__)
CORS(app)

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_ADDRESS = "safex728@gmail.com"  # Replace with your email address
EMAIL_PASSWORD = "cjfe bozj hugi ftnp"  # Replace with your email app password

# In-memory OTP store (for testing purposes)
otp_store = {}
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

#Authentication
@app.route('/signup', methods=['POST'])
def add_user():
    connection = get_db_connection()
    if connection is None:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        # Check if a file is in the request
        if 'profileimg' not in request.files or 'adharimg' not in request.files:
            return jsonify({"error": "Both profile image and Aadhaar image are required"}), 400

        profile_file = request.files['profileimg']
        adhar_file = request.files['adharimg']

        # Check if a file is selected
        if profile_file.filename == '' or adhar_file.filename == '':
            return jsonify({"error": "Both profile image and Aadhaar image must be selected"}), 400

        # Secure the filename
        profileimgname = secure_filename(profile_file.filename)
        adharimgname = secure_filename(adhar_file.filename)

        # Check image size
        MAX_IMAGE_SIZE = 16 * 1024 * 1024  # 16 MB
        if len(profile_file.read()) > MAX_IMAGE_SIZE or len(adhar_file.read()) > MAX_IMAGE_SIZE:
            return jsonify({"error": "Image size exceeds the limit of 16 MB"}), 400

        # Read the files after checking the size
        profile_file.seek(0)  # Reset file pointer after reading for size check
        profileimg = profile_file.read()
        adhar_file.seek(0)  # Reset file pointer after reading for size check
        adharimg = adhar_file.read()

        # Parse JSON data from the request
        try:
            data = request.form
            username = data.get('username')
            email = data.get('email')
            password = data.get('password')
            address = data.get('address')
            phone = data.get('phone')
            age = data.get('age')
            dob = data.get('dob')
            adharnumber = data.get('adharnumber')
        except Exception as e:
            return jsonify({"error": "Invalid input data"}), 400

        # Validate inputs
        required_fields = [username, email, password, address, phone, age, dob, adharnumber, profileimgname, adharimgname]
        if not all(required_fields):
            return jsonify({"error": "All fields (username, email, password, address, phone, age, dob, adharnumber, profileimgname, adharimgname) are required"}), 400

        # Execute INSERT query
        cursor = connection.cursor()
        query = """
            INSERT INTO tbl_user (username, email, password, address, phone, age, dob, adharnumber, profileimgname, profileimg, adharimg) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (username, email, password, address, phone, age, dob, adharnumber, profileimgname, profileimg, adharimg))
        connection.commit()

        return jsonify({"message": "User added successfully!"}), 201
    except mysql.connector.Error as err:
        app.logger.error(f"Error adding user: {err}")
        return jsonify({"error": str(err)}), 500
    except Exception as e:
        app.logger.error(f"Unexpected error: {e}")
        return jsonify({"error": "An unexpected error occurred"}), 500
    finally:
        if 'cursor' in locals():
            cursor.close()
        if connection:
            connection.close()



@app.route('/auth', methods=['POST'])
def authenticate():
    connection = get_db_connection()
    if connection is None:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = connection.cursor(dictionary=True)
        data = request.json
        action = data.get('action')
        email = data.get('email')
        
        if not email:
            return jsonify({"error": "Email is required"}), 400

        if action == "login":
            password = data.get('password')
            if not password:
                return jsonify({"error": "Password is required"}), 400
            
            # Validate user credentials
            query = "SELECT email FROM tbl_user WHERE email = %s AND password = %s"
            cursor.execute(query, (email, password))
            user = cursor.fetchone()
            
            if not user:
                return jsonify({"error": "Invalid email or password"}), 401
            
            # Generate OTP
            otp = random.randint(100000, 999999)
            otp_store[email] = {
                'otp': otp,
                'timestamp': time.time()
            }

            return jsonify({"message": "OTP generated successfully", "otp": otp}), 200  # Return OTP for testing
        
        elif action == "verify-otp":
            received_otp = data.get('otp')
            if not received_otp:
                return jsonify({"error": "OTP is required"}), 400
            
            if email not in otp_store:
                return jsonify({"error": "OTP not found or expired"}), 400
            
            stored_otp_data = otp_store[email]
            stored_otp = stored_otp_data['otp']
            timestamp = stored_otp_data['timestamp']

            if time.time() - timestamp > 300:
                del otp_store[email]
                return jsonify({"error": "OTP has expired"}), 400

            if int(received_otp) == stored_otp:
                del otp_store[email]
                return jsonify({"message": "OTP verified successfully"}), 200
            else:
                return jsonify({"error": "Invalid OTP"}), 400
        
        else:
            return jsonify({"error": "Invalid action"}), 400

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


def send_otp_email(from_email, to_email, otp):
    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.set_debuglevel(1)  # Enable debugging for SMTP
            server.starttls()
            server.login(from_email, EMAIL_PASSWORD)
            subject = "Your OTP Code"
            body = f"Your OTP code is: {otp}"
            message = f"Subject: {subject}\n\n{body}"
            server.sendmail(from_email, to_email, message)
            app.logger.info(f"OTP sent successfully to {to_email}")
    except Exception as e:
        app.logger.error(f"Error sending OTP: {e}")
        raise Exception(f"Failed to send OTP: {e}")

@app.route('/send-otp-login', methods=['POST'])
def send_otp_login():
    try:
        # Extract the receiver's email from the request
        data = request.json
        receiver_email = data.get('email')
        password = data.get('password')

        if not receiver_email:
            return jsonify({"error": "Receiver email is required"}), 400

        # Connect to the database
        connection = get_db_connection()
        if connection is None:
            return jsonify({"error": "Database connection failed"}), 500

        # Check if the email exists in the database
        cursor = connection.cursor(dictionary=True)
        query = "SELECT email,password FROM tbl_user WHERE email = %s AND password=%s"
        cursor.execute(query, (receiver_email,password))
        user = cursor.fetchone()

        if not user:
            return jsonify({"error": "Check Email or Password"}), 404

        # Generate a 6-digit OTP
        otp = random.randint(100000, 999999)

        # Store OTP temporarily (along with expiration time)
        otp_store[receiver_email] = {
            'otp': otp,
            'timestamp': time.time()  # Store the time it was generated
        }

        # Send the OTP to the receiver's email
        send_otp_email(EMAIL_ADDRESS, receiver_email, otp)

        return jsonify({"message": f"OTP sent successfully to {receiver_email}"}), 200

    except Exception as e:
        app.logger.error(f"Error during OTP process: {e}")
        return jsonify({"error": str(e)}), 500

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

@app.route('/send-otp', methods=['POST'])
def send_otp():
    try:
        # Extract the receiver's email from the request
        data = request.json
        receiver_email = data.get('email')

        if not receiver_email:
            return jsonify({"error": "Receiver email is required"}), 400

        # Connect to the database
        connection = get_db_connection()
        if connection is None:
            return jsonify({"error": "Database connection failed"}), 500

        # Check if the email exists in the database
        cursor = connection.cursor(dictionary=True)
        query = "SELECT email FROM tbl_user WHERE email = %s"
        cursor.execute(query, (receiver_email,))
        user = cursor.fetchone()

        if  user:
            return jsonify({"error": "Email not found in the database"}), 404

        # Generate a 6-digit OTP
        otp = random.randint(100000, 999999)

        # Store OTP temporarily (along with expiration time)
        otp_store[receiver_email] = {
            'otp': otp,
            'timestamp': time.time()  # Store the time it was generated
        }

        # Send the OTP to the receiver's email
        send_otp_email(EMAIL_ADDRESS, receiver_email, otp)

        return jsonify({"message": f"OTP sent successfully to {receiver_email}"}), 200

    except Exception as e:
        app.logger.error(f"Error during OTP process: {e}")
        return jsonify({"error": str(e)}), 500

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

@app.route('/send-otp-forgot', methods=['POST'])
def send_otp_forgot():
    try:
        # Extract the receiver's email from the request
        data = request.json
        receiver_email = data.get('email')

        if not receiver_email:
            return jsonify({"error": "Receiver email is required"}), 400

        # Connect to the database
        connection = get_db_connection()
        if connection is None:
            return jsonify({"error": "Database connection failed"}), 500

        # Check if the email exists in the database
        cursor = connection.cursor(dictionary=True)
        query = "SELECT email FROM tbl_user WHERE email = %s"
        cursor.execute(query, (receiver_email,))
        user = cursor.fetchone()

        if not user:
            return jsonify({"error": "Email not found in the database"}), 404

        # Generate a 6-digit OTP
        otp = random.randint(100000, 999999)

        # Store OTP temporarily (along with expiration time)
        otp_store[receiver_email] = {
            'otp': otp,
            'timestamp': time.time()  # Store the time it was generated
        }

        # Send the OTP to the receiver's email
        send_otp_email(EMAIL_ADDRESS, receiver_email, otp)

        return jsonify({"message": f"OTP sent successfully to {receiver_email}"}), 200

    except Exception as e:
        app.logger.error(f"Error during OTP process: {e}")
        return jsonify({"error": str(e)}), 500

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

@app.route('/update_password', methods=['PUT'])
def update_password():
    connection = get_db_connection()
    if connection is None:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = connection.cursor(dictionary=True)
        data = request.json
        email = data.get('email')
        old_password = data.get('old_password')
        new_password = data.get('new_password')

        if not email or not old_password or not new_password:
            return jsonify({"error": "Email, old password, and new password are required"}), 400

        # Fetch user from the database
        query = "SELECT password FROM tbl_user WHERE email = %s"
        cursor.execute(query, (email,))
        user = cursor.fetchone()

        if user:
            # Check if the old password matches the one stored in the database
            if user['password'] == old_password:
                # Update the password in the database
                update_query = "UPDATE tbl_user SET password = %s WHERE email = %s"
                cursor.execute(update_query, (new_password, email))
                connection.commit()

                if cursor.rowcount > 0:
                    return jsonify({"message": "Password updated successfully!"}), 200
                else:
                    return jsonify({"error": "Password update failed"}), 500
            else:
                return jsonify({"error": "Old password is incorrect"}), 401
        else:
            return jsonify({"error": "User not found"}), 404

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

@app.route('/reset_password', methods=['POST'])
def reset_password():
    connection = get_db_connection()
    if connection is None:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        # Get data from request
        data = request.json
        email = data.get('email')
        new_password = data.get('new_password')

        if not email or not new_password:
            return jsonify({"error": "Email and new password are required"}), 400

        # Connect to the database and check if the user exists with the provided email
        cursor = connection.cursor(dictionary=True)
        
        # Use parameterized query to prevent SQL injection
        query = "SELECT email FROM tbl_user WHERE email = %s"
        cursor.execute(query, (email,))
        
        user = cursor.fetchone()  # Use fetchone to get a single result

        if not user:
            return jsonify({"error": "Invalid email"}), 401

        # Update the password in the database
        update_query = "UPDATE tbl_user SET password = %s WHERE email = %s"
        cursor.execute(update_query, (new_password, email))
        connection.commit()

        return jsonify({"message": "Password updated successfully!"}), 200

    except mysql.connector.Error as err:
        app.logger.error(f"Error updating password: {err}")
        return jsonify({"error": str(err)}), 500
    finally:
        cursor.close()
        connection.close()




#Profile Page
@app.route('/fetchuser', methods=['GET'])
def fetch_user():
    connection = get_db_connection()
    if connection is None:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = connection.cursor(dictionary=True)
        email = request.args.get('email')

        if not email:
            return jsonify({"error": "Email is required to fetch user details"}), 400

        # Fetch user details
        query = "SELECT email, username, phone, address, dob, profileimg FROM tbl_user WHERE email = %s"
        cursor.execute(query, (email,))
        user = cursor.fetchone()

        if not user:
            return jsonify({"error": "User not found"}), 404

        # Convert binary profile image to Base64 string
        if user.get('profileimg'):
            user['profileimg'] = base64.b64encode(user['profileimg']).decode('utf-8')

        return jsonify({"user": user}), 200

    except mysql.connector.Error as err:
        app.logger.error(f"Database error: {err}")
        return jsonify({"error": "An error occurred while fetching user data"}), 500

    except Exception as e:
        app.logger.error(f"Unexpected error: {e}")
        return jsonify({"error": "An unexpected error occurred"}), 500

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

@app.route('/update_username', methods=['PUT'])
def update_username():
    connection = get_db_connection()
    if connection is None:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = connection.cursor(dictionary=True)
        data = request.json
        email = data.get('email')
        new_username = data.get('username')

        if not email or not new_username:
            return jsonify({"error": "Email and new username are required"}), 400

        # Use parameterized query to update the username
        update_query = "UPDATE tbl_user SET username = %s WHERE email = %s"
        cursor.execute(update_query, (new_username, email))
        connection.commit()

        if cursor.rowcount > 0:
            return jsonify({"message": "Username updated successfully!"}), 200
        else:
            return jsonify({"error": "User not found or update failed"}), 404

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

@app.route('/update_phone', methods=['PUT'])
def update_phone():
    connection = get_db_connection()
    if connection is None:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = connection.cursor(dictionary=True)
        data = request.json
        email = data.get('email')
        new_phone = data.get('phone')

        if not email or not new_phone:
            return jsonify({"error": "Email and new phone are required"}), 400

        # Use parameterized query to update the phone
        update_query = "UPDATE tbl_user SET phone = %s WHERE email = %s"
        cursor.execute(update_query, (new_phone, email))
        connection.commit()

        if cursor.rowcount > 0:
            return jsonify({"message": "Phone updated successfully!"}), 200
        else:
            return jsonify({"error": "User not found or update failed"}), 404

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

@app.route('/update_address', methods=['PUT'])
def update_address():
    connection = get_db_connection()
    if connection is None:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = connection.cursor(dictionary=True)
        data = request.json
        email = data.get('email')
        new_phone = data.get('address')

        if not email or not new_phone:
            return jsonify({"error": "Email and new address are required"}), 400

        # Use parameterized query to update the phone
        update_query = "UPDATE tbl_user SET address = %s WHERE email = %s"
        cursor.execute(update_query, (new_phone, email))
        connection.commit()

        if cursor.rowcount > 0:
            return jsonify({"message": "address updated successfully!"}), 200
        else:
            return jsonify({"error": "User not found or update failed"}), 404

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

@app.route('/update_dob', methods=['PUT'])
def update_dob():
    connection = get_db_connection()
    if connection is None:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = connection.cursor(dictionary=True)
        data = request.json
        email = data.get('email')
        new_phone = data.get('dob')

        if not email or not new_phone:
            return jsonify({"error": "Email and new Date of Birth are required"}), 400

        # Use parameterized query to update the phone
        update_query = "UPDATE tbl_user SET dob = %s WHERE email = %s"
        cursor.execute(update_query, (new_phone, email))
        connection.commit()

        if cursor.rowcount > 0:
            return jsonify({"message": "Date of Birth updated successfully!"}), 200
        else:
            return jsonify({"error": "User not found or update failed"}), 404

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

@app.route('/update_profile_image', methods=['PUT'])
def update_profile_image():
    connection = get_db_connection()
    if connection is None:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = connection.cursor(dictionary=True)
        data = request.json
        email = data.get('email')
        profile_image_base64 = data.get('profileimage')

        if not email or not profile_image_base64:
            return jsonify({"error": "Email and profile image are required"}), 400

        # Decode the Base64 profile image
        try:
            profile_image_bytes = base64.b64decode(profile_image_base64)
        except Exception as e:
            app.logger.error(f"Error decoding Base64 image: {e}")
            return jsonify({"error": "Invalid profile image format"}), 400

        # Use parameterized query to update the profile image
        update_query = "UPDATE tbl_user SET profileimg = %s WHERE email = %s"
        cursor.execute(update_query, (profile_image_bytes, email))
        connection.commit()

        if cursor.rowcount > 0:
            return jsonify({"message": "Profile image updated successfully!"}), 200
        else:
            return jsonify({"error": "User not found or update failed"}), 404

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


#Entities List
@app.route('/get_users_hospital', methods=['GET'])
def get_users_hospital():
    connection = get_db_connection()
    if connection is None:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT hospital_id,hospital_name,hospital_address,hospital_email,hospital_password,hospital_password,hospital_number,lat,log,link FROM tbl_hospital")
        users = cursor.fetchall()
        return jsonify({"users": users}), 200
    except mysql.connector.Error as err:
        app.logger.error(f"Error fetching users: {err}")
        return jsonify({"error": str(err)}), 500
    finally:
        cursor.close()
        connection.close()


@app.route('/get_users_fire_station', methods=['GET'])
def get_users_fire_station():
    connection = get_db_connection()
    if connection is None:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT fire_station_id,fire_station_name,fire_station_address,fire_station_email,fire_station_password,fire_station_number,lat,log,link FROM tbl_fire_station")
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
        cursor.execute("SELECT police_station_id,police_station_name,police_station_address,police_station_email,police_station_password,police_station_number,lat,log,link FROM tbl_police_station")
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
        cursor.execute("SELECT pet_hospital_id,pet_hospital_name,pet_hospital_address,pet_hospital_email,pet_hospital_password,pet_hospital_number,lat,log,link FROM tbl_pet_hospital")
        users = cursor.fetchall()
        return jsonify({"users": users}), 200
    except mysql.connector.Error as err:
        app.logger.error(f"Error fetching users: {err}")
        return jsonify({"error": str(err)}), 500
    finally:
        cursor.close()
        connection.close()


#Entities History
@app.route('/history_hospital', methods=['GET'])
def history_hospital():
    connection = get_db_connection()
    if connection is None:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = connection.cursor(dictionary=True)

        # Get email and search query from query parameters
        email = request.args.get('email')
        search = request.args.get('search', '')

        if not email:
            return jsonify({"error": "Email is required to fetch user details"}), 400

        # Base query
        query = """
        SELECT 
            p.fullname, p.dob, p.age, p.gender, p.contactNumber, p.patient_address, p.diseases, p.admitDate,
            h.hospital_name, h.hospital_address, h.hospital_number, h.hospital_email,
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
            p.email = %s
        """
        
        params = [email]
        
        # Add search functionality if search query is provided
        if search:
            search_query = """
            AND (
                p.fullname LIKE %s OR
                p.contactNumber LIKE %s OR
                p.diseases LIKE %s OR
                h.hospital_name LIKE %s OR
                d.doctorName LIKE %s OR
                d.doctorSpeciality LIKE %s
            )
            """
            query += search_query
            search_param = f"%{search}%"
            params.extend([search_param] * 6)

        cursor.execute(query, tuple(params))
        records = cursor.fetchall()

        if records:
            app.logger.debug(f"Fetched records: {records}")
            return jsonify({"records": records}), 200
        else:
            app.logger.debug("No records found for email: %s with search: %s", email, search)
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

@app.route('/history_fire_station', methods=['GET'])
def history_fire_station():
    user_email = request.args.get('complain_mail')
    search = request.args.get('search', '')

    if not user_email:
        return jsonify({"error": "Missing 'complain_mail' parameter"}), 400

    connection = get_db_connection()
    if connection is None:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = connection.cursor(dictionary=True)

        # Base query
        query = """
        SELECT 
            i.incident_id,
            i.incident_member,
            i.incident_description,
            i.complain_mail,
            i.incident_type,
            i.incident_location,
            i.incident_date_reported,
            fs.fire_station_name,
            fs.fire_station_address,
            fs.fire_station_email
        FROM 
            tbl_incidents i
        LEFT JOIN 
            tbl_fire_station fs ON i.fire_station_id = fs.fire_station_id
        WHERE 
            i.complain_mail = %s
        """
        
        params = [user_email]

        # Add search functionality
        if search:
            search_query = """
            AND (
                i.incident_description LIKE %s OR
                i.incident_type LIKE %s OR
                i.incident_location LIKE %s OR
                fs.fire_station_name LIKE %s
            )
            """
            query += search_query
            search_param = f"%{search}%"
            params.extend([search_param] * 4)

        cursor.execute(query, tuple(params))
        records = cursor.fetchall()

        if records:
            return jsonify({"records": records}), 200
        else:
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
def history_police_station_station():
    user_email = request.args.get('user_email')
    search_query = request.args.get('search_query', '')

    if not user_email:
        return jsonify({"error": "Missing 'user_email' parameter"}), 400

    connection = get_db_connection()
    if connection is None:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = connection.cursor(dictionary=True)

        # Base query
        query = """
        SELECT 
            ps.police_station_name, 
            ps.police_station_address, 
            ps.police_station_email, 
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
            c.user_email = %s
        """

        params = [user_email]

        # Add search filter if provided
        if search_query:
            query += """ AND (
                ps.police_station_name LIKE %s OR
                ps.police_station_address LIKE %s OR
                ps.police_station_email LIKE %s OR
                c.case_number LIKE %s OR
                c.case_title LIKE %s OR
                cr.criminal_name LIKE %s OR
                o.officer_name LIKE %s
            )"""
            search_term = f"%{search_query}%"
            params.extend([search_term] * 7)

        cursor.execute(query, tuple(params))
        records = cursor.fetchall()

        return jsonify({"records": records}) if records else jsonify({"message": "No records found"}), 200

    except mysql.connector.Error as err:
        app.logger.error(f"Database error: {err}")
        return jsonify({"error": f"Database error: {err}"}), 500
    except Exception as e:
        app.logger.error(f"Unexpected error: {e}")
        return jsonify({"error": f"Unexpected error: {e}"}), 500
    finally:
        cursor.close()
        connection.close()

@app.route('/history_pet', methods=['GET'])
def history_pet_hospital():
    user_email = request.args.get('owner_email')
    search_query = request.args.get('search_query', '')

    if not user_email:
        return jsonify({"error": "Missing 'owner_email' parameter"}), 400

    connection = get_db_connection()
    if connection is None:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = connection.cursor(dictionary=True)

        # Base query
        query = """
        SELECT 
            o.owner_name, 
            o.owner_address, 
            o.owner_phone, 
            o.owner_email,
            p.pet_name, 
            p.pet_species, 
            p.pet_breed, 
            p.pet_age, 
            ph.pet_hospital_name, 
            ph.pet_hospital_address, 
            ph.pet_hospital_email,
            d.doc_name, 
            d.doc_specialization, 
            d.doc_phone, 
            d.doc_email,
            a.appointment_date, 
            a.appointment_reason, 
            a.appointment_description,
            m.diagnosis, 
            m.treatment, 
            m.prescription, 
            m.record_date
        FROM 
            tbl_owner o
        LEFT JOIN 
            tbl_pets p ON o.owner_id = p.owner_id
        LEFT JOIN 
            tbl_pet_hospital ph ON p.pet_hospital_id = ph.pet_hospital_id
        LEFT JOIN 
            tbl_appointments a ON p.pet_id = a.pet_id
        LEFT JOIN 
            tbl_doctor d ON a.doc_id = d.doc_id
        LEFT JOIN 
            tbl_medical_records m ON a.appointment_id = m.appointment_id
        WHERE 
            o.owner_email = %s
        """

        params = [user_email]

        # Add search filter if provided
        if search_query:
            query += """ AND (
                o.owner_name LIKE %s OR
                p.pet_name LIKE %s OR
                p.pet_species LIKE %s OR
                p.pet_breed LIKE %s OR
                ph.pet_hospital_name LIKE %s OR
                d.doc_name LIKE %s OR
                a.appointment_reason LIKE %s OR
                m.diagnosis LIKE %s
            )"""
            search_term = f"%{search_query}%"
            params.extend([search_term] * 8)

        cursor.execute(query, tuple(params))
        records = cursor.fetchall()

        return jsonify({"records": records}) if records else jsonify({"message": "No records found"}), 200

    except mysql.connector.Error as err:
        app.logger.error(f"Database error: {err}")
        return jsonify({"error": f"Database error: {err}"}), 500
    except Exception as e:
        app.logger.error(f"Unexpected error: {e}")
        return jsonify({"error": f"Unexpected error: {e}"}), 500
    finally:
        cursor.close()
        connection.close()


#Bill
@app.route('/add_bill', methods=['POST'])
def add_bill():
    connection = get_db_connection()
    if connection is None:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        # Parse JSON data from the request
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No data provided"}), 400

        # Extract required fields
        name = data.get('name')
        number = data.get('number')
        email = data.get('email')
        device_name = data.get('device_name')
        price = data.get('price')
        qty = data.get('qty')
        final_amt = data.get('final_amt')
        date = data.get('date')

        # Validate inputs
        if not all([name, number, email, device_name, price, qty, final_amt, date]):
            return jsonify({"error": "All fields (name, number, email, device_name, price, qty, final_amt, date) are required"}), 400

        # Execute INSERT query
        cursor = connection.cursor()
        query = """
            INSERT INTO tbl_user_bill (name, number, email, device_name, price, qty, final_amt, date) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (name, number, email, device_name, price, qty, final_amt, date))
        connection.commit()

        return jsonify({"message": "Bill added successfully!"}), 201

    except mysql.connector.Error as err:
        app.logger.error(f"Database error: {err}")
        return jsonify({"error": str(err)}), 500
    except Exception as e:
        app.logger.error(f"Unexpected error: {e}")
        return jsonify({"error": "An unexpected error occurred"}), 500
    finally:
        if 'cursor' in locals():
            cursor.close()
        if connection:
            connection.close()

@app.route('/getBill', methods=['GET'])
def get_bill():
    phone = request.args.get('phone')
    email = request.args.get('email')

    if not phone or not email:
        return jsonify({"error": "Missing 'phone' or 'email' parameter"}), 400

    connection = get_db_connection()
    if connection is None:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = connection.cursor(dictionary=True)
        query = """
        SELECT * FROM tbl_user_bill 
        WHERE number = %s AND email = %s 
        ORDER BY STR_TO_DATE(date, '%d/%m/%Y, %h:%i %p') DESC 
        LIMIT 1;
        """
        
        cursor.execute(query, (phone, email))
        bill = cursor.fetchone()

        return jsonify({"bill": bill}) if bill else jsonify({"message": "No bill found"}), 200

    except mysql.connector.Error as err:
        app.logger.error(f"Database error: {err}")
        return jsonify({"error": f"Database error: {err}"}), 500
    except Exception as e:
        app.logger.error(f"Unexpected error: {e}")
        return jsonify({"error": f"Unexpected error: {e}"}), 500
    finally:
        cursor.close()
        connection.close()

@app.route('/bill_history', methods=['GET'])
def history_bill():
    user_email = request.args.get('email')
    search_query = request.args.get('search_query', '')

    if not user_email:
        return jsonify({"error": "Missing 'email' parameter"}), 400

    connection = get_db_connection()
    if connection is None:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = connection.cursor(dictionary=True)

        # Base query
        query = """
        
        WHERE email = %s;
        """

        params = [user_email]

        # Add search filter if provided
        if search_query:
            query += """ AND (
                tbl_user_bill.email LIKE %s OR
                tbl_user_bill.name LIKE %s OR
                
            )"""
            search_term = f"%{search_query}%"
            params.extend([search_term] * 8)

        cursor.execute(query, tuple(params))
        records = cursor.fetchall()

        return jsonify({"records": records}) if records else jsonify({"message": "No records found"}), 200

    except mysql.connector.Error as err:
        app.logger.error(f"Database error: {err}")
        return jsonify({"error": f"Database error: {err}"}), 500
    except Exception as e:
        app.logger.error(f"Unexpected error: {e}")
        return jsonify({"error": f"Unexpected error: {e}"}), 500
    finally:
        cursor.close()
        connection.close()

#User_id
@app.route('/get_user_id_by_email', methods=['GET'])
def get_user_id_by_email():
    email = request.args.get("email")

    if not email:
        return jsonify({"error": "Email is required"}), 400

    connection = get_db_connection()
    if connection is None:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = connection.cursor(dictionary=True)
        query = "SELECT user_id FROM tbl_user WHERE email = %s"
        cursor.execute(query, (email,))
        result = cursor.fetchone()

        if result:
            return jsonify({"user_id": result["user_id"]}), 200
        else:
            return jsonify({"error": "User not found"}), 404

    except mysql.connector.Error as err:
        app.logger.error(f"Error fetching user_id: {err}")
        return jsonify({"error": str(err)}), 500
    finally:
        cursor.close()
        connection.close()

#SOS
@app.route('/insert_user_hospital', methods=['POST'])
def insert_user_hospital():
    data = request.get_json()

    user_id = data.get("user_id")
    lat = data.get("lat")
    log = data.get("log")
    hospital_id = data.get("hospital_id")  # New field

    if not all([user_id, lat, log, hospital_id]):
        return jsonify({"error": "Missing required fields"}), 400

    connection = get_db_connection()
    if connection is None:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = connection.cursor()
        query = "INSERT INTO tbl_hospital_dashboard (user_id, lat, log, hospital_id,device) VALUES (%s, %s, %s, %s,'APP')"
        cursor.execute(query, (user_id, lat, log, hospital_id))
        connection.commit()
        
        return jsonify({"message": "User linked to hospital successfully", "inserted_id": cursor.lastrowid}), 201
    except mysql.connector.Error as err:
        app.logger.error(f"Error inserting data: {err}")
        return jsonify({"error": str(err)}), 500
    finally:
        cursor.close()
        connection.close()

@app.route('/insert_user_pet_hospital', methods=['POST'])
def insert_user_pet_hospital():
    data = request.get_json()

    user_id = data.get("user_id")
    lat = data.get("lat")
    log = data.get("log")
    hospital_id = data.get("pet_hospital_id")  # New field

    if not all([user_id, lat, log, hospital_id]):
        return jsonify({"error": "Missing required fields"}), 400

    connection = get_db_connection()
    if connection is None:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = connection.cursor()
        query = "INSERT INTO tbl_pet_hospital_dashboard (user_id, lat, log, pet_hospital_id,device) VALUES (%s, %s, %s, %s,'APP')"
        cursor.execute(query, (user_id, lat, log, hospital_id))
        connection.commit()
        
        return jsonify({"message": "User linked to hospital successfully", "inserted_id": cursor.lastrowid}), 201
    except mysql.connector.Error as err:
        app.logger.error(f"Error inserting data: {err}")
        return jsonify({"error": str(err)}), 500
    finally:
        cursor.close()
        connection.close()

@app.route('/insert_user_fire_station', methods=['POST'])
def insert_user_fire_station():
    data = request.get_json()

    user_id = data.get("user_id")
    lat = data.get("lat")
    log = data.get("log")
    fire_station_id = data.get("fire_station_id")  # New field

    if not all([user_id, lat, log, fire_station_id]):
        return jsonify({"error": "Missing required fields"}), 400

    connection = get_db_connection()
    if connection is None:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = connection.cursor()
        query = "INSERT INTO tbl_fire_station_dashboard (user_id, lat, log, fire_station_id,device) VALUES (%s, %s, %s, %s,'APP')"
        cursor.execute(query, (user_id, lat, log, fire_station_id))
        connection.commit()
        
        return jsonify({"message": "User linked to hospital successfully", "inserted_id": cursor.lastrowid}), 201
    except mysql.connector.Error as err:
        app.logger.error(f"Error inserting data: {err}")
        return jsonify({"error": str(err)}), 500
    finally:
        cursor.close()
        connection.close()

@app.route('/insert_user_police_station', methods=['POST'])
def insert_user_police_station():
    data = request.get_json()

    user_id = data.get("user_id")
    lat = data.get("lat")
    log = data.get("log")
    police_station_id = data.get("police_station_id")  # New field

    if not all([user_id, lat, log, police_station_id]):
        return jsonify({"error": "Missing required fields"}), 400

    connection = get_db_connection()
    if connection is None:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = connection.cursor()
        query = "INSERT INTO tbl_police_station_dashboard (user_id, lat, log, police_station_id,device) VALUES (%s, %s, %s, %s,'APP')"
        cursor.execute(query, (user_id, lat, log, police_station_id))
        connection.commit()
        
        return jsonify({"message": "User linked to hospital successfully", "inserted_id": cursor.lastrowid}), 201
    except mysql.connector.Error as err:
        app.logger.error(f"Error inserting data: {err}")
        return jsonify({"error": str(err)}), 500
    finally:
        cursor.close()
        connection.close()


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)