
//screens/home_screen.dart

import 'package:flutter/material.dart';
import 'package:SunGreen/screens/plant_screen.dart';
import '../endpoints.dart';
import '../local_notificationService.dart';
import 'add_plant_screen.dart';
import 'models/plant.dart';
import 'package:timezone/timezone.dart' as tz;

class HomeScreen extends StatefulWidget {
  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  late Future<List<Plant>> _plantsFuture;
  bool _shouldWater = false;

  @override
  void initState() {
    super.initState();
    _plantsFuture = PlantApiService.fetchPlants();
    LocalNotificationService.initialize();
    _checkWateringStatus();
    _scheduleDailyReminder();
  }

  Future<void> _checkWateringStatus() async {
    bool result = await PlantApiService.shouldWaterPlantsToday();
    setState(() {
      _shouldWater = result;
    });
    if (_shouldWater) {
      LocalNotificationService.showReminderNotification();
    }
  }

  Future<void> _scheduleDailyReminder() async {
    final now = DateTime.now();
    DateTime scheduleTime = DateTime(now.year, now.month, now.day, 11);
    if (scheduleTime.isBefore(now)) {
      scheduleTime = scheduleTime.add(const Duration(days: 1));
    }
    await LocalNotificationService.showReminderNotificationAt(scheduleTime);
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFFF9EED9),
      floatingActionButton: FloatingActionButton(
        onPressed: () async {
          await showDialog(
            context: context,
            builder: (context) => Dialog(child: AddPlantScreen()),
          );
          setState(() {
            _plantsFuture = PlantApiService.fetchPlants();
          });
        },
        backgroundColor: const Color(0xFF688C28),
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(50)),
        child: const Icon(Icons.add, color: Colors.white),
      ),
      body: Stack(
        children: [
          SingleChildScrollView(
            padding: const EdgeInsets.all(16),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                TextField(
                  decoration: InputDecoration(
                    hintText: 'Поиск',
                    filled: true,
                    fillColor: Colors.grey[200],
                    border: OutlineInputBorder(
                      borderRadius: BorderRadius.circular(12),
                      borderSide: BorderSide.none,
                    ),
                  ),
                ),
                const SizedBox(height: 20),
                FutureBuilder<List<Plant>>(
                  future: _plantsFuture,
                  builder: (context, snapshot) {
                    if (snapshot.connectionState == ConnectionState.waiting) {
                      return const Center(child: CircularProgressIndicator());
                    }
                    if (snapshot.hasError) {
                      return Center(child: Text('Ошибка: ${snapshot.error}'));
                    }
                    if (!snapshot.hasData || snapshot.data!.isEmpty) {
                      return const Center(child: Text('Список растений пуст'));
                    }
                    final plants = snapshot.data!;
                    return ListView.builder(
                      shrinkWrap: true,
                      itemCount: plants.length,
                      physics: const NeverScrollableScrollPhysics(),
                      itemBuilder: (context, index) {
                        final plant = plants[index];
                        return ListTile(
                          leading: CircleAvatar(
                            backgroundImage: (plant.photoUrl != null && plant.photoUrl!.isNotEmpty)
                                ? NetworkImage(plant.photoUrl!)
                                : const AssetImage('assets/plant.png') as ImageProvider,
                          ),
                          title: Text(plant.name),
                          subtitle: Text(plant.type),
                          onTap: () {
                            Navigator.push(
                              context,
                              MaterialPageRoute(
                                builder: (context) => PlantScreen(
                                  plantId: plant.id,
                                  photoUrl: plant.photoUrl ?? '',
                                ),
                              ),
                            );
                          },
                        );
                      },
                    );
                  },
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}
