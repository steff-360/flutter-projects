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
