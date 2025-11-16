from src.inventory import Inventory

from src import params


class Player:
    """
    Représente le joueur dans le manoir.

    Le Player contient :
        - sa position (x, y) dans la grille
        - sa direction actuelle (0=E, 1=N, 2=W, 3=S)
        - son inventaire (Inventory)
        - les informations nécessaires pour déterminer la pièce suivante
          (next_room_position, next_room_status)

    Le joueur est initialisé à la position de l’Entrance Hall : (2, 8).
    """

    def __init__(self, data):
        """
        Initialise le joueur, sa position et son inventaire.

        Args:
            data: Référence à HandleData, contenant tout l'état global du jeu.
        """
        self.data = data

        # Position initiale (Entrance Hall)
        position = (2, 8)
        self.x = position[0]
        self.y = position[1]

        # Inventaire de départ défini dans params
        starting_inventory = params.INITIAL_ITEMS_DICT
        self.inventory = Inventory(starting_inventory, self.data, is_self_player=True)

        # Direction initiale (le joueur regarde vers le Nord)
        self.direction = 1  # 0 = Est, 1 = Nord, 2 = Ouest, 3 = Sud
        
        # Indique où se trouve la prochaine pièce selon la direction du joueur
        self.next_room_position = [self.x, self.y - 1]
        self.next_room_status = 0  # -1 = vide et générable, 0 = mur, 1 = ouverte, 2 = bloquée à un tour, 3 = bloquée à deux tours
        
    def __repr__(self):
        """
        Représentation lisible du joueur, utilisée pour le débugging.

        Returns:
            str: Position  et inventaire actuel.
        """
        return f"Player x={self.x},y={self.y}   inv={self.inventory}"
    
    def update(self):
        """
        Met à jour l’inventaire du joueur.
        Cette méthode est appelée à chaque frame du jeu.
        """
        # Mise à jour interne de l’inventaire (ex: UI)
        self.inventory.update()

    def addData(self,data):
        """
        Met à jour la référence vers HandleData si nécessaire.

        Args:
            data: Instance HandleData.
        """
        self.data = data
