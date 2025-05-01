
//lib/endpoints.dart

import 'dart:convert';
import 'dart:io';
import 'package:flutter/cupertino.dart';
import 'package:http/http.dart' as http;
import 'package:SunGreen/screens/models/plant.dart';
import 'package:SunGreen/screens/models/plant_details.dart';
import 'package:path/path.dart';
import 'package:mime/mime.dart';
import 'package:http_parser/http_parser.dart';

class PlantApiService {
  static Future<List<Plant>> fetchPlants() async {
    final response = await http.get(
      Uri.parse('http://134.209.254.255:8000/plants/'),
    );
    if (response.statusCode == 200) {
      final List<dynamic> jsonData = json.decode(response.body);
      return jsonData.map((item) => Plant.fromJson(item)).toList();
    } else {
      throw Exception('Failed to load plants');
    }
  }

  static Future<void> addPlant({
    required String name,
    required String type,
    required DateTime lastWatered,
  }) async {
    final url = Uri.parse('http://134.209.254.255:8000/plants/');
    final headers = {'Content-Type': 'application/json'};
    final body = jsonEncode({
      'name': name,
      'type': type,
      'last_watered': lastWatered.toIso8601String(),
    });
    final response = await http.post(url, headers: headers, body: body);
    if (!(response.statusCode == 200 || response.statusCode == 201)) {
      throw Exception('Failed to add plant: ${response.statusCode}');
    }
  }

  static Future<PlantDetails> plantDetails(plantId) async {
    final url = Uri.parse('http://134.209.254.255:8000/plants/$plantId/details');
    final response = await http.get(url);
    if (response.statusCode == 200 && response.body.isNotEmpty) {
      final jsonData = json.decode(response.body);
      return PlantDetails.fromJson(jsonData);
    } else {
      throw Exception('Failed to load plant details');
    }
  }

  static Future<String> diagnoseByPhoto(String plantId) async {
    final url = Uri.parse('http://134.209.254.255:8000/diagnose/photo/$plantId');
    final response = await http.post(url);
    if (response.statusCode == 200) {
      final jsonData = json.decode(response.body);
      return jsonData['content'] ?? 'Нет текста рекомендации';
    } else {
      throw Exception('Ошибка диагностики по фото: ${response.statusCode}');
    }
  }

  static Future<String> diagnoseCombined(String plantId) async {
    final url = Uri.parse('http://134.209.254.255:8000/diagnose/combined/$plantId');
    final response = await http.post(url);
    if (response.statusCode == 200) {
      final jsonData = json.decode(response.body);
      return jsonData['content'] ?? 'Нет текста рекомендации';
    } else {
      throw Exception('Ошибка комбинированной диагностики: ${response.statusCode}');
    }
  }

  static Future<String?> fetchPlantPhoto(String plantId) async {
    final url = Uri.parse('http://134.209.254.255:8000/plants/$plantId/photos');
    final response = await http.get(url);
    if (response.statusCode == 200) {
      final data = json.decode(response.body);
      if (data is List && data.isNotEmpty) {
        return data[0]['s3_url'];
      }
    }
    return null;
  }

  static Future<bool> uploadPhoto({
    required String plantId,
    required File imageFile,
  }) async {
    final uri = Uri.parse('http://134.209.254.255:8000/plants/$plantId/photos');
    final request = http.MultipartRequest('POST', uri);
    final mimeType = lookupMimeType(imageFile.path) ?? 'image/jpeg';
    request.files.add(
      await http.MultipartFile.fromPath(
        'file',
        imageFile.path,
        contentType: MediaType.parse(mimeType),
      ),
    );
    final response = await request.send();
    return response.statusCode == 200 || response.statusCode == 201;
  }

  static Future<Map<String, dynamic>?> fetchPlantHistory({
    required String plantId,
    required String selectedDate,
  }) async {
    final url = 'http://134.209.254.255:8000/plants/plants/$plantId/history/$selectedDate';
    final response = await http.get(Uri.parse(url));
    if (response.statusCode == 200) {
      return json.decode(response.body);
    } else {
      return null;
    }
  }

  static Future<void> sendSensorDataToBackend({
    required String plantId,
    required Map<String, dynamic> sensorData,
  }) async {
    final url = Uri.parse('http://134.209.254.255:8000/plants/$plantId/sensor-data');
    final headers = {'Content-Type': 'application/json'};

    final body = jsonEncode(sensorData);

    final response = await http.post(url, headers: headers, body: body);

    if (response.statusCode == 200 || response.statusCode == 201) {
      print("✅ Сенсорные данные успешно отправлены");
    } else {
      print("❌ Ошибка при отправке данных: ${response.statusCode}");
      print(response.body);
    }
  }


  static Future<bool> shouldWaterPlantsToday() async {
    final url = Uri.parse('http://134.209.254.255:8000/plants/watering-today');
    final response = await http.get(url);
    if (response.statusCode == 200) {
      final data = json.decode(response.body);
      return data is List && data.isNotEmpty;
    }
    return false;
  }

  static Future<void> markPlantAsWatered(String plantId) async {
    final url = Uri.parse('http://134.209.254.255:8000/plants/$plantId/water');
    final response = await http.post(url);

    if (response.statusCode != 200) {
      throw Exception('Ошибка при обновлении даты полива');
    }
  }
}

