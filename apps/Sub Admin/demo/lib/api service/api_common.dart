import 'dart:convert';
import 'package:http/http.dart' as http;

class ApiService {
  final String baseUrl = "http://192.168.139.155:5000";


  Future<Map<String, dynamic>> loginUser(String email, String password) async {
    final url = Uri.parse("$baseUrl/login"); // Update the URL to match the API endpoint

    try {
      final response = await http.post(
        url,
        headers: {"Content-Type": "application/json"},
        body: jsonEncode({
          "email": email, // Match the key expected by the API
          "password": password // Match the key expected by the API
        }),
      );

      if (response.statusCode == 200) {
        // Successful login
        final responseData = jsonDecode(response.body);
        return {
          "success": true,
          "message": responseData['message'],
          "table": responseData['table'] // Include the table name if needed
        };
      } else if (response.statusCode == 400 || response.statusCode == 401) {
        // Handle specific error cases
        final responseData = jsonDecode(response.body);
        return {
          "success": false,
          "error": responseData['error'] // Return the error message from the API
        };
      } else {
        // Handle other status codes
        return {
          "success": false,
          "error": "An unexpected error occurred. Status code: ${response.statusCode}"
        };
      }
    } catch (e) {
      // Handle network or other exceptions
      return {
        "success": false,
        "error": "An error occurred: $e"
      };
    }
  }


  Future<void> signup_fire_station(String name, String address, String email, String password,String number, String lat, String log, String link) async {
    final url = Uri.parse('$baseUrl/add');

    Map<String, dynamic> data = {
      'fire_station_name': name,
      'fire_station_address': address,
      'fire_station_email': email,
      'fire_station_password': password,
      'fire_station_number': number,
      'lat': lat,
      'log': log,
      'link': link,
    };

    try {
      final String jsonData = json.encode(data);

      final response = await http.post(
        url,
        headers: {'Content-Type': 'application/json'},
        body: jsonData,
      );

      // Debugging logs
      print("Response Status: ${response.statusCode}");
      print("Response Body: ${response.body}");

      if (response.statusCode == 201) {
        print("User added successfully!");
      } else {
        throw Exception("Failed to add user: ${response.reasonPhrase}");
      }
    } catch (e) {
      print("Error: $e");
      throw Exception("Error adding user: $e");
    }
  }

  Future<List<dynamic>> fetchUsers_fire_station() async {
    final String apiUrl = '$baseUrl/get_users_fire_station';

    try {
      final response = await http.get(Uri.parse(apiUrl));

      // Debugging logs
      print("Response Status: ${response.statusCode}");
      print("Response Body: ${response.body}");

      if (response.statusCode == 200) {
        final Map<String, dynamic> data = json.decode(response.body);
        return data['users'];
      } else {
        throw Exception('Failed to load users. Status code: ${response.statusCode}');
      }
    } catch (e) {
      print("Error: $e");
      throw Exception('Error fetching users: $e');
    }
  }


  Future<List<Map<String, dynamic>>?> fetchFireStationHistory(String email) async {
    final url = Uri.parse('$baseUrl/history_fire_station?fire_station_email=$email');
    try {
      final response = await http.get(url);

      if (response.statusCode == 200) {
        final jsonData = json.decode(response.body);

        // Adjust key to match the response structure from the API
        return List<Map<String, dynamic>>.from(jsonData['records']); // 'records' is the key in the API response
      } else {
        print('Failed to load data. Status code: ${response.statusCode}');
        return null;
      }
    } catch (e) {
      print('Error fetching data: $e');
      return null;
    }
  }


  Future<void> signup_hospital(String name, String address, String email, String password,String number, String lat, String log, String link) async {
    final url = Uri.parse('$baseUrl/add');

    Map<String, dynamic> data = {
      'hospital_name': name,
      'hospital_address': address,
      'hospital_email': email,
      'hospital_password': password,
      'hospital_number': number,
      'lat': lat,
      'log': log,
      'link': link,
    };

    try {
      final String jsonData = json.encode(data);

      final response = await http.post(
        url,
        headers: {'Content-Type': 'application/json'},
        body: jsonData,
      );

      // Debugging logs
      print("Response Status: ${response.statusCode}");
      print("Response Body: ${response.body}");

      if (response.statusCode == 201) {
        print("User added successfully!");
      } else {
        throw Exception("Failed to add user: ${response.reasonPhrase}");
      }
    } catch (e) {
      print("Error: $e");
      throw Exception("Error adding user: $e");
    }
  }

  Future<List<dynamic>> fetchUsers_hospital() async {
    final String apiUrl = '$baseUrl/get_users_hospital';

    try {
      final response = await http.get(Uri.parse(apiUrl));

      // Debugging logs
      print("Response Status: ${response.statusCode}");
      print("Response Body: ${response.body}");

      if (response.statusCode == 200) {
        final Map<String, dynamic> data = json.decode(response.body);
        return data['users'];
      } else {
        throw Exception('Failed to load users. Status code: ${response.statusCode}');
      }
    } catch (e) {
      print("Error: $e");
      throw Exception('Error fetching users: $e');
    }
  }



