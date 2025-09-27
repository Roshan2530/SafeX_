import 'package:demo/login.dart';

import 'package:flutter/material.dart';
import 'package:video_player/video_player.dart';

class SplashScreen extends StatefulWidget {
  const SplashScreen({super.key});

  @override
  _SplashScreenState createState() => _SplashScreenState();
}

class _SplashScreenState extends State<SplashScreen> {
  late VideoPlayerController _videoController;

  @override
  void initState() {
    super.initState();
    _videoController = VideoPlayerController.asset('assets/video/splashvideo1.mp4')
      ..initialize().then((_) {
        setState(() {}); // Update the UI after video is initialized
        _videoController.play();
        _videoController.setLooping(false);
      });

    // Simulate getting an email or pass the email through some other method
   // This should come from your user data or previous screen

    // Navigate to the next screen after the video ends
    _videoController.addListener(() {
      if (_videoController.value.position == _videoController.value.duration) {
        Navigator.of(context).pushReplacement(
          MaterialPageRoute(builder: (context) =>Loginpage()),
        );
      }
    });
  }

  @override
  void dispose() {
    _videoController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.white,
      body: _videoController.value.isInitialized
          ? SizedBox.expand(
        child: FittedBox(
          fit: BoxFit.cover,
          child: SizedBox(
            width: _videoController.value.size.width,
            height: _videoController.value.size.height,
            child: VideoPlayer(_videoController),
          ),
        ),
      )
          : const Center(
        child: CircularProgressIndicator(), // Show loader while the video initializes
      ),
    );
  }
}