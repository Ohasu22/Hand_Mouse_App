import 'dart:convert';
import 'dart:typed_data';
import 'package:web_socket_channel/web_socket_channel.dart';

typedef FrameCallback =
    void Function(Uint8List? frame, Map<String, dynamic> meta);

class WSService {
  final String url;
  final FrameCallback onFrame;
  late WebSocketChannel channel;

  WSService(this.url, this.onFrame) {
    channel = WebSocketChannel.connect(Uri.parse(url));

    channel.stream.listen((message) {
      final data = jsonDecode(message);

      if (data['type'] == 'frame') {
        final bytes = base64Decode(data['jpeg_base64']);
        final meta = data['meta'] ?? {};
        onFrame(bytes, meta);
      }
    });
  }

  void send(Map<String, dynamic> msg) {
    channel.sink.add(jsonEncode(msg));
  }

  void dispose() {
    channel.sink.close();
  }
}
