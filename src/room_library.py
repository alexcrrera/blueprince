import json, random, os
from src.room import Room

class RoomLibrary:
    def __init__(self, json_path="src/rooms.json"):
        with open(json_path, "r", encoding="utf-8") as f:
            self.rooms_data = json.load(f)
        self.remaining_rooms = list(self.rooms_data.keys())

    def draw_random_rooms(self, n=3):
        """Retourne n chambres tirées aléatoirement selon leur rareté."""
        pool = []
        for name, data in self.rooms_data.items():
            # Plus la rareté est élevée, moins la pièce apparaît
            weight = 1 / (3 ** data["rarity"])
            pool.append((name, weight))
        names = random.choices(
            [name for name, _ in pool],
            weights=[w for _, w in pool],
            k=n
        )
        return [name for name in names]

    def create_room_instance(self, name, x, y):
        """Instancie une Room à partir du JSON."""
        return Room(name, self.rooms_data[name], x, y)