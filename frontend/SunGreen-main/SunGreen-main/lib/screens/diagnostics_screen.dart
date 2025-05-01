
//screens/diagnostics_screen.dart

import 'package:flutter/material.dart';
import '../endpoints.dart';

class DiagnosticsScreen extends StatefulWidget {
  final String plantId;

  const DiagnosticsScreen({super.key, required this.plantId});

  @override
  State<DiagnosticsScreen> createState() => _DiagnosticsScreenState();
}

class _DiagnosticsScreenState extends State<DiagnosticsScreen> {
  String recommendationText = 'Рекомендация';
  bool isLoading = false;

  Future<void> diagnoseByPhoto() async {
    setState(() => isLoading = true);
    try {
      final recommendation = await PlantApiService.diagnoseByPhoto(widget.plantId);
      setState(() => recommendationText = recommendation);
    } catch (e) {
      setState(() => recommendationText = 'Ошибка: $e');
    } finally {
      setState(() => isLoading = false);
    }
  }

  Future<void> diagnoseCombined() async {
    setState(() => isLoading = true);
    try {
      final recommendation = await PlantApiService.diagnoseCombined(widget.plantId);
      setState(() => recommendationText = recommendation);
    } catch (e) {
      setState(() => recommendationText = 'Ошибка: $e');
    } finally {
      setState(() => isLoading = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        backgroundColor: const Color(0xFFF4D79F),
        elevation: 0,
        title: const Text('', style: TextStyle(color: Colors.black)),
        iconTheme: const IconThemeData(color: Colors.black),
      ),
      backgroundColor: const Color(0xFFF3E3B4),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16),
        child: Column(
          children: [
            const SizedBox(height: 20),
            const Text(
              'Диагностика',
              style: TextStyle(fontSize: 30, color: Colors.black),
            ),
            const SizedBox(height: 20),
            ElevatedButton(
              onPressed: diagnoseByPhoto,
              style: ElevatedButton.styleFrom(
                padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 8),
                backgroundColor: const Color(0xFFF4D79F),
                shape: RoundedRectangleBorder(
                  borderRadius: BorderRadius.circular(10),
                ),
                elevation: 5,
              ),
              child: const Text(
                'По фото',
                style: TextStyle(color: Colors.white, fontSize: 14),
              ),
            ),
            const SizedBox(height: 10),
            ElevatedButton(
              onPressed: diagnoseCombined,
              style: ElevatedButton.styleFrom(
                padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 8),
                backgroundColor: const Color(0xFFF4D79F),
                shape: RoundedRectangleBorder(
                  borderRadius: BorderRadius.circular(10),
                ),
                elevation: 5,
              ),
              child: const Text(
                'Комбинированно',
                style: TextStyle(color: Colors.white, fontSize: 14),
              ),
            ),
            const SizedBox(height: 20),
            const Text('Выберите способ диагностики', style: TextStyle(fontSize: 16)),
            const SizedBox(height: 20),
            Container(
              decoration: BoxDecoration(
                color: const Color(0x7E7D887F),
                borderRadius: BorderRadius.circular(24),
              ),
              padding: const EdgeInsets.all(16),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  const Text('Рекомендации', style: TextStyle(fontWeight: FontWeight.bold)),
                  const Divider(
                    color: Colors.grey,
                    thickness: 1,
                    indent: 16,
                    endIndent: 16,
                  ),
                  isLoading
                      ? const Center(child: CircularProgressIndicator())
                      : Text(
                    recommendationText,
                    style: const TextStyle(fontSize: 16),
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }
}

