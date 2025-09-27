import 'package:demo/splashscreen.dart';
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'subadmin_themenotifire.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized(); // Ensure binding is initialized
  final themeNotifier = ThemeNotifier();
  await themeNotifier.loadTheme(); // Load the theme preference

  runApp(
    ChangeNotifierProvider(
      create: (context) => themeNotifier,
      child: MyApp(),
    ),
  );
}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    final themeProvider = Provider.of<ThemeNotifier>(context);
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      themeMode: themeProvider.themeMode,
      theme: ThemeData.light(), // Define your light theme
      darkTheme: ThemeData.dark(), // Define your dark theme
      home: SplashScreen()
    );
  }
}