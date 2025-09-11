import 'package:flutter/material.dart';

class ChatBubble extends StatelessWidget {
  final String message;
  final bool isUser; // true = user message, false = bot/other

  const ChatBubble({
    super.key,
    required this.message,
    this.isUser = true,
  });

  @override
  Widget build(BuildContext context) {
    return Align(
      alignment: isUser ? Alignment.centerRight : Alignment.centerLeft,
      child: Container(
        margin: const EdgeInsets.symmetric(vertical: 4, horizontal: 12),
        padding: const EdgeInsets.all(12),
        decoration: BoxDecoration(
          color: isUser ? Colors.deepPurple[200] : Colors.grey[300],
          borderRadius: BorderRadius.circular(16),
        ),
        child: Text(
          message,
          style: const TextStyle(fontSize: 16, color:Colors.white),
        ),
      ),
    );
  }
}