  Future<List<Map<String, dynamic>>?> fetchHospitalHistory_hospital(String email) async {
    final url = Uri.parse('$baseUrl/history_hospital?hospital_email=$email');
    try {
      final response = await http.get(url);

      if (response.statusCode == 200) {
        final jsonData = json.decode(response.body);

        // Adjust key to match the response structure from the API
        return List<Map<String, dynamic>>.from(jsonData['records']); // 'records' is the key in the API response
      } else {
        print('Failed to load data. Status code: ${response.statusCode}');
        return null;
      }
    } catch (e) {
      print('Error fetching data: $e');
      return null;
    }
  }

  Future<void> signup_pet_hospital(String name, String address, String email, String password,String number, String lat, String log, String link) async {
    final url = Uri.parse('$baseUrl/add');

    Map<String, dynamic> data = {
      'pet_hospital_name': name,
      'pet_hospital_address': address,
      'pet_hospital_email': email,
      'pet_hospital_password': password,
      'pet_hospital_number': number,
      'lat': lat,
      'log': log,
      'link': link,
    };

    try {
      final String jsonData = json.encode(data);

      final response = await http.post(
        url,
        headers: {'Content-Type': 'application/json'},
        body: jsonData,
      );

      // Debugging logs
      print("Response Status: ${response.statusCode}");
      print("Response Body: ${response.body}");

      if (response.statusCode == 201) {
        print("User added successfully!");
      } else {
        throw Exception("Failed to add user: ${response.reasonPhrase}");
      }
    } catch (e) {
      print("Error: $e");
      throw Exception("Error adding user: $e");
    }
  }

  Future<List<dynamic>> fetchUsers_pet_hospital() async {
    final String apiUrl = '$baseUrl/get_users_pet_hospital';

    try {
      final response = await http.get(Uri.parse(apiUrl));

      // Debugging logs
      print("Response Status: ${response.statusCode}");
      print("Response Body: ${response.body}");

      if (response.statusCode == 200) {
        final Map<String, dynamic> data = json.decode(response.body);
        return data['users'];
      } else {
        throw Exception('Failed to load users. Status code: ${response.statusCode}');
      }
    } catch (e) {
      print("Error: $e");
      throw Exception('Error fetching users: $e');
    }
  }



  Future<List<Map<String, dynamic>>?> fetchHistorypet_hospital(String email) async {
    final url = Uri.parse('$baseUrl/history_pet_hospital?pet_hospital_email=$email');
    try {
      final response = await http.get(url);

      if (response.statusCode == 200) {
        final jsonData = json.decode(response.body);

        // Adjust key to match the response structure from the API
        return List<Map<String, dynamic>>.from(jsonData['records']); // 'records' is the key in the API response
      } else {
        print('Failed to load data. Status code: ${response.statusCode}');
        return null;
      }
    } catch (e) {
      print('Error fetching data: $e');
      return null;
    }
  }

  Future<void> signup_police_station(String name, String address, String email, String password,String number, String lat, String log, String link) async {
    final url = Uri.parse('$baseUrl/add');

    Map<String, dynamic> data = {
      'police_station_name': name,
      'police_station_address': address,
      'police_station_email': email,
      'police_station_password': password,
      'police_station_number': number,
      'lat': lat,
      'log': log,
      'link': link,
    };

    try {
      final String jsonData = json.encode(data);

      final response = await http.post(
        url,
        headers: {'Content-Type': 'application/json'},
        body: jsonData,
      );

      // Debugging logs
      print("Response Status: ${response.statusCode}");
      print("Response Body: ${response.body}");

      if (response.statusCode == 201) {
        print("User added successfully!");
      } else {
        throw Exception("Failed to add user: ${response.reasonPhrase}");
      }
    } catch (e) {
      print("Error: $e");
      throw Exception("Error adding user: $e");
    }
  }

  Future<List<dynamic>> fetchUsers_police_station() async {
    final String apiUrl = '$baseUrl/get_users_police_station';

    try {
      final response = await http.get(Uri.parse(apiUrl));

      // Debugging logs
      print("Response Status: ${response.statusCode}");
      print("Response Body: ${response.body}");

      if (response.statusCode == 200) {
        final Map<String, dynamic> data = json.decode(response.body);
        return data['users'];
      } else {
        throw Exception('Failed to load users. Status code: ${response.statusCode}');
      }
    } catch (e) {
      print("Error: $e");
      throw Exception('Error fetching users: $e');
    }
  }



  Future<List<Map<String, dynamic>>?> fetchHistoryPoliceStation(String email) async {
    final url = Uri.parse('$baseUrl/history_police_station?police_station_email=$email');
    try {
      final response = await http.get(url);

      if (response.statusCode == 200) {
        final jsonData = json.decode(response.body);

        // Adjust key to match the response structure from the API
        return List<Map<String, dynamic>>.from(jsonData['records']); // 'records' is the key in the API response
      } else {
        print('Failed to load data. Status code: ${response.statusCode}');
        return null;
      }
    } catch (e) {
      print('Error fetching data: $e');
      return null;
    }
  }


}
