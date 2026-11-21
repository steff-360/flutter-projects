import 'package:flutter/material.dart';

class RatingStars extends StatefulWidget {
  final int maxStars;
  final double initialRating;
  final ValueChanged<double>? onRatingChanged;
  const RatingStars({super.key, this.maxStars = 5, this.initialRating = 0, this.onRatingChanged});
  @override State<RatingStars> createState() => _RatingStarsState();
}

class _RatingStarsState extends State<RatingStars> {
  late double _rating;

  @override void initState() { super.initState(); _rating = widget.initialRating; }

  @override
  Widget build(BuildContext context) => Row(
    mainAxisSize: MainAxisSize.min,
    children: List.generate(widget.maxStars, (i) {
      final full = i < _rating.floor();
      final half = !full && i < _rating;
      return GestureDetector(
        onTap: () { setState(() => _rating = i + 1.0); widget.onRatingChanged?.call(_rating); },
        child: Icon(full ? Icons.star : half ? Icons.star_half : Icons.star_border, color: Colors.amber, size: 32),
      );
    }),
  );
}
