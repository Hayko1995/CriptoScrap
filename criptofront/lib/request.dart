import 'dart:convert';

import 'package:http/http.dart' as http;

class MyAPI {
  final client = http.Client();
  final headers = {'Content-Type': 'application/text; charset=utf-8'};

  Future request() async {
    //todo add problem response failure situation
    const subUrl = 'coins/';
    final Uri uri = Uri.parse('http://backend:8000/' + subUrl);
    // final Uri uri = Uri.parse('http://localhost:8000/' + subUrl);
    try {
      final http.Response response = await client.post(uri, headers: headers);
      return jsonDecode(response.body);
    } catch (e) {
      return Null;
    }
  }
}
