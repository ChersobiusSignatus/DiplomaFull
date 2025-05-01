
//screens/change_photo_screen.dart

import 'dart:io';
import 'package:flutter/material.dart';
import 'package:image_picker/image_picker.dart';

import '../endpoints.dart';
import '../widgets/custom_app_bar.dart';

class ChangePhotoScreen extends StatefulWidget {
  final String plantId;
  final String photoUrl;

  const ChangePhotoScreen({super.key,required this.plantId,required this.photoUrl});

  @override
  State<ChangePhotoScreen> createState() => _ChangePhotoScreenState();
}

class _ChangePhotoScreenState extends State<ChangePhotoScreen> {
  File? _selectedImage;
  final ImagePicker _picker = ImagePicker();
  late  String imagePath = '';
  Future<void> _pickImage() async {
    final pickedFile = await _picker.pickImage(source: ImageSource.gallery);
    if (pickedFile != null) {
      imagePath=pickedFile.path;
      print('Путь к изображению: ${pickedFile.path}');

      setState(() {
        _selectedImage = File(pickedFile.path);
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: CustomAppBar(
        title: 'title',
        actions: [
          IconButton(
            icon: const Icon(Icons.arrow_back, color: Colors.black),
            onPressed: () {
              Navigator.pop(context);
            },
          )
        ],
      ),
      backgroundColor: const Color(0xFFF3E3B4),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            _selectedImage != null
                ? Image.file(
              _selectedImage!,
              width: MediaQuery.of(context).size.width * 0.5,
              height: MediaQuery.of(context).size.height * 0.5,
              fit: BoxFit.cover,
            )
                :  (widget.photoUrl.isNotEmpty)
                ? Image.network(
              widget.photoUrl,
              height: 200,
              fit: BoxFit.cover,
              loadingBuilder: (context, child, loadingProgress) {
                if (loadingProgress == null) return child;
                return Center(child: CircularProgressIndicator());
              },
              errorBuilder: (context, error, stackTrace) {
                return Image.asset(
                  'assets/plant.png',
                  height: 200,
                  fit: BoxFit.cover,
                );
              },
            )
                : Image.asset(
              'assets/plant.png',
              height: 200,
              fit: BoxFit.cover,
            ),
            const SizedBox(height: 20),
            ElevatedButton(
              onPressed: _pickImage,
              style: ElevatedButton.styleFrom(
                padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 3),
                backgroundColor: const Color(0xFFF4D79F),
                shape: RoundedRectangleBorder(
                  borderRadius: BorderRadius.circular(10),
                ),
                elevation: 5,
              ),
              child: const Text(
                'Выбрать',
                style: TextStyle(color: Colors.white, fontSize: 14),
              ),
            ),
            const SizedBox(height: 10),
            ElevatedButton(
              onPressed: () async {
                final result = await PlantApiService.uploadPhoto(  plantId: widget.plantId, imageFile: File(imagePath),
                );

                if (result) {
                  ScaffoldMessenger.of(context).showSnackBar(
                    SnackBar(content: Text('Фото успешно отправлено!')),
                  );
                } else {
                  ScaffoldMessenger.of(context).showSnackBar(
                    SnackBar(content: Text('Ошибка, Фото не сохранено!.')),
                  );
                }
                Navigator.pop(context);
              },
              style: ElevatedButton.styleFrom(
                padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 3),
                backgroundColor: const Color(0xFFF4D79F),
                shape: RoundedRectangleBorder(
                  borderRadius: BorderRadius.circular(10),
                ),
                elevation: 5,
              ),
              child: const Text(
                'Сохранить',
                style: TextStyle(color: Colors.white, fontSize: 14),
              ),
            ),
          ],
        ),
      ),
    );
  }
}

