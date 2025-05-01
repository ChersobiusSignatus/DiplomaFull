
//widgets/custom_app_bar.dart

import 'package:flutter/material.dart';

class CustomAppBar extends StatelessWidget implements PreferredSizeWidget {
  final String title;
  final List<Widget>? actions;

  const CustomAppBar({
    Key? key,
    required this.title,
    this.actions,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return AppBar(
      backgroundColor: Color(0xFFF4D79F),
      elevation: 4,
      actions: [
        IconButton(
          icon: Icon(Icons.notifications_none_outlined),
          onPressed: () {
            print('Settings icon pressed');
          },
        ),
      ],
    );
  }


  @override
  Size get preferredSize => const Size.fromHeight(kToolbarHeight);
}

