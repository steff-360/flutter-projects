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
