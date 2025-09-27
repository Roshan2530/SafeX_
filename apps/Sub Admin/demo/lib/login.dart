import 'package:demo/hospital/hospitalhomepage.dart';
import 'package:demo/pet%20hospital/pethomepage.dart';
import 'package:demo/police%20station/policehomepage.dart';
import 'package:demo/subadmin_themenotifire.dart';
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'api service/api_common.dart';
import 'fire station/firestationhomepage.dart';

class Loginpage extends StatefulWidget {
  const Loginpage({Key? key}) : super(key: key);

  @override
  State<Loginpage> createState() => _LoginpageState();
}

class _LoginpageState extends State<Loginpage> {
  final GlobalKey<FormState> _formKey = GlobalKey<FormState>();
  final TextEditingController _emailController = TextEditingController();
  final TextEditingController _passwordController = TextEditingController();
  bool _isLoading = false;
  bool _obscurePassword = true;

  void _login() async {
    if (!_formKey.currentState!.validate()) return; // Validate the form first

    setState(() {
      _isLoading = true; // Show loading indicator
    });

    final email = _emailController.text;
    final password = _passwordController.text;

    try {
      // Call the updated login API
      final response = await ApiService().loginUser(email, password);

      if (response["success"] == true) {
        // If login is successful, show success message
        _showSnackBar(context, response["message"], Colors.green);

        // Retrieve the user's table (or role) from the response
        final String userTable = response["table"]; // Ensure your API returns this key

        // Navigate to different pages based on the table value
        if (userTable == "tbl_police_login") {
          Navigator.pushReplacement(
            context,
            MaterialPageRoute(builder: (context) => policehomepage()),
          );
        } else if (userTable == "tbl_pet_hospital_login") {
          Navigator.pushReplacement(
            context,
            MaterialPageRoute(builder: (context) => pethomepage()),
          );
        } else if (userTable == "tbl_fire_station_login") {
          Navigator.pushReplacement(
            context,
            MaterialPageRoute(builder: (context) => firestationhomepage()),
          );
        } else {
          // Fallback if none of the expected tables match
          Navigator.pushReplacement(
            context,
            MaterialPageRoute(builder: (context) => Homepage()),
          );
        }
      } else {
        // If there is an error, show the error message
        _showSnackBar(context, response["error"], Colors.red);
      }
    } catch (e) {
      // Handle any unexpected errors (e.g., network issues)
      debugPrint("Error during login: $e");
      _showSnackBar(context, "An error occurred: $e", Colors.red);
    } finally {
      setState(() {
        _isLoading = false; // Hide loading indicator after the request is completed
      });
    }
  }

  void _showSnackBar(BuildContext context, String message, Color color) {
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(
        content: Text(message),
        backgroundColor: color,
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    // Access the current theme mode
    final themeMode = Provider.of<ThemeNotifier>(context).themeMode;
    final isDarkMode = themeMode == ThemeMode.dark;

    return Scaffold(
      backgroundColor: isDarkMode ? Colors.black : Colors.white,
      body: SingleChildScrollView(
        child: Stack(
          children: [
            // Background Image
            Center(
              child: isDarkMode
                  ? Image.asset(
                'assets/image/dark_background.jpg',
                fit: BoxFit.cover,
                height: MediaQuery.of(context).size.height,
                width: MediaQuery.of(context).size.width,
              )
                  : Image.asset(
                'assets/image/background.png',
                fit: BoxFit.cover,
                height: MediaQuery.of(context).size.height,
                width: MediaQuery.of(context).size.width,
              ),
            ),
            // Login Form
            Center(
              child: SingleChildScrollView(
                child: Padding(
                  padding: const EdgeInsets.only(top: 200.0),
                  child: Form(
                    key: _formKey,
                    child: Column(
                      mainAxisSize: MainAxisSize.min,
                      children: [
                        // Title
                        Text(
                          "Welcome Back",
                          style: TextStyle(
                            fontSize: 24,
                            color: isDarkMode ? Colors.white : Color(0xFFED1F2F),
                            fontWeight: FontWeight.bold,
                          ),
                        ),
                        SizedBox(height: 10),
                        Text(
                          "Log in to continue",
                          style: TextStyle(
                            fontSize: 16,
                            color: isDarkMode ? Colors.white70 : Colors.black,
                          ),
                        ),
                        SizedBox(height: 30),
                        // Card for Login Form
                        Padding(
                          padding: const EdgeInsets.all(20.0),
                          child: Column(
                            children: [
                              // Email Field
                              Card(
                                color: isDarkMode ? Colors.grey[800] : Colors.white,
                                child: TextFormField(
                                  controller: _emailController,
                                  decoration: InputDecoration(
                                    labelText: "Email",
                                    hintText: "Enter your email",
                                    prefixIcon: Icon(Icons.email, color: Color(0xFFED1F2F)),
                                    border: OutlineInputBorder(
                                      borderRadius: BorderRadius.circular(15),
                                    ),
                                  ),
                                  keyboardType: TextInputType.emailAddress,
                                  validator: (value) {
                                    if (value == null || value.isEmpty) {
                                      return "Please enter your email";
                                    } else if (!RegExp(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$").hasMatch(value)) {
                                      return "Enter a valid email address";
                                    }
                                    return null;
                                  },
                                ),
                              ),
                              SizedBox(height: 20),
                              // Password Field
                              Card(
                                color: isDarkMode ? Colors.grey[800] : Colors.white,
                                child: TextFormField(
                                  controller: _passwordController,
                                  obscureText: _obscurePassword,
                                  decoration: InputDecoration(
                                    labelText: "Password",
                                    hintText: "Enter your password",
                                    prefixIcon: Icon(Icons.lock, color: Color(0xFFED1F2F)),
                                    suffixIcon: IconButton(
                                      icon: Icon(
                                        _obscurePassword ? Icons.visibility_off : Icons.visibility,
                                        color: Color(0xFFED1F2F),
                                      ),
                                      onPressed: () {
                                        setState(() {
                                          _obscurePassword = !_obscurePassword;
                                        });
                                      },
                                    ),
                                    border: OutlineInputBorder(
                                      borderRadius: BorderRadius.circular(15),
                                    ),
                                  ),
                                  validator: (value) {
                                    if (value == null || value.isEmpty) {
                                      return "Please enter your password";
                                    } else if (value.length < 6) {
                                      return "Password must be at least 6 characters long";
                                    }
                                    return null;
                                  },
                                ),
                              ),
                              SizedBox(height: 30),
                              // Login Button
                              ElevatedButton(
                                onPressed: _login,
                                style: ElevatedButton.styleFrom(
                                  backgroundColor: Color(0xFFED1F2F),
                                  padding: EdgeInsets.symmetric(horizontal: 100, vertical: 15),
                                  shape: RoundedRectangleBorder(
                                    borderRadius: BorderRadius.circular(15),
                                  ),
                                ),
                                child: Text(
                                  _isLoading ? "Logging in..." : "Log In",
                                  style: TextStyle(fontSize: 16, color: Colors.white),
                                ),
                              ),
                            ],
                          ),
                        ),





                      ],
                    ),
                  ),
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}

