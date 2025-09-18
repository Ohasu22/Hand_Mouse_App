import 'dart:typed_data';
import 'package:flutter/material.dart';
import 'ws_service.dart';

class LiveFeedPage extends StatefulWidget {
  final String mode;
  const LiveFeedPage({super.key, required this.mode});

  @override
  State<LiveFeedPage> createState() => _LiveFeedPageState();
}

class _LiveFeedPageState extends State<LiveFeedPage> {
  Uint8List? currentFrame;
  Map<String, dynamic> meta = {};
  late WSService ws;

  @override
  void initState() {
    super.initState();

    ws = WSService("ws://127.0.0.1:8000/ws", (frame, m) {
      setState(() {
        currentFrame = frame;
        meta = m;
      });
    });

    // Send selected mode to backend
    ws.send({
      "action": widget.mode == "mouse" ? "mouse_enable" : "gesture_enable",
    });
  }

  @override
  void dispose() {
    ws.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text("Live Feed (${widget.mode})")),
      body: Column(
        children: [
          Expanded(
            child: currentFrame != null
                ? Image.memory(currentFrame!, gaplessPlayback: true)
                : const Center(child: CircularProgressIndicator()),
          ),
          Container(
            padding: const EdgeInsets.all(16),
            color: Colors.black54,
            width: double.infinity,
            child: Text(
              "Meta: $meta",
              style: const TextStyle(color: Colors.white),
            ),
          ),
        ],
      ),
    );
  }
}
