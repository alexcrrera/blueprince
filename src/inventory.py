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

    

        self.ui_items = [0,0,0,0]
        # Objets permanents (pelle, marteau, etc.)
        self.permanent_items = []


    


    def getItemQ(self,key):

        if key not in self.items:
            return 0
        
        else:
            return self.items.get(key)
   
    def update(self):
        gold = self.getItemQ("gold")
        gems = self.getItemQ("gems")
        steps_left = self.getItemQ("steps_left")
        dice = self.getItemQ("dice")
        keys = self.getItemQ("keys")
        self.ui_items = [steps_left,gold, gems, keys,dice]
        

    def addItem(self,key,q):
        if(key not in self.items):
            self.items[key]= q
        else:
            self.items[key] +=q


    def removeItems(self,key,q,data,keep_item=False):
        self.data = data

        print("Removing", key, " x ", q)
        self.data.updateHistory(key,q)
        if(key not in self.items):
            raise TypeError("Can't remove remove what's not there!")
        else:
            self.items[key] -=q


            if(self.items[key]<=0):
                if not keep_item:
                    self.items.pop(key, None)
                else:
                    self.items[key] = 0 # keeps in inventory at 0
            
                print("CAREFUL REMOVING MORE THAN WE HAVE !")


    def getSpecialItems(self):
        special_items = {}
        for key in self.items:
            descriptor = params.ITEMS_DESCRIPTION_DICT.get(key)
            if(descriptor[2]=="p"): #
                
                
                special_items[key] = self.items.get(key)
        
        return special_items


    def __repr__(self):
        # Affiche les objets de l'inventaire - TEST
        return f"Inventory gems={self.gems} dice={self.dice} gold={self.gold} permanent_items={self.permanent_items}"
    


class RoomInventory(Inventory):

    def __init__(self, items_dict,actions_dict):
        super().__init__(items_dict)
        self.actions = actions_dict
        




    def addAction(self,key,q):
        print("Adding action: ", key, " x ", q)
        if(key not in self.actions):
            self.actions[key]= q
        else:
            self.actions[key] +=q
    

    def removeActions(self,key,q):
        print("Removing action: ", key, " x ", q)
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