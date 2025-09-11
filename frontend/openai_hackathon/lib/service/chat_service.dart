import 'dart:convert';
import 'package:http/http.dart' as http;

class ChatService {
  final String baseUrl = "http://192.168.0.113:8000/v1"; // Change to your backend address

  Future<String> sendMessage(String message) async {
    final url = Uri.parse('$baseUrl/ask');

    final response = await http.post(
      url,
      headers: {"Content-Type": "application/json"},
      body: jsonEncode({
        "request": message,
        "longitude": "77.6107",
        "latitude": "12.9345",
        }),
    );

    if (response.statusCode == 200) {
      final data = jsonDecode(response.body);
      // adjust depending on AccidentReport model
      return data["details"] ?? "No response from server";
    } else {
      throw Exception("Failed to get response: ${response.body}");
    }
  }
}