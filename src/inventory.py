from src import params

class Inventory:
    """
    Représente l'inventaire du joueur ou celui d'une salle.

    L'inventaire contient :
        - des objets consommables (gold, gems, keys, dice, steps_left, etc.)
        - des objets permanents/spéciaux (selon ITEMS_DESCRIPTION_DICT)
        - des objets spécifiques aux salles ("actions")

    Il gère également :
        - l'ajout et le retrait d'objets
        - la mise à jour des informations affichées dans l'UI
        - la mise à jour de l'historique textuel de l'UI des gains/pertes d'objets
    """

    
    def __init__(self,items_dict,data,is_self_player=False):
        """
        Initialise un inventaire.

        Args:
            items_dict (dict): Dictionnaire contenant les objets déjà présents.
            data: Référence vers l'objet global HandleData.
            is_self_player (bool): True si cet inventaire est celui du joueur.
        """
        self.data = data

        # Dictionnaire des objets (consommables, permanents selon les cas)
        self.items = items_dict

        # Structure utilisée uniquement pour l'affichage UI
        self.ui_items = [0,0,0,0]

        self.isPlayerInventory = is_self_player # bool: est inventaire du joueur ou pas
    

    def getItemQ(self,item):
        """
        Retourne la quantité associée à un objet donné.

        Args:
            item (str): Nom de l'objet.

        Returns:
            int: Quantité, ou 0 si l'objet n'est pas présent.
        """
        if item not in self.items:
            return 0
        else:
            return self.items.get(item)
   
    def update(self):
        """
        Met à jour ui_items, utilisé pour l'affichage en temps réel dans l'UI.
        Les objets suivis sont steps_left, gold, gems, keys et dice.
        """
        gold = self.getItemQ("gold")
        gems = self.getItemQ("gems")
        steps_left = self.getItemQ("steps_left")
        dice = self.getItemQ("dice")
        keys = self.getItemQ("keys")

        # Ordre utilisé par la partie UI
        self.ui_items = [steps_left,gold, gems, keys,dice]
        

    def addItem(self,item,q):
        """
        Ajoute un item dans l'inventaire.

        Cas spéciaux :
            - Si l'objet est un consommable et que l'inventaire est celui du joueur,
              handleConsommable() est appelé directement.
            - La modification est enregistrée dans l'historique textuel de l'UI si isPlayerInventory=True.

        Args:
            item (str): Nom de l'objet.
            q (int): Quantité à ajouter.
        """
        
        consomables = params.POSSIBLE_CONSUMABLES_DICT

        # Cas des consommables propres au joueur (nourriture, etc.)
        if item in consomables and self.isPlayerInventory:
            self.handleConsommable(item)
            return

        # Ajout dans l'inventaire
        if(item not in self.items): # Si objet pas encore dans l'inventaire alors initialisation
            self.items[item]= q
        else: # sinon mis à jour simple du compteur
            self.items[item] +=q


        # Ajout dans l'historique (uniquement pour le joueur)
        if self.isPlayerInventory:
            descriptor = params.ITEMS_DESCRIPTION_DICT[item] # dictionnaire associé à l'item 
            verb = descriptor[4].lower() #recupère verbe associé à l'action quand c'est le joueur qui prend l'objet pour le mettre dans son inventaire
            self.data.updateHistory(item,q,verb=verb)
        

        
        


    def handleConsommable(self,item):
        """
        Gestion spéciale des consommables consommés immédiatement (nourriture...).

        Args:
            item (str): Nom du consommable.
        """
        consomables = params.POSSIBLE_CONSUMABLES_DICT # dictionnaire avec consommables possibles
        steps_gained = consomables.get(item).get("gives") # recupère nombre de pas que le consommable donne

    
        self.addItem("steps_left",steps_gained) # ajoute ce nombre au compteur de pas
      


    def removeItems(self,item,q,keep_item=False):
        """
        Retire un objet de l'inventaire.

        Args:
            item (str): Nom de l'objet.
            q (int): Quantité à retirer.
            keep_item (bool): Si True, l'objet reste dans le dict même à 0.

        Raises:
            TypeError: si l'objet n'existe pas.
        """
        if self.isPlayerInventory:
            keep_item = True  # les objets du joueur restent visibles même à 0
        else:
            keep_item = False # les objets des chambres avec quantité nulle sont retirés

        if(item not in self.items): 
            raise TypeError("Item non présent dans l'inventaire!") # debugging
        else:
            self.items[item] -=q #on enlève q quantité de l'item

            if(self.items[item]<=0): # si quantité nulle alors:
                if not keep_item:
                    self.items.pop(item, None) # si inventaire de chambre alors on le retire
                else:
                    self.items[item] = 0  # l'objet reste avec quantité 0
            
        descriptor = params.ITEMS_DESCRIPTION_DICT[item]

        # Mise à jour de l'historique textuel de l'UI (uniquement si joueur)
        if(self.isPlayerInventory):
            verb = descriptor[5].lower() # recupère le verbe textuel associé à l'action quand c'est le joueur qui enlève l'objet de son inventaire
            self.data.updateHistory(item,q,verb=verb)     

 

    def getSpecialItems(self):
        """
        Retourne les objets permanents ou spéciaux du joueur. Utilisé pour l'affichage UI

        Returns:
            dict: Clés = nom des objets spéciaux, valeur = quantité.
        """
        special_items = {}
        for item in self.items:
            descriptor = params.ITEMS_DESCRIPTION_DICT.get(item)[2] # récupère le type d'item
            if(descriptor=="p"):
                special_items[item] = self.items.get(item)
        
        return special_items


    def __repr__(self):
        """
        Représentation interne de l'inventaire (debug). Jamais utilisé.

        Returns:
            str: Informations sur certains objets principaux.
        """
        return f"Inventory gems={self.gems} dice={self.dice} gold={self.gold}"
    


class RoomInventory(Inventory):
    """
    Inventaire interne à une Room.

    Hérite d’Inventory, et ajoute :
        - un dictionnaire d'actions disponibles dans la salle
          (creuser, ouvrir coffre, etc.)
    """

    def __init__(self, items_dict,actions_dict,data):
        """
        Initialise un inventaire de salle.

        Args:
            items_dict (dict): Objets forcément présents dans la salle.
            actions_dict (dict): Actions réalisables dans la salle.
            data: Référence DATA globale.
        """
        super().__init__(items_dict,data)
        self.actions = actions_dict
        


    def addAction(self,action,q):
        """
        Ajoute une action à l'inventaire de la salle. Par action on nomme les emplacements
        pour creuser, acheter banane...

        Args:
            action (str): Nom de l'action.
            q (int): Quantité/compteur associé.
        """
        if(action not in self.actions):
            self.actions[action]= q
        else:
            self.actions[action] +=q
    

    def removeActions(self,action,q):
        """
        Retire une action de la salle.

        Args:
            action (str): Nom de l'action.
            q (int): Quantité à retirer.

        Raises:
            TypeError: si l'action n'existe pas.
        """
        if(action not in self.actions):
            raise TypeError("Action non présente dans la salle")
        else:
            self.actions[action] -=q

            if(self.actions[action]<=0): # si quantité action inférieur à 1 alors on l'enlève
                self.actions.pop(action, None)
        

        
    def getActionQ(self,action):
        """
        Retourne la quantité associée à une action.

        Args:
            action (str): Nom de l'action.

        Returns:
            int: Quantité, ou 0 si absente.
        """
        if action not in self.actions:
            return 0
        else:
            return self.actions.get(action)



    def update(self):
        """
        Met à jour l'inventaire de salle (hérite du comportement général).
        """
        return super().update()
