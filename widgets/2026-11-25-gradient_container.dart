import 'package:flutter/material.dart';

class GradientContainer extends StatelessWidget {
  final Widget child;
  final List<Color> colors;
  final AlignmentGeometry begin, end;
  final double borderRadius;
  final EdgeInsetsGeometry? padding;

  const GradientContainer({super.key, required this.child, required this.colors,
    this.begin = Alignment.topLeft, this.end = Alignment.bottomRight,
    this.borderRadius = 12, this.padding});

  static const presets = {
    'ocean':   [Color(0xFF0a0f1d), Color(0xFF2563eb)],
    'sunset':  [Color(0xFFFF6B6B), Color(0xFFFFE66D)],
    'forest':  [Color(0xFF134E5E), Color(0xFF71B280)],
    'purple':  [Color(0xFF8360C3), Color(0xFF2EBF91)],
  };

  @override
  Widget build(BuildContext context) => Container(
    padding: padding,
    decoration: BoxDecoration(
      gradient: LinearGradient(colors: colors, begin: begin, end: end),
      borderRadius: BorderRadius.circular(borderRadius),
    ),
    child: child,
  );
}
