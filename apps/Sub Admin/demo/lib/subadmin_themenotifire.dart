import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';

class ThemeNotifier extends ChangeNotifier {
  ThemeMode _themeMode = ThemeMode.light; // Default theme mode

  ThemeMode get themeMode => _themeMode; // Getter for the theme mode

  // Load the theme from SharedPreferences
  Future<void> loadTheme() async {
    SharedPreferences prefs = await SharedPreferences.getInstance();
    String? theme = prefs.getString('themeMode');
    if (theme != null) {
      _themeMode = theme == 'dark' ? ThemeMode.dark : ThemeMode.light;
    }
    notifyListeners(); // Notify listeners after loading theme
  }

  // Set the theme and save it to SharedPreferences
  void setTheme(ThemeMode mode) {
    _themeMode = mode;
    _saveThemeToPrefs(mode); // Save the theme preference
    notifyListeners(); // Notify listeners about the change
  }

  // Save the theme preference to SharedPreferences
  Future<void> _saveThemeToPrefs(ThemeMode mode) async {
    SharedPreferences prefs = await SharedPreferences.getInstance();
    prefs.setString('themeMode', mode == ThemeMode.dark ? 'dark' : 'light');
  }
}