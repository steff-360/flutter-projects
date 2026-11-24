import 'package:flutter/material.dart';

class AppDialog {
  static Future<bool?> confirm(BuildContext context, {required String title, required String message, String confirmLabel = 'Confirmar', String cancelLabel = 'Cancelar'}) =>
    showDialog<bool>(context: context, builder: (_) => AlertDialog(
      title: Text(title),
      content: Text(message),
      actions: [
        TextButton(onPressed: () => Navigator.pop(context, false), child: Text(cancelLabel)),
        ElevatedButton(onPressed: () => Navigator.pop(context, true), child: Text(confirmLabel)),
      ],
    ));

  static Future<void> info(BuildContext context, {required String title, required String message}) =>
    showDialog(context: context, builder: (_) => AlertDialog(
      title: Text(title), content: Text(message),
      actions: [TextButton(onPressed: () => Navigator.pop(context), child: const Text('Cerrar'))],
    ));

  static Future<String?> input(BuildContext context, {required String title, String hint = ''}) {
    final ctrl = TextEditingController();
    return showDialog<String>(context: context, builder: (_) => AlertDialog(
      title: Text(title),
      content: TextField(controller: ctrl, decoration: InputDecoration(hintText: hint)),
      actions: [
        TextButton(onPressed: () => Navigator.pop(context), child: const Text('Cancelar')),
        ElevatedButton(onPressed: () => Navigator.pop(context, ctrl.text), child: const Text('OK')),
      ],
    ));
  }
}
