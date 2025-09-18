import 'package:flutter/material.dart';
import 'mode_selection_page.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Hand Mouse App',
      theme: ThemeData.dark(),
      debugShowCheckedModeBanner: false,
      home: const ModeSelectionPage(),
    );
  }
}
