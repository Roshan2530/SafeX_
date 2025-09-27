import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import '../api service/api_common.dart';
import 'firestationhomepage.dart';

class FireStationHistory extends StatefulWidget {
  final String email;

  const FireStationHistory({Key? key, required this.email}) : super(key: key);

  @override
  _FireStationHistoryState createState() => _FireStationHistoryState();
}

class _FireStationHistoryState extends State<FireStationHistory> {

  bool isLoading = true;
  List<Map<String, dynamic>> fireStationRecords = [];
  String errorMessage = '';

  @override
  void initState() {
    super.initState();
    fetchFireStationHistory();
  }

  Future<void> fetchFireStationHistory() async {
    try {
      final data = await ApiService().fetchFireStationHistory(widget.email);
      if (data != null && data is List) {
        setState(() {
          fireStationRecords = List<Map<String, dynamic>>.from(data);
        });
      } else {
        setState(() {
          errorMessage = 'No records found.';
        });
      }
    } catch (e) {
      setState(() {
        errorMessage = 'Error fetching data: $e';
      });
    } finally {
      setState(() {
        isLoading = false;
      });
    }
  }



  void _deleteRecord(int index) {
    final isDarkMode = Theme.of(context).brightness == Brightness.dark;
    showDialog(
      context: context,
      builder: (_) =>
          AlertDialog(
            backgroundColor: isDarkMode ? Colors.black : Colors.white,
            title: const Text('Delete Record'),
            content: const Text('Are you sure you want to delete this record?'),
            actions: [
              TextButton(
                onPressed: () => Navigator.pop(context),
                child: Text('Cancel',style: TextStyle(color: isDarkMode ? Colors.white : Colors.black,),),
              ),
              ElevatedButton(
                onPressed: () {
                  setState(() {
                    fireStationRecords.removeAt(index);
                  });
                  Navigator.pop(context);
                },
                style: ElevatedButton.styleFrom(backgroundColor:Colors.red[900]),
                child: const Text('Delete',style: TextStyle(color:Colors.white),),
              ),
            ],
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
                  icon:  Icon(Icons.arrow_back, color: Colors.red[900]),
                  onPressed: () => Navigator.pop(context),
                ),
                CircleAvatar(
                  backgroundColor: isDarkMode ? Theme.of(context).colorScheme.background : Colors.white,
                  radius: 24,
                  child: Icon(Icons.local_fire_department, color: Colors.red[900], size: 22),
                ),
                Text(
                  'Fire Station History',
                  style: TextStyle(
                    color: Colors.red[900],
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



  Widget _buildRecordList() {
    final themeData = Theme.of(context);
    final isDarkMode = themeData.brightness == Brightness.dark;

    // Filter out completely empty records
    final validRecords = fireStationRecords.where((record) => record.values.any((value) => value != null && value.toString().isNotEmpty)).toList();

    if (validRecords.isEmpty) {
      return Center(
        child: Text(
          'No records found.',
          style: GoogleFonts.poppins(
            color: isDarkMode ? Colors.white : Colors.black,
            fontSize: 18,
            fontWeight: FontWeight.w600,
          ),
        ),
      );
    }

    return ListView.builder(
      padding: const EdgeInsets.all(16),
      itemCount: validRecords.length,
      itemBuilder: (context, index) {
        final record = validRecords[index];

        return Card(
          elevation: 8,
          margin: const EdgeInsets.only(bottom: 24),
          color: isDarkMode ? themeData.colorScheme.background : Colors.grey[100],
          shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(20)),
          shadowColor: Colors.white.withOpacity(0.3),
          child: Padding(
            padding: const EdgeInsets.all(20),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.stretch,
              children: [
                Text(
                  "Record ${index + 1}",
                  style: GoogleFonts.robotoMono(
                    fontSize: 20,
                    fontWeight: FontWeight.bold,
                    color: Colors.red[900],
                  ),
                ),
                const Divider(thickness: 1.5, height: 30),
                ...record.entries.map((entry) {
                  final textColor = isDarkMode ? Colors.white : Colors.black87;
                  final fillColor = isDarkMode ? Colors.grey[850] : Colors.grey[100];
                  final borderColor = isDarkMode ? Colors.white54 : Colors.black26;

                  return Padding(
                    padding: const EdgeInsets.symmetric(vertical: 8),
                    child: TextField(
                      readOnly: true,
                      controller: TextEditingController(text: entry.value?.toString() ?? ''),
                      decoration: InputDecoration(
                        labelText: entry.key,
                        labelStyle: GoogleFonts.poppins(
                          fontWeight: FontWeight.w600,
                          fontSize: 14,
                          color: textColor,
                        ),
                        filled: true,
                        fillColor: fillColor,
                        border: OutlineInputBorder(
                          borderRadius: BorderRadius.circular(12),
                          borderSide: BorderSide(color: borderColor),
                        ),
                        enabledBorder: OutlineInputBorder(
                          borderRadius: BorderRadius.circular(12),
                          borderSide: BorderSide(color: borderColor),
                        ),
                        contentPadding: const EdgeInsets.symmetric(horizontal: 14, vertical: 12),
                      ),
                      style: GoogleFonts.poppins(
                        fontSize: 14,
                        color: textColor,
                      ),
                    ),
                  );
                }),
                const SizedBox(height: 16),

              ],
            ),
          ),
        );
      },
    );
  }
  @override
  Widget build(BuildContext context) {
    final themeData = Theme.of(context);
    final isDarkMode = themeData.brightness == Brightness.dark;
    return Scaffold(
      backgroundColor:
      isDarkMode ? themeData.colorScheme.background : Colors.grey[100],
      appBar: _buildAppBar(),
      body: isLoading
          ? const Center(child: CircularProgressIndicator())
          : errorMessage.isNotEmpty
          ? Center(
        child: Text(
          errorMessage,
          style: GoogleFonts.poppins(
            color: Colors.red,
            fontSize: 18,
            fontWeight: FontWeight.w600,
          ),
        ),
      )
          : _buildRecordList(),
    );
  }
}
