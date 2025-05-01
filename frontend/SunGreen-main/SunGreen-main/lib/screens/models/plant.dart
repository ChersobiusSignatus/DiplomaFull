
//models/plant.dart

class Plant {
  final String id;

  final String name;
  final String type;
  final String? photoUrl;


  Plant({required this.id,required this.name,required this.type,required this.photoUrl});

  factory Plant.fromJson(Map<String, dynamic> json) {
    return Plant(id: json['id'],name: json['name'], type: json['type'], photoUrl: json['photo_url']);
  }
}

