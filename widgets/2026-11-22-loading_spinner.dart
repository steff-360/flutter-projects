import 'package:flutter/material.dart';

class LoadingSpinner extends StatelessWidget {
  final String? message;
  final Color? color;
  final double size;
  const LoadingSpinner({super.key, this.message, this.color, this.size = 40});

  @override
  Widget build(BuildContext context) => Center(child: Column(mainAxisSize: MainAxisSize.min, children: [
    SizedBox(width: size, height: size,
        child: CircularProgressIndicator(strokeWidth: 3, valueColor: AlwaysStoppedAnimation(color ?? Theme.of(context).primaryColor))),
    if (message != null) ...[const SizedBox(height: 16), Text(message!, style: TextStyle(color: Colors.grey[600]))],
  ]));
}

// Overlay de carga para toda la pantalla
class LoadingOverlay extends StatelessWidget {
  final Widget child;
  final bool isLoading;
  final String? message;
  const LoadingOverlay({super.key, required this.child, required this.isLoading, this.message});

  @override
  Widget build(BuildContext context) => Stack(children: [
    child,
    if (isLoading) Container(color: Colors.black38, child: LoadingSpinner(message: message)),
  ]);
}
