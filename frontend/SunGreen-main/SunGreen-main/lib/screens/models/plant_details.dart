//models/plant_details.dart

class PlantDetails {
  final String plantId;
  final String name;
  final String type;
  final DateTime? lastWatered;
  final DateTime? nextWatering;
  final String? lastPhoto;
  final SensorData? lastSensorData;
  final String? lastRecommendation;

  PlantDetails({
    required this.plantId,
    required this.name,
    required this.type,
    this.lastWatered,
    this.nextWatering,
    this.lastPhoto,
    this.lastSensorData,
    this.lastRecommendation,
  });

  factory PlantDetails.fromJson(Map<String, dynamic> json) {
    return PlantDetails(
      plantId: json['plant_id'],
      name: json['name'],
      type: json['type'],
      lastWatered: json['last_watered'] != null && json['last_watered'] is String
          ? DateTime.tryParse(json['last_watered'])
          : null,
      nextWatering: json['next_watering'] != null && json['next_watering'] is String
          ? DateTime.tryParse(json['next_watering'])
          : null,
      lastPhoto: json['last_photo'],
      lastSensorData: json['last_sensor_data'] != null
          ? SensorData.fromJson(json['last_sensor_data'])
          : null,
      lastRecommendation: json['last_gemini_recommendation']?['text'],
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'plant_id': plantId,
      'name': name,
      'type': type,
      'last_watered': lastWatered?.toIso8601String().split("T")[0],
      'next_watering': nextWatering?.toIso8601String().split("T")[0],
      'last_photo': lastPhoto,
      'last_sensor_data': lastSensorData?.toJson(),
      'last_recommendation': lastRecommendation,
    };
  }

  String? get formattedLastWatered => lastWatered != null
      ? "${lastWatered!.year.toString().padLeft(4, '0')}-${lastWatered!.month.toString().padLeft(2, '0')}-${lastWatered!.day.toString().padLeft(2, '0')}"
      : null;

  String? get formattedNextWatering => nextWatering != null
      ? "${nextWatering!.year.toString().padLeft(4, '0')}-${nextWatering!.month.toString().padLeft(2, '0')}-${nextWatering!.day.toString().padLeft(2, '0')}"
      : null;
}

class SensorData {
  final double? temperature;
  final double? humidity;
  final double? soilMoisture;
  final double? light;
  final double? gasQuality;
  final DateTime? createdAt;

  SensorData({
    this.temperature,
    this.humidity,
    this.soilMoisture,
    this.light,
    this.gasQuality,
    this.createdAt,
  });

  factory SensorData.fromJson(Map<String, dynamic> json) {
    return SensorData(
      temperature: json['temperature']?.toDouble(),
      humidity: json['humidity']?.toDouble(),
      soilMoisture: json['soil_moisture']?.toDouble(),
      light: json['light']?.toDouble(),
      gasQuality: json['gas_quality']?.toDouble(),
      createdAt: json['created_at'] != null && json['created_at'] is String
          ? DateTime.tryParse(json['created_at'])
          : null,
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'temperature': temperature,
      'humidity': humidity,
      'soil_moisture': soilMoisture,
      'light': light,
      'gas_quality': gasQuality,
      'created_at': createdAt?.toIso8601String(),
    };
  }
}
