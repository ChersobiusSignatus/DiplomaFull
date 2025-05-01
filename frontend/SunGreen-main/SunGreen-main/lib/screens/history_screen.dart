
//screens/history_screen.dart

import 'package:flutter/material.dart';
import 'package:intl/intl.dart';
import 'package:SunGreen/endpoints.dart';

import '../widgets/custom_app_bar.dart';

class HistoryScreen extends StatefulWidget {
  final String plantId;
  const HistoryScreen({Key? key, required this.plantId}) : super(key: key);

  @override
  State<HistoryScreen> createState() => _HistoryPageState();
}

class _HistoryPageState extends State<HistoryScreen> {
  DateTime? selectedDate;
  Map<String, dynamic>? historyData;
  bool isLoading = false;

  Future<void> _pickDate() async {
    final picked = await showDatePicker(
      context: context,
      initialDate: selectedDate ?? DateTime.now(),
      firstDate: DateTime(2020),
      lastDate: DateTime(2100),
    );

    if (picked != null) {
      setState(() {
        selectedDate = picked;
        isLoading = true;
        historyData = null;
      });

      final formattedDate = DateFormat('yyyy-MM-dd').format(picked);

      try {
        final data = await PlantApiService.fetchPlantHistory(
          plantId: widget.plantId,
          selectedDate: formattedDate,
        );

        setState(() {
          historyData = data;
          isLoading = false;
        });
      } catch (e) {
        setState(() {
          isLoading = false;
        });
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('Ошибка загрузки данных: $e')),
        );
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    final formattedDate = selectedDate != null
        ? DateFormat('yyyy-MM-dd').format(selectedDate!)
        : 'Выбрать дату';

    return Scaffold(
      backgroundColor: const Color(0xFFFDF0D0),
      appBar: CustomAppBar(
        title: 'История растения',
        actions: [
          IconButton(
            icon: const Icon(Icons.arrow_back, color: Colors.black),
            onPressed: () {
              Navigator.pop(context);
            },
          ),
        ],
      ),
      body: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Center(
              child: Text('История', style: TextStyle(fontSize: 30)),
            ),
            const SizedBox(height: 16),
            const Text('Выбрать дату:'),
            const SizedBox(height: 8),
            GestureDetector(
              onTap: _pickDate,
              child: Container(
                width: double.infinity,
                padding: const EdgeInsets.symmetric(
                  vertical: 12,
                  horizontal: 16,
                ),
                decoration: BoxDecoration(
                  color: const Color(0xFFFBE1B6),
                  borderRadius: BorderRadius.circular(12),
                  boxShadow: const [
                    BoxShadow(
                      color: Colors.black26,
                      blurRadius: 4,
                      offset: Offset(2, 2),
                    ),
                  ],
                ),
                child: Text(
                  formattedDate,
                  style: const TextStyle(fontSize: 16),
                ),
              ),
            ),
            const SizedBox(height: 16),
            const Text('Результат:'),
            const SizedBox(height: 8),
            isLoading
                ? const Center(child: CircularProgressIndicator())
                : historyData != null
                ? Container(
              width: double.infinity,
              padding: const EdgeInsets.all(16),
              decoration: BoxDecoration(
                color: const Color(0xFFD7D9A6),
                borderRadius: BorderRadius.circular(16),
              ),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text('Дата: ${historyData!['date'] ?? '-'}'),
                  const SizedBox(height: 8),
                  Text('Температура воздуха: ${historyData!['air_temperature'] ?? '-'}'),
                  Text('Влажность воздуха: ${historyData!['air_humidity'] ?? '-'}'),
                  Text('Влажность почвы: ${historyData!['soil_humidity'] ?? '-'}'),
                  Text('Свет: ${historyData!['light'] ?? '-'}'),
                  Text('Газ: ${historyData!['gas'] ?? '-'}'),
                  const SizedBox(height: 12),
                  Text('Рекомендация: ${historyData!['recommendation'] ?? '-'}'),
                ],
              ),
            )
                : const Text('Нет данных для выбранной даты.'),
          ],
        ),
      ),
    );
  }
}

