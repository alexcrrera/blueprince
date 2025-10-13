class Item:
    """
    Représente un objet du jeu.
    - name : nom de l’objet
    - type : 'consommable' ou 'permanent'
    """

    def __init__(self, name: str, type_: str):
        self.name = name   # nom de l’objet ("clé", "gemme", "pelle", etc.)
        self.type = type_  # "consommable" ou "permanent"

    def __repr__(self):
        # Affiche les informations de l'objet - TEST
        return f"Item {self.name} ({self.type})"