from src.item import Item

from src import params

class Inventory:
    """
    Représente l'inventaire du joueur uniquement.
    - consommable: gemmes, clés, dés, pièces d'or, etc.
    - liste d'objets permanents: pelle, marteau, etc.
    """
    # C'est comme un sac à dos
    
    def __init__(self):
        # Ressources de base
        self.gems = params.INITIAL_GEMS # Initialement à 2 (énoncé)
        self.keys = params.INTIAL_KEY
        self.dice = params.INTIAL_DICE
        self.gold = params.INTIAL_GOLD
        self.steps_left = params.INITIAL_STEPS 

        self.ui_items = [self.steps_left,self.gold,self.gems, self.keys,self.dice] #for inventory ui

        # Objets permanents (pelle, marteau, etc.)
        self.permanent_items = []

    def add_item(self, item: Item):
        """Ajoute un objet à l'inventaire selon son type."""
        if item.type == "permanent":
            self.permanent_items.append(item)
            print(f"Objet permanent ajouté : {item.name}")

        elif item.type == "consommable":
        # selon le nom, on met à jour le compteur
        # Pour l'instant tout est a 1 -> TODO: gérer les quantités
            if item.name == "clé":
                self.keys += 1
            elif item.name == "dé":
                self.dice += 1
            elif item.name == "gemme":
                self.gems += 1
            elif item.name == "or":
                self.gold += 1
            print(f"Objet consommable ramassé : {item.name}")

        else:
            print(f"Type d'objet inconnu : {item.name}")

    def add_item(self, item: Item):
        """Ajoute un objet à l'inventaire selon son type."""
        
        # Vérifie que l'objet existe
        if item is None:
            print("Aucun objet à ajouter (item = None)")
            return

        # Cas 1 : objet permanent
        if item.type == "permanent":
            self.permanent_items.append(item)
            print(f"Objet permanent ajouté : {item.name}")

        # Cas 2 : consommable
        elif item.type == "consommable":
            if item.name == "clé":
                self.keys += 1
            elif item.name == "dé":
                self.dice += 1
            elif item.name == "gemme":
                self.gems += 1
            elif item.name == "or":
                self.gold += 1
            print(f"Objet consommable ramassé : {item.name}")

        # Cas 3 : type non reconnu
        else:
            print(f"Type d'objet inconnu pour {item.name}")


    def has_item(self, name: str):
        """Vérifie si un objet est présent (permanent ou consommable)."""
        
        # 1 Objets permanents
        if any(i.name == name for i in self.permanent_items):
            return True

        # 2 Objets consommables
        if name == "clé" and self.keys > 0:
            return True
        elif name == "dé" and self.dice > 0:
            return True
        elif name == "gemme" and self.gems > 0:
            return True
        elif name == "or" and self.gold > 0:
            return True

        # 3 Si rien trouvé
        return False

    def update(self):
        self.ui_items = [self.steps_left,self.gold,self.gems, self.keys,self.dice]


    def __repr__(self):
        # Affiche les objets de l'inventaire - TEST
        return f"Inventory gems={self.gems} keys={self.keys} dice={self.dice} gold={self.gold} permanent_items={self.permanent_items}"