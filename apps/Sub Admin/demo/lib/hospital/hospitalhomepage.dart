import 'dart:async';
import 'package:demo/hospital/hospitaldetails.dart';
import 'package:demo/hospital/hospitallist.dart';
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:shared_preferences/shared_preferences.dart';
import '../api service/api_common.dart';
import '../login.dart';
import '../subadmin_themenotifire.dart';

class Homepage extends StatefulWidget {
  const Homepage({super.key});

  @override
  State<Homepage> createState() => _HomepageState();
}

class _HomepageState extends State<Homepage> {
  final GlobalKey<ScaffoldState> _scaffoldKey = GlobalKey<ScaffoldState>();
  final _formKey = GlobalKey<FormState>();
  final _hospitalNameController = TextEditingController();
  final _addressController = TextEditingController();
  final _latitudeController = TextEditingController();
  final _longitudeController = TextEditingController();
  final _mapLinkController = TextEditingController();
  final _emailController = TextEditingController();
  final _passwordController = TextEditingController();
  final _numberController = TextEditingController();
  final ApiService apiService = ApiService();
  bool isLoading = false;
  String _themeSelection = 'Light Theme';
  ThemeMode _themeMode = ThemeMode.light;


  @override
  void initState() {
    super.initState();
    _loadThemePreference(); // Load the theme preference when the page is created
  }

  Future<void> _loadThemePreference() async {
    SharedPreferences prefs = await SharedPreferences.getInstance();
    String? theme = prefs.getString('theme') ?? 'Light Theme';
    _setTheme(theme);
  }

  void _setTheme(String theme) async {
    setState(() {
      _themeSelection = theme;
      _themeMode = theme == 'Dark Theme' ? ThemeMode.dark : ThemeMode.light;
    });

    Provider.of<ThemeNotifier>(context, listen: false).setTheme(_themeMode);

    SharedPreferences prefs = await SharedPreferences.getInstance();
    prefs.setString('theme', theme);
  }


  Future<void> insert(String name, String address, String email, String password, String number, String lat, String log, String link) async {
    setState(() {
      isLoading = true;
    });

    try {
      await apiService.signup_hospital(name, address, email, password, number, lat, log, link);

      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text("Human Hospital added successfully!")),
      );

