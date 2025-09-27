<?php
$host = "localhost";
$user = "root";
$pass = "";
$dbname = "user_data";

$conn = new mysqli($host, $user, $pass, $dbname);
if ($conn->connect_error) {
  die("Connection failed: " . $conn->connect_error);
}

$user_id = 31;
$lat = $_GET['lat'] ?? '';
$lon = $_GET['lon'] ?? '';
$hospital_id = 9;
$device = 'IOT';

$sql = "INSERT INTO tbl_hospital_dashboard (user_id, lat, log, hospital_id, device)
        VALUES ('$user_id', '$lat', '$lon', '$hospital_id', '$device')";

if ($conn->query($sql) === TRUE) {
  echo "Success";
} else {
  echo "Error: " . $conn->error;
}
$conn->close();
?>