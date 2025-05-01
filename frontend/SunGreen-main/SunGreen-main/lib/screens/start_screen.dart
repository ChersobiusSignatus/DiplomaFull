
//screens/start_screen.dart

import 'package:flutter/material.dart';
import 'root_screen.dart';

class StartScreen extends StatefulWidget {
  const StartScreen({super.key});

  @override
  _StartScreenState createState() => _StartScreenState();
}

class _StartScreenState extends State<StartScreen>
    with SingleTickerProviderStateMixin {
  late AnimationController _controller;
  late Animation<double> _animation;

  @override
  void initState() {
    super.initState();
    _controller = AnimationController(
      vsync: this,
      duration: Duration(milliseconds: 200),
    )..repeat(reverse: true);

    _animation = Tween<double>(begin: 0, end: 5).animate(
      CurvedAnimation(
        parent: _controller,
        curve: Curves.easeInOut,
      ),
    );
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    double screenHeight = MediaQuery.of(context).size.height;
    double screenWidth = MediaQuery.of(context).size.width;

    return Scaffold(
      body: Stack(
        children: [
          // Фон
          Container(
            width: double.infinity,
            height: double.infinity,
            decoration: BoxDecoration(
              image: DecorationImage(
                image: AssetImage('assets/animation.gif'),
                fit: BoxFit.cover,
              ),
            ),
          ),

          Positioned(
            top: screenHeight * 0.1,
            left: screenWidth * 0.1,
            right: screenWidth * 0.1,
            child: RichText(
              textAlign: TextAlign.center,
              text: TextSpan(
                style: TextStyle(
                  fontFamily: 'Cartoon',
                  fontSize: 50,
                  fontWeight: FontWeight.bold,
                  shadows: [
                    Shadow(
                      offset: Offset(3, 3),
                      blurRadius: 6.0,
                      color: Colors.black.withOpacity(0.9),
                    ),
                  ],
                ),
                children: [
                  TextSpan(text: 'S', style: TextStyle(color: Color(0xFFD16980))),
                  TextSpan(text: 'U', style: TextStyle(color: Color(0xFF9CACCE))),
                  TextSpan(text: 'N', style: TextStyle(color: Color(0xFF688C28))),
                  TextSpan(text: '\n', style: TextStyle(color: Colors.transparent)),
                  TextSpan(text: 'G', style: TextStyle(color: Color(0xFFF19903))),
                  TextSpan(text: 'R', style: TextStyle(color: Color(0xFF9CACCE))),
                  TextSpan(text: 'E', style: TextStyle(color: Color(0xFF688C28))),
                  TextSpan(text: 'E', style: TextStyle(color: Color(0xFF688C28))),
                  TextSpan(text: 'N', style: TextStyle(color: Color(0xFFF19903))),
                ],
              ),
            ),
          ),

          Align(
            alignment: Alignment.bottomCenter,
            child: Padding(
              padding: EdgeInsets.only(bottom: screenHeight * 0.15),
              child: AnimatedBuilder(
                animation: _animation,
                builder: (context, child) {
                  return Transform.translate(
                    offset: Offset(0, _animation.value),
                    child: child,
                  );
                },
                child: ElevatedButton(
                  onPressed: () {
                    Navigator.pushReplacement(
                      context,
                      MaterialPageRoute(builder: (context) => RootScreen()),
                    );
                  },
                  style: ElevatedButton.styleFrom(
                    backgroundColor: Color(0xFF688C28),
                    padding: EdgeInsets.only(top: 13, left: 20, right: 20, bottom: 8),
                    elevation: 15,
                    shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(17),
                      side: BorderSide(color: Color(0xFFF4D79F), width: 5),
                    ),
                  ),
                  child: Text(
                    'GET STARTED',
                    style: TextStyle(
                      fontFamily: 'Cartoon',
                      fontSize: 28,
                      color: Color(0xFFF4D79F),
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                ),
              ),
            ),
          ),
        ],
      ),
    );
  }
}

