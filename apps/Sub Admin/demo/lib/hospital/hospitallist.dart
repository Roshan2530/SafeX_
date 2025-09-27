import 'package:flutter/material.dart';
import '../api service/api_common.dart';
import 'hospitaldetails.dart';
import 'hospitalhomepage.dart';

class HospitalsListPage extends StatefulWidget {
  @override
  _HospitalsListPageState createState() => _HospitalsListPageState();
}

class _HospitalsListPageState extends State<HospitalsListPage> {
  late Future<List<dynamic>> _hospitalsFuture;
  late ApiService apiService;

  @override
  void initState() {
    super.initState();
    apiService = ApiService();
    _hospitalsFuture = apiService.fetchUsers_hospital();
  }

  @override
  Widget build(BuildContext context) {
    final themeData = Theme.of(context);
    final isDarkMode = themeData.brightness == Brightness.dark;

    return Scaffold(
      backgroundColor: isDarkMode ? themeData.colorScheme.background : Colors.grey[100],
      appBar: _buildAppBar(),
      body: FutureBuilder<List<dynamic>>(
        future: _hospitalsFuture,
        builder: (context, snapshot) {
          if (snapshot.connectionState == ConnectionState.waiting) {
            return Center(child: CircularProgressIndicator());
          } else if (snapshot.hasError) {
            return Center(child: Text("Error: ${snapshot.error}"));
          } else if (!snapshot.hasData || snapshot.data!.isEmpty) {
            return Center(child: Text("No hospitals found."));
          } else {
            return _hospitalList(snapshot.data!);
          }
        },
      ),
      floatingActionButton: FloatingActionButton.extended(
        onPressed: () {
          Navigator.push(
            context,
            MaterialPageRoute(builder: (context) => Homepage()),
          );
        },
        backgroundColor: Colors.green[900],
        icon: Icon(Icons.add, color: Colors.white),
        label: Text(
          "Add Hospital",
          style: TextStyle(color: Colors.white),
        ),
      ),
    );
  }
  PreferredSizeWidget _buildAppBar() {
    final isDarkMode = Theme.of(context).brightness == Brightness.dark;
    return PreferredSize(
      preferredSize: const Size.fromHeight(100),
      child: SafeArea(
        child: Padding(
          padding: const EdgeInsets.all(10),
          child: Container(
            height: 55,
            decoration: BoxDecoration(
              color: isDarkMode ? Theme.of(context).colorScheme.background : Colors.white,
              boxShadow: [
                BoxShadow(
                  color: Colors.black26,
                  blurRadius: 10,
                  offset: const Offset(0, 5),
                ),
              ],
              borderRadius: const BorderRadius.vertical(
                bottom: Radius.circular(30),
                top: Radius.circular(30),
              ),
            ),
            child: Row(
              children: [
                IconButton(
                  icon:  Icon(Icons.arrow_back, color: Colors.green[900]),
                  onPressed: () => Navigator.pop(context),
                ),
                CircleAvatar(
                  backgroundColor: isDarkMode ? Theme.of(context).colorScheme.background : Colors.white,
                  radius: 24,
                  child: Icon(Icons.local_hospital, color: Colors.green[900], size: 22),
                ),
                Text(
                  'Hospital List',
                  style: TextStyle(
                    color: Colors.green[900],
                    fontSize: 18,
                    fontWeight: FontWeight.bold,
                  ),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }


  Widget _hospitalList(List<dynamic> hospitals) {
    final isDarkMode = Theme.of(context).brightness == Brightness.dark;

    return ListView.builder(
      itemCount: hospitals.length,
      itemBuilder: (context, index) {
        var hospital = hospitals[index];
        String name = hospital['hospital_name'] ?? 'Unknown Hospital';
        String address = hospital['hospital_address'] ?? 'No Address';
        String phone = hospital['hospital_number'] ?? 'No Phone';
        String email = hospital['hospital_email'] ?? 'No Email';

        return Card(
          margin: EdgeInsets.symmetric(vertical: 10, horizontal: 16),
          elevation: 5,
          color: isDarkMode ? Colors.grey[850] : Colors.white,
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(15),
          ),
          child: Padding(
            padding: const EdgeInsets.all(16),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                ListTile(
                  contentPadding: EdgeInsets.zero,
                  title: Text(
                    name,
                    style: TextStyle(
                      fontSize: 20,
                      fontWeight: FontWeight.bold,
                      color: isDarkMode ? Colors.white : Colors.black,
                    ),
                  ),
                  subtitle: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      SizedBox(height: 4),
                      Text(address, style: TextStyle(color: Colors.grey[600])),
                      SizedBox(height: 4),
                      Text('Phone: $phone', style: TextStyle(color: Colors.grey[600])),
                      Text('Email: $email', style: TextStyle(color: Colors.grey[600])),
                    ],
                  ),
                  trailing: IconButton(
                    icon: Icon(Icons.arrow_forward_ios, color: Colors.grey[500], size: 20),
                    onPressed: () {
                      Navigator.push(
                        context,
                        MaterialPageRoute(
                          builder: (context) => HospitalHistory(email: email),
                        ),
                      );
                    },
                  ),
                ),

              ],
            ),
          ),
        );
      },
    );
  }
}
