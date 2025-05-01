
//screens/plant_screen.dart

import 'dart:async';
import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:flutter_blue_plus/flutter_blue_plus.dart';
import 'package:permission_handler/permission_handler.dart';
import '../endpoints.dart';
import '../widgets/custom_app_bar.dart';
import 'change_photo_screen.dart';
import 'diagnostics_screen.dart';
import 'history_screen.dart';
import 'models/plant_details.dart';

class PlantScreen extends StatefulWidget {
  final String plantId;
  final String photoUrl;

  const PlantScreen({super.key, required this.plantId, required this.photoUrl});

  @override
  State<PlantScreen> createState() => _PlantScreenState();
}

class _PlantScreenState extends State<PlantScreen> {
  PlantDetails? details;
  bool isLoading = true;
  bool isCollectingData = false;
  bool bluetoothConnected = false;
  StreamSubscription? scanSubscription;

  @override
  void initState() {
    super.initState();
    loadPlantDetails();
  }

  @override
  void dispose() {
    scanSubscription?.cancel();
    super.dispose();
  }

  Future<void> loadPlantDetails() async {
    try {
      final data = await PlantApiService.plantDetails(widget.plantId);
      setState(() {
        details = data;
        isLoading = false;
      });
    } catch (e) {
      setState(() => isLoading = false);
    }
  }

