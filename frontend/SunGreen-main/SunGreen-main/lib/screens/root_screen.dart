
//screens/root_screen.dart

import 'package:curved_navigation_bar/curved_navigation_bar.dart';
import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:SunGreen/screens/add_plant_screen.dart';
import 'package:SunGreen/screens/home_screen.dart';
import 'package:SunGreen/screens/profile_settings_screen.dart';
import 'package:SunGreen/widgets/custom_app_bar.dart';

class RootScreen extends StatefulWidget {
  @override
  State<RootScreen> createState() => _RootScreenState();
}

class _RootScreenState extends State<RootScreen> {
  int _selectedIndex = 0;

  final List<Widget> _pages = [
    HomeScreen(),
    Center(child: Text('Search Page')),
    ProfileSettingsScreen()
  ];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: CustomAppBar(title: ''),
      body: Stack(
        children: [
          _pages[_selectedIndex],


        ],
      ),
      bottomNavigationBar: CurvedNavigationBar(
        height: 55,
        backgroundColor: Colors.transparent, // Прозрачный фон
        color: Color(0xFFF4D79F), // Цвет панели
        items: <Widget>[
          Icon(Icons.home_outlined, size: 30,
            color: _selectedIndex == 0 ? Colors.white : Colors.black,
          ),

          Visibility(
            visible: false, // Скрываем
            maintainSize: true, // Оставляем место
            maintainAnimation: true,
            maintainState: true,
            child: Icon(Icons.circle, size: 30),
          ),
          Icon(Icons.person_outline, size: 30,
            color: _selectedIndex == 2 ? Colors.white : Colors.black,
          ),
        ],
        onTap: (index) {
          if(index!=1){
            setState(() {
              _selectedIndex = index;
            });
          }
print(index);
        },
      ),
    );
  }
}

