import datetime, os, sys

colombia_tz = datetime.timezone(datetime.timedelta(hours=-5))
now_col = datetime.datetime.now(colombia_tz)
today = now_col.date()
date_str = today.isoformat()
idx = (now_col.timetuple().tm_yday - 1) % 15

challenges = [
    ("widgets", "calculator.dart", """\
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
"""),
    ("widgets", "stopwatch.dart", """\
import 'dart:async';
import 'package:flutter/material.dart';

class StopwatchWidget extends StatefulWidget {
  const StopwatchWidget({super.key});
  @override State<StopwatchWidget> createState() => _StopwatchWidgetState();
}

class _StopwatchWidgetState extends State<StopwatchWidget> {
  Timer? _timer;
  int _ms = 0;
  final List<String> _laps = [];
  bool _running = false;

  void _toggle() {
    if (_running) { _timer?.cancel(); }
    else { _timer = Timer.periodic(const Duration(milliseconds: 10), (_) => setState(() => _ms += 10)); }
    setState(() => _running = !_running);
  }

  void _reset() { _timer?.cancel(); setState(() { _ms = 0; _running = false; _laps.clear(); }); }

  void _lap() => setState(() => _laps.insert(0, _format(_ms)));

  String _format(int ms) {
    final m  = (ms ~/ 60000).toString().padLeft(2, '0');
    final s  = ((ms ~/ 1000) % 60).toString().padLeft(2, '0');
    final cs = ((ms ~/ 10) % 100).toString().padLeft(2, '0');
    return '$m:$s.$cs';
  }

  @override
  Widget build(BuildContext context) => Scaffold(
    appBar: AppBar(title: const Text('Cronometro')),
    body: Column(children: [
      const SizedBox(height: 40),
      Text(_format(_ms), style: const TextStyle(fontSize: 56, fontWeight: FontWeight.w200)),
      const SizedBox(height: 24),
      Row(mainAxisAlignment: MainAxisAlignment.center, children: [
        FloatingActionButton(onPressed: _toggle, child: Icon(_running ? Icons.pause : Icons.play_arrow)),
        const SizedBox(width: 16),
        FloatingActionButton(onPressed: _lap, child: const Icon(Icons.flag)),
        const SizedBox(width: 16),
        FloatingActionButton(onPressed: _reset, child: const Icon(Icons.stop)),
      ]),
      const SizedBox(height: 20),
      Expanded(child: ListView.separated(
        itemCount: _laps.length,
        separatorBuilder: (_, __) => const Divider(),
        itemBuilder: (_, i) => ListTile(
          leading: Text('${_laps.length - i}', style: const TextStyle(fontWeight: FontWeight.bold)),
          title: Text(_laps[i], style: const TextStyle(fontFamily: 'monospace', fontSize: 20)),
        ),
      )),
    ]),
  );

  @override void dispose() { _timer?.cancel(); super.dispose(); }
}
"""),
    ("widgets", "bmi_calculator.dart", """\
import 'package:flutter/material.dart';

class BmiCalculator extends StatefulWidget {
  const BmiCalculator({super.key});
  @override State<BmiCalculator> createState() => _BmiCalculatorState();
}

class _BmiCalculatorState extends State<BmiCalculator> {
  double _height = 170, _weight = 70;
  double get _bmi => _weight / ((_height / 100) * (_height / 100));
  String get _category => _bmi < 18.5 ? 'Bajo peso' : _bmi < 25 ? 'Normal' : _bmi < 30 ? 'Sobrepeso' : 'Obesidad';
  Color get _color => _bmi < 18.5 ? Colors.blue : _bmi < 25 ? Colors.green : _bmi < 30 ? Colors.orange : Colors.red;

  @override
  Widget build(BuildContext context) => Scaffold(
    appBar: AppBar(title: const Text('Calculadora IMC')),
    body: Padding(
      padding: const EdgeInsets.all(24),
      child: Column(crossAxisAlignment: CrossAxisAlignment.stretch, children: [
        Text('Altura: ${_height.round()} cm', style: const TextStyle(fontSize: 18)),
        Slider(value: _height, min: 100, max: 250, divisions: 150, label: '${_height.round()} cm', onChanged: (v) => setState(() => _height = v)),
        const SizedBox(height: 20),
        Text('Peso: ${_weight.round()} kg', style: const TextStyle(fontSize: 18)),
        Slider(value: _weight, min: 30, max: 200, divisions: 170, label: '${_weight.round()} kg', onChanged: (v) => setState(() => _weight = v)),
        const SizedBox(height: 40),
        Card(color: _color.withOpacity(0.1), child: Padding(
          padding: const EdgeInsets.all(24),
          child: Column(children: [
            Text('IMC', style: TextStyle(fontSize: 16, color: Colors.grey[600])),
            Text(_bmi.toStringAsFixed(1), style: TextStyle(fontSize: 64, fontWeight: FontWeight.bold, color: _color)),
            Text(_category, style: TextStyle(fontSize: 22, color: _color)),
          ]),
        )),
      ]),
    ),
  );
}
"""),
    ("widgets", "temperature_converter.dart", """\
import 'package:flutter/material.dart';

class TemperatureConverter extends StatefulWidget {
  const TemperatureConverter({super.key});
  @override State<TemperatureConverter> createState() => _TemperatureConverterState();
}

class _TemperatureConverterState extends State<TemperatureConverter> {
  final _ctrl = TextEditingController();
  String _from = 'Celsius';
  double? _c, _f, _k;

  final _units = ['Celsius', 'Fahrenheit', 'Kelvin'];

  void _convert() {
    final val = double.tryParse(_ctrl.text);
    if (val == null) return;
    setState(() {
      switch (_from) {
        case 'Celsius':     _c = val; _f = val * 9/5 + 32; _k = val + 273.15;
        case 'Fahrenheit':  _f = val; _c = (val - 32) * 5/9; _k = _c! + 273.15;
        case 'Kelvin':      _k = val; _c = val - 273.15; _f = _c! * 9/5 + 32;
      }
    });
  }

  Widget _result(String unit, double? value) => ListTile(
    title: Text(unit),
    trailing: Text(value != null ? '${value.toStringAsFixed(2)} deg' : '-',
        style: const TextStyle(fontSize: 20, fontWeight: FontWeight.bold)),
  );

  @override
  Widget build(BuildContext context) => Scaffold(
    appBar: AppBar(title: const Text('Conversor de Temperatura')),
    body: Padding(padding: const EdgeInsets.all(16), child: Column(children: [
      DropdownButtonFormField(value: _from, items: _units.map((u) => DropdownMenuItem(value: u, child: Text(u))).toList(),
        decoration: const InputDecoration(labelText: 'Unidad de entrada', border: OutlineInputBorder()),
        onChanged: (v) => setState(() => _from = v!)),
      const SizedBox(height: 12),
      TextField(controller: _ctrl, keyboardType: TextInputType.number, decoration: const InputDecoration(labelText: 'Valor', border: OutlineInputBorder()),
        onSubmitted: (_) => _convert()),
      const SizedBox(height: 12),
      ElevatedButton(onPressed: _convert, child: const Text('Convertir')),
      const Divider(height: 32),
      _result('Celsius', _c), _result('Fahrenheit', _f), _result('Kelvin', _k),
    ])),
  );
}
"""),
    ("widgets", "custom_button.dart", """\
import 'package:flutter/material.dart';

class CustomButton extends StatelessWidget {
  final String label;
  final VoidCallback? onPressed;
  final Color? color;
  final IconData? icon;
  final bool loading;
  final bool outlined;

  const CustomButton({super.key, required this.label, this.onPressed, this.color, this.icon, this.loading = false, this.outlined = false});

  @override
  Widget build(BuildContext context) {
    final c = color ?? Theme.of(context).primaryColor;
    final child = loading
        ? SizedBox(width: 20, height: 20, child: CircularProgressIndicator(strokeWidth: 2, color: outlined ? c : Colors.white))
        : Row(mainAxisSize: MainAxisSize.min, children: [
            if (icon != null) ...[Icon(icon, size: 18), const SizedBox(width: 8)],
            Text(label),
          ]);

    return outlined
        ? OutlinedButton(
            style: OutlinedButton.styleFrom(foregroundColor: c, side: BorderSide(color: c), minimumSize: const Size(120, 48)),
            onPressed: loading ? null : onPressed, child: child)
        : ElevatedButton(
            style: ElevatedButton.styleFrom(backgroundColor: c, foregroundColor: Colors.white, minimumSize: const Size(120, 48)),
            onPressed: loading ? null : onPressed, child: child);
  }
}
"""),
    ("widgets", "animated_counter.dart", """\
import 'package:flutter/material.dart';

class AnimatedCounter extends StatefulWidget {
  const AnimatedCounter({super.key});
  @override State<AnimatedCounter> createState() => _AnimatedCounterState();
}

class _AnimatedCounterState extends State<AnimatedCounter> with SingleTickerProviderStateMixin {
  late AnimationController _ctrl;
  late Animation<double> _scale;
  int _count = 0;

  @override
  void initState() {
    super.initState();
    _ctrl = AnimationController(vsync: this, duration: const Duration(milliseconds: 150));
    _scale = TweenSequence([
      TweenSequenceItem(tween: Tween(begin: 1.0, end: 1.3), weight: 1),
      TweenSequenceItem(tween: Tween(begin: 1.3, end: 1.0), weight: 1),
    ]).animate(CurvedAnimation(parent: _ctrl, curve: Curves.easeInOut));
  }

  void _increment() { setState(() => _count++); _ctrl.forward(from: 0); }
  void _decrement() { setState(() => _count--); _ctrl.forward(from: 0); }
  void _reset()     { setState(() => _count = 0); }

  @override
  Widget build(BuildContext context) => Scaffold(
    appBar: AppBar(title: const Text('Contador Animado')),
    body: Center(child: Column(mainAxisAlignment: MainAxisAlignment.center, children: [
      ScaleTransition(scale: _scale,
        child: Text('$_count', style: TextStyle(fontSize: 80, fontWeight: FontWeight.bold,
            color: _count > 0 ? Colors.green : _count < 0 ? Colors.red : Colors.grey))),
      const SizedBox(height: 32),
      Row(mainAxisAlignment: MainAxisAlignment.center, children: [
        FloatingActionButton(onPressed: _decrement, heroTag: 'dec', child: const Icon(Icons.remove)),
        const SizedBox(width: 24),
        FloatingActionButton(onPressed: _reset, heroTag: 'rst', backgroundColor: Colors.grey, child: const Icon(Icons.refresh)),
        const SizedBox(width: 24),
        FloatingActionButton(onPressed: _increment, heroTag: 'inc', child: const Icon(Icons.add)),
      ]),
    ])),
  );

  @override void dispose() { _ctrl.dispose(); super.dispose(); }
}
"""),
    ("widgets", "search_bar.dart", """\
import 'package:flutter/material.dart';

class SearchBarWidget extends StatefulWidget {
  final List<String> items;
  const SearchBarWidget({super.key, required this.items});
  @override State<SearchBarWidget> createState() => _SearchBarWidgetState();
}

class _SearchBarWidgetState extends State<SearchBarWidget> {
  final _ctrl = TextEditingController();
  List<String> _results = [];

  @override
  void initState() { super.initState(); _results = widget.items; }

  void _search(String query) => setState(() {
    _results = query.isEmpty
        ? widget.items
        : widget.items.where((i) => i.toLowerCase().contains(query.toLowerCase())).toList();
  });

  @override
  Widget build(BuildContext context) => Scaffold(
    appBar: AppBar(title: const Text('Busqueda')),
    body: Column(children: [
      Padding(
        padding: const EdgeInsets.all(12),
        child: TextField(
          controller: _ctrl,
          decoration: InputDecoration(
            hintText: 'Buscar...',
            prefixIcon: const Icon(Icons.search),
            suffixIcon: _ctrl.text.isNotEmpty
                ? IconButton(icon: const Icon(Icons.clear), onPressed: () { _ctrl.clear(); _search(''); })
                : null,
            border: OutlineInputBorder(borderRadius: BorderRadius.circular(12)),
          ),
          onChanged: _search,
        ),
      ),
      Expanded(child: ListView.builder(
        itemCount: _results.length,
        itemBuilder: (_, i) => ListTile(leading: const Icon(Icons.label_outline), title: Text(_results[i])),
      )),
    ]),
  );
}
"""),
    ("widgets", "form_validator.dart", """\
import 'package:flutter/material.dart';

class FormValidatorWidget extends StatefulWidget {
  const FormValidatorWidget({super.key});
  @override State<FormValidatorWidget> createState() => _FormValidatorWidgetState();
}

class _FormValidatorWidgetState extends State<FormValidatorWidget> {
  final _formKey = GlobalKey<FormState>();
  final _name = TextEditingController();
  final _email = TextEditingController();
  final _pass = TextEditingController();
  bool _submitted = false;

  String? _validateName(String? v)  => (v?.trim().isEmpty ?? true) ? 'Nombre requerido' : null;
  String? _validateEmail(String? v) => v?.contains('@') == true ? null : 'Email invalido';
  String? _validatePass(String? v)  => (v?.length ?? 0) >= 8 ? null : 'Minimo 8 caracteres';

  void _submit() {
    if (_formKey.currentState!.validate()) {
      setState(() => _submitted = true);
      ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text('Registro exitoso')));
    }
  }

  @override
  Widget build(BuildContext context) => Scaffold(
    appBar: AppBar(title: const Text('Registro')),
    body: Padding(padding: const EdgeInsets.all(24), child: Form(key: _formKey, child: Column(children: [
      TextFormField(controller: _name, validator: _validateName, decoration: const InputDecoration(labelText: 'Nombre', prefixIcon: Icon(Icons.person))),
      const SizedBox(height: 16),
      TextFormField(controller: _email, validator: _validateEmail, keyboardType: TextInputType.emailAddress, decoration: const InputDecoration(labelText: 'Email', prefixIcon: Icon(Icons.email))),
      const SizedBox(height: 16),
      TextFormField(controller: _pass, validator: _validatePass, obscureText: true, decoration: const InputDecoration(labelText: 'Contrasena', prefixIcon: Icon(Icons.lock))),
      const SizedBox(height: 24),
      SizedBox(width: double.infinity, child: ElevatedButton(onPressed: _submit, child: const Text('Registrarse'))),
    ]))),
  );
}
"""),
    ("widgets", "profile_card.dart", """\
import 'package:flutter/material.dart';

class ProfileCard extends StatelessWidget {
  final String name, role, email;
  final String? avatarUrl;
  final List<String> skills;
  final VoidCallback? onContact;

  const ProfileCard({super.key, required this.name, required this.role, required this.email, this.avatarUrl, this.skills = const [], this.onContact});

  @override
  Widget build(BuildContext context) => Card(
    elevation: 4,
    shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
    child: Padding(padding: const EdgeInsets.all(20), child: Column(children: [
      CircleAvatar(radius: 40,
        backgroundImage: avatarUrl != null ? NetworkImage(avatarUrl!) : null,
        child: avatarUrl == null ? Text(name[0], style: const TextStyle(fontSize: 32)) : null),
      const SizedBox(height: 12),
      Text(name, style: const TextStyle(fontSize: 20, fontWeight: FontWeight.bold)),
      Text(role, style: TextStyle(color: Colors.grey[600])),
      Text(email, style: TextStyle(color: Colors.blue[700], fontSize: 12)),
      if (skills.isNotEmpty) ...[
        const SizedBox(height: 12),
        Wrap(spacing: 6, children: skills.map((s) => Chip(label: Text(s, style: const TextStyle(fontSize: 11)), padding: EdgeInsets.zero)).toList()),
      ],
      if (onContact != null) ...[
        const SizedBox(height: 12),
        OutlinedButton.icon(onPressed: onContact, icon: const Icon(Icons.mail_outline), label: const Text('Contactar')),
      ],
    ])),
  );
}
"""),
    ("widgets", "rating_stars.dart", """\
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
"""),
    ("widgets", "loading_spinner.dart", """\
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
"""),
    ("helpers", "snackbar_helper.dart", """\
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
"""),
    ("helpers", "dialog_helper.dart", """\
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
"""),
    ("widgets", "gradient_container.dart", """\
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
"""),
    ("widgets", "chip_group.dart", """\
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
"""),
]

folder, name, content = challenges[idx]
os.makedirs(folder, exist_ok=True)
base_target = os.path.join(folder, f"{date_str}-{name}")
target = base_target
v = 2
while os.path.exists(target):
    target = os.path.join(folder, f"{date_str}-v{v}-{name}")
    v += 1
with open(target, "w") as f:
    f.write(content)
print(f"Created: {target}")
