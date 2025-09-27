import serial
import requests

arduino = serial.Serial('COM6', 9600)  # Update with your port
url = 'http://localhost/php/gpslocation/data_receiver.php'

while True:
    try:
        line = arduino.readline().decode().strip()
        
        if "SOS Activated" in line:
            print("Detected SOS")
            
            # Read next few lines and parse lat/lon
            lat_line = arduino.readline().decode().strip()
            lon_line = arduino.readline().decode().strip()
            
            lat = lat_line.split(": ")[1] if ": " in lat_line else "0"
            lon = lon_line.split(": ")[1] if ": " in lon_line else "0"

            # Optional: read and ignore other lines
            arduino.readline()
            arduino.readline()

            payload = {
                'lat': lat,
                'lon': lon,
                'sos': 'yes'
            }

            r = requests.get(url, params=payload)
            print("Sent:", payload, "| Response:", r.text)

    except Exception as e:
        print("Error:", e)
