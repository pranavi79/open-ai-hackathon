import 'package:flutter/material.dart';
import 'package:openai_hackathon/components/chat_bubble.dart';
import 'package:openai_hackathon/components/text_field.dart';
import 'package:openai_hackathon/service/chat_service.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  // This widget is the root of your application.
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      title: 'Medi Agent',
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.deepPurple),
      ),
      home: const MyHomePage(title: 'Medi Agent'),
    );
  }
}

class MyHomePage extends StatefulWidget {
  const MyHomePage({super.key, required this.title});

  final String title;

  @override
  State<MyHomePage> createState() => _MyHomePageState();
}

class _MyHomePageState extends State<MyHomePage> {
  final TextEditingController _controller = TextEditingController();
  final List<Map<String, dynamic>> _messages = []; // { "text": "", "isUser": true }
  final ChatService _chatService = ChatService();

  void _handleSend() async {
    if (_controller.text.trim().isEmpty) return;

    final userMessage = _controller.text.trim();

    setState(() {
      _messages.add({"text": userMessage, "isUser": true});
    });
    _controller.clear();

    try {
      final botResponse = await _chatService.sendMessage(userMessage);
      setState(() {
        _messages.add({"text": botResponse, "isUser": false});
      });
    } catch (e) {
      setState(() {
        _messages.add({"text": "Error: $e", "isUser": false});
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        backgroundColor: Theme.of(context).colorScheme.inversePrimary,
        title: const Text('Medi Aid'),
      ),
      body: Column(
        children: [
          Expanded(
            child: ListView.builder(
              padding: EdgeInsets.all(6),
              itemCount: _messages.length,
              itemBuilder: (context, index) {
                final msg = _messages[index];
                return ChatBubble(
                  message: msg["text"],
                  isUser: msg["isUser"],
                );
              },
            ),
          ),
          CustomTextField(
            controller: _controller,
            onSend: _handleSend,
          ),
        ],
      ),
    );
  }
}