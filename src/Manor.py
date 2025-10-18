import json
from src.room import Room
from src import params

class RoomGrid:
    def __init__(self, data):
        # Grille vide
        self.mansion = [[None for _ in range(params.ROOM_GRID_SIZE_VERTICAL)] for _ in range(params.ROOM_GRID_SIZE_HORIZONTAL)]

        # Position du joueur au début
        x, y = data.roomX, data.roomY

        # Charger le JSON des rooms
        with open("src/rooms.json", "r") as f:
            rooms_data = json.load(f)

        # 🔹 Au lancement : on place uniquement l’Entrance Hall, sans tirage
        entrance_data = rooms_data.get("Entrance_Hall")
        if entrance_data:
            entrance_room = Room("Entrance_Hall", entrance_data, x, y)
            self.mansion[x][y] = entrance_room
            print("🏰 Salle de départ : Entrance_Hall")
        else:
            print("Erreur : 'Entrance_Hall' introuvable dans rooms.json !")

    def update(self):
        pass
 