  Future<void> connectToBluetoothSensor() async {
    try {
      if (!(await Permission.bluetoothScan.request().isGranted) ||
          !(await Permission.bluetoothConnect.request().isGranted) ||
          !(await Permission.location.request().isGranted)) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text('⚠️ Требуются разрешения Bluetooth и Геолокации')),
        );
        return;
      }

      FlutterBluePlus.startScan(timeout: const Duration(seconds: 5));

      scanSubscription = FlutterBluePlus.scanResults.listen((results) async {
        for (ScanResult result in results) {
          if (result.device.name == "HM-10") {
            await scanSubscription?.cancel();
            FlutterBluePlus.stopScan();
            await result.device.connect();

            setState(() => bluetoothConnected = true);

            final services = await result.device.discoverServices();
            for (var service in services) {
              for (var characteristic in service.characteristics) {
                if (characteristic.properties.notify) {
                  await characteristic.setNotifyValue(true);
                  characteristic.value.listen((value) {
                    final jsonStr = utf8.decode(value);
                    try {
                      final sensorData = json.decode(jsonStr);
                      PlantApiService.sendSensorDataToBackend(
                        plantId: widget.plantId,
                        sensorData: sensorData,
                      );
                    } catch (e) {
                      print("\u274c Ошибка разбора JSON: $e");
                    }
                  });
                }
              }
            }
            break;
          }
        }
      });
    } catch (e) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('❌ Ошибка Bluetooth: $e')),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: CustomAppBar(
        title: 'Растение',
        actions: [
          IconButton(
            icon: const Icon(Icons.arrow_back, color: Colors.black),
            onPressed: () => Navigator.pop(context),
          ),
        ],
      ),
      backgroundColor: const Color(0xFFF3E3B4),
      body: isLoading
          ? const Center(child: CircularProgressIndicator())
          : details == null
          ? const Center(child: Text('Ошибка загрузки данных'))
          : SingleChildScrollView(
        child: Column(
          children: [
            const SizedBox(height: 20),
            widget.photoUrl.isNotEmpty
                ? Image.network(widget.photoUrl, height: 200, fit: BoxFit.cover)
                : Image.asset('assets/plant.png', height: 200, fit: BoxFit.cover),
            const SizedBox(height: 20),
            Container(
              decoration: BoxDecoration(
                color: const Color(0xFF314D36),
                borderRadius: BorderRadius.circular(24),
              ),
              margin: const EdgeInsets.symmetric(horizontal: 16),
              padding: const EdgeInsets.all(16),
              child: Column(
                children: [
                  Text(details!.name,
                      style: const TextStyle(color: Colors.white, fontSize: 20, fontWeight: FontWeight.bold)),
                  Text(details!.type,
                      style: const TextStyle(color: Colors.white70, fontSize: 14)),
                  const SizedBox(height: 16),
                  Row(
                    mainAxisAlignment: MainAxisAlignment.spaceAround,
                    children: [
                      _buildSensorColumn('humidity', details?.lastSensorData?.humidity, '%'),
                      _buildSensorColumn('soil', details?.lastSensorData?.soilMoisture, '%'),
                      _buildSensorColumn('temp', details?.lastSensorData?.temperature, '°C'),
                      _buildSensorColumn('light', details?.lastSensorData?.light, ''),
                      _buildSensorColumn('gas', details?.lastSensorData?.gasQuality, ''),
                    ],
                  ),
                  const SizedBox(height: 12),
                  _buildTextRow("Последняя дата полива:", details?.lastWatered?.toString()),
                  _buildTextRow("Следующая дата полива:", details?.nextWatering?.toString()),
                  const SizedBox(height: 16),
                  if (details?.lastRecommendation != null)
                    Container(
                      padding: const EdgeInsets.all(12),
                      decoration: BoxDecoration(
                        color: const Color(0xFFF6E7C1),
                        borderRadius: BorderRadius.circular(16),
                      ),
                      child: Text(
                        "Рекомендация последняя от Gemini\n" +
                            details!.lastRecommendation!,
                        style: const TextStyle(fontSize: 13),
                        textAlign: TextAlign.center,
                      ),
                    ),
                ],
              ),
            ),
            const SizedBox(height: 10),
            Row(
              children: [
                const SizedBox(width: 16),
                const Icon(Icons.bluetooth),
                const SizedBox(width: 8),
                const Text('Подключить сенсор'),
                const Spacer(),
                Switch(
                  value: isCollectingData,
                  onChanged: (val) async {
                    setState(() => isCollectingData = val);
                    if (val) await connectToBluetoothSensor();
                  },
                ),
                const SizedBox(width: 16),
              ],
            ),
            const SizedBox(height: 16),
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceEvenly,
              children: [
                _buildActionButton("Обновить фото", () {
                  Navigator.push(
                    context,
                    MaterialPageRoute(
                      builder: (context) => ChangePhotoScreen(
                        plantId: widget.plantId,
                        photoUrl: widget.photoUrl,
                      ),
                    ),
                  );
                }),
                _buildActionButton("Диагностика", () {
                  Navigator.push(
                    context,
                    MaterialPageRoute(
                      builder: (context) => DiagnosticsScreen(plantId: widget.plantId),
                    ),
                  );
                }),
                _buildActionButton("История", () {
                  Navigator.push(
                    context,
                    MaterialPageRoute(
                      builder: (context) => HistoryScreen(plantId: widget.plantId),
                    ),
                  );
                }),
              ],
            ),
            const SizedBox(height: 20),
          ],
        ),
      ),
    );
  }

  Widget _buildSensorColumn(String label, num? value, String unit) {
    return Column(
      children: [
        Text(
          value != null ? '$value$unit' : '—',
          style: const TextStyle(color: Colors.white, fontSize: 18, fontWeight: FontWeight.bold),
        ),
        Text(label,
            textAlign: TextAlign.center,
            style: const TextStyle(color: Colors.white70, fontSize: 10)),
      ],
    );
  }

  Widget _buildTextRow(String label, String? value) {
    return Row(
      children: [
        Text(label, style: const TextStyle(color: Colors.white)),
        const SizedBox(width: 6),
        Expanded(
          child: Text(value ?? '—',
              style: const TextStyle(color: Colors.white70, fontSize: 10)),
        ),
      ],
    );
  }

  Widget _buildActionButton(String text, VoidCallback onPressed) {
    return ElevatedButton(
      onPressed: onPressed,
      style: ElevatedButton.styleFrom(
        backgroundColor: const Color(0xFFF4D79F),
        padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 8),
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(10)),
      ),
      child: Text(text, style: const TextStyle(color: Colors.white)),
    );
  }
}
