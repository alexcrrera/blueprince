class Door:
    """
    Représente une porte reliant deux pièces.
    - level_lock : niveau de verrouillage (0=ouverte, 1=verrouillée, 2=double verrou)
    - is_open : indique si la porte est ouverte
    - connected_room : référence vers la pièce reliée
    """

    def __init__(self, level_lock: int = 0):
        self.level_lock = level_lock
        self.is_open = (level_lock == 0)
        self.connected_room = None

    def open(self):
        """Ouvre la porte (pour l’instant sans gestion de clés)."""
        # Toutes les portes sont ouvertes pour l’instant
        self.is_open = True

    def __repr__(self):
        # Affiche l'état de la porte (ouverte ou verrouillée) - TEST
        state = "ouverte" if self.is_open else f"verrouillée (lvl {self.level_lock})"
        return f"Door {state}"