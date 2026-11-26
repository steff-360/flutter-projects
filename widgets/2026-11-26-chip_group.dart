import 'package:flutter/material.dart';

class ChipGroup extends StatefulWidget {
  final List<String> options;
  final bool multiSelect;
  final List<String>? initialSelected;
  final ValueChanged<List<String>>? onChanged;
  const ChipGroup({super.key, required this.options, this.multiSelect = false, this.initialSelected, this.onChanged});
  @override State<ChipGroup> createState() => _ChipGroupState();
}

class _ChipGroupState extends State<ChipGroup> {
  late Set<String> _selected;

  @override void initState() { super.initState(); _selected = Set.from(widget.initialSelected ?? []); }

  void _toggle(String option) {
    setState(() {
      if (!widget.multiSelect) _selected.clear();
      _selected.contains(option) ? _selected.remove(option) : _selected.add(option);
    });
    widget.onChanged?.call(_selected.toList());
  }

  @override
  Widget build(BuildContext context) => Wrap(
    spacing: 8, runSpacing: 4,
    children: widget.options.map((opt) {
      final selected = _selected.contains(opt);
      return FilterChip(
        label: Text(opt),
        selected: selected,
        onSelected: (_) => _toggle(opt),
        selectedColor: Theme.of(context).primaryColor.withOpacity(0.2),
        checkmarkColor: Theme.of(context).primaryColor,
      );
    }).toList(),
  );
}
