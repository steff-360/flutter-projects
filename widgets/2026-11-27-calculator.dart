import 'package:flutter/material.dart';

class CalculatorWidget extends StatefulWidget {
  const CalculatorWidget({super.key});
  @override State<CalculatorWidget> createState() => _CalculatorWidgetState();
}

class _CalculatorWidgetState extends State<CalculatorWidget> {
  String _display = '0';
  double _prev = 0, _current = 0;
  String _op = '';
  bool _reset = false;

  void _input(String val) => setState(() {
    if (_reset) { _display = val; _reset = false; return; }
    _display = _display == '0' ? val : _display + val;
    _current = double.tryParse(_display) ?? 0;
  });

  void _operator(String op) => setState(() {
    _prev = _current; _op = op; _reset = true;
  });

  void _equals() => setState(() {
    final result = switch (_op) {
      '+' => _prev + _current,
      '-' => _prev - _current,
      'x' => _prev * _current,
      '/' => _current != 0 ? _prev / _current : double.nan,
      _   => _current,
    };
    _display = result % 1 == 0 ? result.toInt().toString() : result.toStringAsFixed(4);
    _current = result; _op = ''; _reset = true;
  });

  Widget _btn(String label, {Color? color, VoidCallback? onTap}) => Expanded(
    child: Padding(
      padding: const EdgeInsets.all(4),
      child: ElevatedButton(
        style: ElevatedButton.styleFrom(backgroundColor: color ?? Colors.grey[800], foregroundColor: Colors.white, padding: const EdgeInsets.all(20)),
        onPressed: onTap,
        child: Text(label, style: const TextStyle(fontSize: 20)),
      ),
    ),
  );

  @override
  Widget build(BuildContext context) => Scaffold(
    backgroundColor: Colors.black,
    body: SafeArea(child: Column(children: [
      Expanded(child: Container(alignment: Alignment.bottomRight, padding: const EdgeInsets.all(24),
        child: Text(_display, style: const TextStyle(color: Colors.white, fontSize: 48)))),
      for (final row in [
        [('C', Colors.red[700]!, () => setState(() { _display='0'; _prev=_current=0; _op=''; })),
         ('+/-', null, null), ('%', null, null), ('/', Colors.orange, () => _operator('/'))],
        [('7', null, () => _input('7')), ('8', null, () => _input('8')), ('9', null, () => _input('9')), ('x', Colors.orange, () => _operator('x'))],
        [('4', null, () => _input('4')), ('5', null, () => _input('5')), ('6', null, () => _input('6')), ('-', Colors.orange, () => _operator('-'))],
        [('1', null, () => _input('1')), ('2', null, () => _input('2')), ('3', null, () => _input('3')), ('+', Colors.orange, () => _operator('+'))],
        [('0', null, () => _input('0')), ('.', null, () => _input('.')), ('=', Colors.orange, _equals)],
      ])
        Row(children: row.map((r) => _btn(r.$1, color: r.$2 as Color?, onTap: r.$3 as VoidCallback?)).toList()),
    ])),
  );
}
