import 'package:flutter/material.dart';

class AppSnackbar {
  static void show(BuildContext context, String message, {SnackBarAction? action, Duration duration = const Duration(seconds: 3)}) {
    ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text(message), action: action, duration: duration));
  }

  static void success(BuildContext context, String message) => show(context, message,
    action: SnackBarAction(label: 'OK', onPressed: () => ScaffoldMessenger.of(context).hideCurrentSnackBar()));

  static void error(BuildContext context, String message) {
    ScaffoldMessenger.of(context).showSnackBar(SnackBar(
      content: Row(children: [const Icon(Icons.error_outline, color: Colors.white), const SizedBox(width: 8), Expanded(child: Text(message))]),
      backgroundColor: Colors.red[700],
      duration: const Duration(seconds: 4),
    ));
  }

  static void info(BuildContext context, String message) {
    ScaffoldMessenger.of(context).showSnackBar(SnackBar(
      content: Row(children: [const Icon(Icons.info_outline, color: Colors.white), const SizedBox(width: 8), Text(message)]),
      backgroundColor: Colors.blue[700],
    ));
  }
}