      // ✅ Clear all the fields after successful addition
      _hospitalNameController.clear();
      _addressController.clear();
      _emailController.clear();
      _passwordController.clear();
      _numberController.clear();
      _latitudeController.clear();
      _longitudeController.clear();
      _mapLinkController.clear();
    } catch (e) {
      debugPrint("Error adding Human Hospital : $e");
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text("Error adding Human Hospital : $e")),
      );
    } finally {
      setState(() {
        isLoading = false;
      });
    }
  }


  Future<void> signup() async {
    if (_formKey.currentState!.validate()) {
      await insert(
        _hospitalNameController.text,
        _addressController.text,
        _emailController.text,
        _passwordController.text,
        _numberController.text,
        _latitudeController.text,
        _longitudeController.text,
        _mapLinkController.text,
      );
    }
  }

  void _extractLatLong() {
    String mapLink = _mapLinkController.text;
    RegExp regExp = RegExp(r'!3d(-?\d+\.\d+)!4d(-?\d+\.\d+)');
    Match? match = regExp.firstMatch(mapLink);

    if (match != null) {
      setState(() {
        _latitudeController.text = match.group(1)!;  // Extracted Latitude
        _longitudeController.text = match.group(2)!; // Extracted Longitude
      });
    } else {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text("Invalid Google Maps link. Please enter a valid link.")),
      );
    }
  }


  @override
  Widget build(BuildContext context) {
    final themeData = Theme.of(context);
    final isDarkMode = themeData.brightness == Brightness.dark;
    return Scaffold(
      backgroundColor: isDarkMode ? themeData.colorScheme.background : Colors.white,
      key: _scaffoldKey,
      appBar: _buildAppBar(themeData),
      drawer: _drawer(),
      body: _addhumanhospital(),
    );
  }

  PreferredSizeWidget _buildAppBar(ThemeData themeData) {
    final isDarkMode = Theme.of(context).brightness == Brightness.dark;
    return PreferredSize(
      preferredSize: Size.fromHeight(150),
      child: SafeArea(
        child: Padding(
          padding: EdgeInsets.all(10),
          child: Container(
            height: 55,
            decoration: BoxDecoration(
              color: isDarkMode
                  ? Theme.of(context).colorScheme.background
                  : Colors.white,
              boxShadow: [
                BoxShadow(
                  color: Colors.black26,
                  blurRadius: 10,
                  offset: Offset(0, 5),
                ),
              ],
              borderRadius: const BorderRadius.vertical(
                bottom: Radius.circular(30),
                top: Radius.circular(30),
              ),
            ),
            child: SafeArea(
              child: Padding(
                padding: EdgeInsets.symmetric(horizontal: 20.0, vertical: 10.0),
                child: _buildTopBar(),
              ),
            ),
          ),
        ),
      ),
    );
  }

  Widget _buildTopBar() {
    return Row(
      children: [
        IconButton(
          icon: Icon(Icons.menu, color: Colors.green[900]),
          onPressed: () {
            _scaffoldKey.currentState?.openDrawer(); // Open the drawer
          },
        ),
        // Container(
        //   width: 50,
        //   height: 50,
        //   decoration: BoxDecoration(
        //     image: DecorationImage(
        //       image: AssetImage('assets/image/bg_remove.png'),
        //       fit: BoxFit.cover,
        //     ),
        //     borderRadius: BorderRadius.zero,
        //   ),
        // ),
        // SizedBox(width: 5),
        CircleAvatar(
          backgroundColor: Colors.green[100],
          radius: 30,
          child: Icon(Icons.local_hospital, color: Colors.green[900], size: 20),
        ),
        Text(
          'Human Hospital',
          style: TextStyle(
            color: Colors.green[900],
            fontSize: 18,
            fontWeight: FontWeight.bold,
          ),
        ),
        Spacer(),
      ],
    );
  }

  Widget _drawer() {
    final themeData = Theme.of(context);
    final isDarkMode = themeData.brightness == Brightness.dark;
    return Drawer(
      backgroundColor: isDarkMode ? themeData.colorScheme.background : Colors.white,
      child: Column(
        children: [
          DrawerHeader(
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                CircleAvatar(
                  backgroundColor: Colors.green[100],
                  radius: 40,
                  child: Icon(Icons.local_hospital, color: Colors.green[900], size: 40),
                ),
                SizedBox(height: 10),
                Text(
                  'Hospital App',
                  style: TextStyle(
                    color: Colors.green[900],
                    fontSize: 18,
                    fontWeight: FontWeight.bold,
                  ),
                ),
              ],
            ),
          ),
          Expanded(
            child: ListView(
              padding: EdgeInsets.zero,
              children: [
                _buildDrawerItem(
                  icon: Icons.fire_truck,
                  text: 'Hospital List',
                  onTap: () {
                    Navigator.push(
                      context,
                      MaterialPageRoute(builder: (context) => HospitalsListPage()),
                    );
                  },
                ),
                // App Appearance with CustomSwitch
                ListTile(
                  leading: Icon(Icons.brightness_6, color: Colors.green[900]),
                  title: Text('App Appearance', style: TextStyle(color: isDarkMode ? Colors.white : Colors.black,)),
                  trailing: CustomSwitch(
                    isDarkMode: _themeMode == ThemeMode.dark,
                    onToggle: (bool value) {
                      String newTheme = value ? 'Dark Theme' : 'Light Theme';
                      _setTheme(newTheme); // Update the theme
                    },
                  ),
                ),
                Divider(),
                _buildDrawerItem(
                  icon: Icons.logout,
                  text: 'Logout',
                  onTap: () {
                    _showLogoutConfirmationDialog();
                  },
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }

  void _showLogoutConfirmationDialog() {
    showDialog(
      context: context,
      builder: (BuildContext context) {
        final themeData = Theme.of(context);
        final isDarkMode = themeData.brightness == Brightness.dark;
        return AlertDialog(
          backgroundColor: isDarkMode ? Theme.of(context).colorScheme.background : Colors.white,
          title: Text("Logout", style: TextStyle(fontWeight: FontWeight.bold)),
          content: Text("Are you sure you want to logout?", style: TextStyle(fontWeight: FontWeight.bold)),
          actions: [
            TextButton(
              onPressed: () {
                Navigator.of(context).pop(); // Close the dialog
              },
              child: Text("Cancel", style: TextStyle(color:isDarkMode ? Colors.white : Colors.black, fontWeight: FontWeight.bold)),
            ),
            TextButton(
              onPressed: () {
                // Perform logout action here
                Navigator.of(context).pop(); // Close the dialog
                // Navigate to login page or perform logout
                Navigator.pushAndRemoveUntil(
                  context,
                  MaterialPageRoute(builder: (context) => Loginpage()),
                      (route) => false, // Removes all previous routes
                );
              },
              child: Text("Logout", style: TextStyle(color: Colors.red[400], fontWeight: FontWeight.bold)),
            ),
          ],
        );
      },
    );
  }

  Widget _buildDrawerItem({required IconData icon, required String text, required VoidCallback onTap}) {
    return ListTile(
      leading: Icon(icon, color: Colors.green[900]),
      title: Text(
        text,
        style: TextStyle(fontSize: 16, fontWeight: FontWeight.w500),
      ),
      onTap: onTap,
    );
  }

  Widget _addhumanhospital()
  {
    return SingleChildScrollView(
    padding: EdgeInsets.all(16.0),
    child: Center(
      child: Form(
        key: _formKey,
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text('Enter Details for Adding Your Hospital',
                style: TextStyle(color: Colors.grey, fontSize: 16, fontWeight: FontWeight.bold)),
            SizedBox(height: 20),
            _buildTextField(_hospitalNameController, 'Hospital Name', 'Enter hospital name', Icons.local_hospital),
            _buildTextField(_addressController, 'Address', 'Enter address', Icons.location_on),
            _buildTextField(_emailController, 'Email', 'Enter email', Icons.email, isEmail: true),
            _buildTextField(_passwordController, 'Password', 'Enter password', Icons.lock, isPassword: true),
            _buildTextField(_numberController, 'Number', 'Enter number', Icons.phone, isNumber: true),
            _buildTextField(_latitudeController, 'Latitude', 'Extracted from Map Link', Icons.map, isDecimal: true, readOnly: true),
            _buildTextField(_longitudeController, 'Longitude', 'Extracted from Map Link', Icons.map, isDecimal: true, readOnly: true),
            _buildTextField(_mapLinkController, 'Map Link', 'Enter Google Maps link', Icons.link, isURL: true, isMapLink: true),
            SizedBox(height: 32.0),
            Center(
              child: ElevatedButton(
                onPressed: signup,
                style: ElevatedButton.styleFrom(
                  backgroundColor: Colors.green[900],
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(15),
                  ),
                ),
                child: const Text("ADD", style: TextStyle(fontSize: 16, color: Colors.white)),
              ),
            ),
          ],
        ),
      ),
    ),
    );
  }
  Widget _buildTextField(
      TextEditingController controller,
      String label,
      String hint,
      IconData icon, {
        bool isEmail = false,
        bool isPassword = false,
        bool isNumber = false,
        bool isDecimal = false,
        bool isURL = false,
        bool isMapLink = false,
        bool readOnly = false,
      }) {
    return Padding(
      padding: const EdgeInsets.only(bottom: 16.0),
      child: TextFormField(
        controller: controller,
        obscureText: isPassword,
        readOnly: readOnly,
        keyboardType: isNumber
            ? TextInputType.number
            : isDecimal
            ? TextInputType.numberWithOptions(decimal: true)
            : isEmail
            ? TextInputType.emailAddress
            : isURL || isMapLink
            ? TextInputType.url
            : TextInputType.text,
        decoration: InputDecoration(
          labelText: label,
          hintText: hint,
          prefixIcon: Icon(icon, color: Colors.green[900]),
          border: OutlineInputBorder(borderRadius: BorderRadius.circular(15)),
        ),
        validator: (value) {
          if (value == null || value.isEmpty) {
            return 'Please enter $label';
          }
          if (isEmail && !RegExp(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$").hasMatch(value)) {
            return 'Enter a valid email';
          }
          if (isPassword && value.length < 6) {
            return 'Password must be at least 6 characters';
          }
          if (isNumber && !RegExp(r'^\d{10}$').hasMatch(value)) {
            return 'Enter a valid 10-digit number';
          }
          if (isDecimal && !RegExp(r'^-?\d+(\.\d+)?$').hasMatch(value)) {
            return 'Enter a valid number';
          }
          if (isURL && !Uri.parse(value).isAbsolute) {
            return 'Enter a valid URL';
          }
          return null;
        },
        onChanged: (value) {
          if (isMapLink) {
            _extractLatLong(); // Automatically extract lat & long when the Map Link field changes
          }
        },
      ),
    );
  }

}

class CustomSwitch extends StatefulWidget {
  final bool isDarkMode; // Current theme mode
  final ValueChanged<bool> onToggle; // Callback for toggle changes

  const CustomSwitch({Key? key, required this.isDarkMode, required this.onToggle}) : super(key: key);

  @override
  _CustomSwitchState createState() => _CustomSwitchState();
}

class _CustomSwitchState extends State<CustomSwitch> {
  late bool _isDarkMode;

  @override
  void initState() {
    super.initState();
    _isDarkMode = widget.isDarkMode;
  }

  @override
  void didUpdateWidget(CustomSwitch oldWidget) {
    super.didUpdateWidget(oldWidget);
    if (oldWidget.isDarkMode != widget.isDarkMode) {
      setState(() {
        _isDarkMode = widget.isDarkMode;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: () {
        setState(() {
          _isDarkMode = !_isDarkMode;
        });
        widget.onToggle(_isDarkMode);
      },
      child: Container(
        width: 100, // Reduced width
        height: 50, // Reduced height
        decoration: BoxDecoration(
          color: _isDarkMode ? Colors.blueGrey : Colors.yellow[200],
          borderRadius: BorderRadius.circular(25), // Reduced border radius
        ),
        child: Stack(
          children: [
            // Text for Light and Dark
            Align(
              alignment: Alignment.centerLeft,
              child: Padding(
                padding: const EdgeInsets.only(left: 8), // Adjusted padding
                child: Text(
                  'Light',
                  style: TextStyle(
                    color: _isDarkMode ? Colors.grey : Colors.black,
                    fontWeight: FontWeight.bold,
                    fontSize: 12, // Smaller font size
                  ),
                ),
              ),
            ),
            Align(
              alignment: Alignment.centerRight,
              child: Padding(
                padding: const EdgeInsets.only(right: 8), // Adjusted padding
                child: Text(
                  'Dark',
                  style: TextStyle(
                    color: _isDarkMode ? Colors.white : Colors.grey,
                    fontWeight: FontWeight.bold,
                    fontSize: 12, // Smaller font size
                  ),
                ),
              ),
            ),
            // Toggle Thumb
            AnimatedAlign(
              duration: Duration(milliseconds: 300),
              curve: Curves.easeInOut,
              alignment: _isDarkMode ? Alignment.centerRight : Alignment.centerLeft,
              child: Container(
                width: 40, // Reduced thumb size
                height: 40, // Reduced thumb size
                decoration: BoxDecoration(
                  color: _isDarkMode ? Colors.blue : Colors.yellow,
                  shape: BoxShape.circle,
                ),
                child: Icon(
                  _isDarkMode ? Icons.dark_mode : Icons.light_mode,
                  color: Colors.white,
                  size: 20, // Smaller icon size
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}