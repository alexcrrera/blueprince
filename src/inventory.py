from src.item import Item

from src import params

class Inventory:
    """
    Représente l'inventaire du joueur uniquement.
    - consommable: gemmes, clés, dés, pièces d'or, etc.
    - liste d'objets permanents: pelle, marteau, etc.
    """
    # C'est comme un sac à dos
    
    def __init__(self,items_dict):
        # Ressources de base
        self.items = items_dict
        self.gold = self.getItemQ("gold")
        self.gems = self.getItemQ("gems")
        self.steps_left = self.getItemQ("steps_left")
        self.dice = self.getItemQ("dice")
        self.keys = self.getItemQ("keys")

        self.ui_items = [self.steps_left,self.gold,self.gems, self.keys,self.dice] #for inventory ui

        # Objets permanents (pelle, marteau, etc.)
        self.permanent_items = []


    


    def getItemQ(self,key):

        if key not in self.items:
            return 0
        
        else:
            return self.items.get(key)
   
    def update(self):
        self.gold = self.getItemQ("gold")
        self.gems = self.getItemQ("gems")
        self.steps_left = self.getItemQ("steps_left")
        self.dice = self.getItemQ("dice")
        self.keys = self.getItemQ("keys")
        self.ui_items = [self.steps_left,self.gold, self.gems, self.keys,self.dice]
        

    def addItem(self,key,q):
        if(key not in self.items):
            self.items[key]= q
        else:
            self.items[key] +=q


    def removeItems(self,key,q):

        print("Reomving", key, " x ", q)
        if(key not in self.items):
            raise TypeError("Can't remove remove what's not there!")
        else:
            self.items[key] -=q


            if(self.items[key]<=0):
                self.items.pop(key, None)
            
                print("CAREFUL REMOVING MORE THAN WE HAVE !")



    def __repr__(self):
        # Affiche les objets de l'inventaire - TEST
        return f"Inventory gems={self.gems} keys={self.keys} dice={self.dice} gold={self.gold} permanent_items={self.permanent_items}"
    


class RoomInventory(Inventory):

    def __init__(self, items_dict,actions_dict):
        super().__init__(items_dict)
        self.actions = actions_dict
        




    def addAction(self,key,q):
        if(key not in self.actions):
            self.actions[key]= q
        else:
            self.actions[key] +=q
    

    def removeActions(self,key,q):
        print("Reomving", key, " x ", q)
        if(key not in self.actions):
            raise TypeError("Can't remove remove what's not there!")
        else:
            self.actions[key] -=q


            if(self.actions[key]<=0):
                self.actions.pop(key, None)
            
                print("CAREFUL REMOVING MORE THAN WE HAVE !")

        
    def getActionQ(self,key):
        if key not in self.actions:
            return 0
        
        else:
            return self.actions.get(key)



    def update(self):
        return super().update()