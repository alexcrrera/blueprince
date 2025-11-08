from src.item import Item

from src import params

class Inventory:
    """
    Représente l'inventaire du joueur uniquement.
    - consommable: gemmes, clés, dés, pièces d'or, etc.
    - liste d'objets permanents: pelle, marteau, etc.
    """
    # C'est comme un sac à dos
    
    def __init__(self,items_dict,data,is_self_player=False):

        self.data = data
        # Ressources de base
        self.items = items_dict

    

        self.ui_items = [0,0,0,0]
        # Objets permanents (pelle, marteau, etc.)
        self.permanent_items = []


        self.isPlayerInventory = is_self_player
    

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
        

    def addItem(self,item,q,showHistory=True):


        consomables = params.POSSIBLE_CONSUMABLES_DICT

        # si on prend un consommable depuis l'inventaire du joueur
        if item in consomables and self.isPlayerInventory:
            self.handleConsommable(item)
            return

        if(item not in self.items):
            self.items[item]= q
        else:
            self.items[item] +=q


        descriptor = params.ITEMS_DESCRIPTION_DICT[item]


        if not self.isPlayerInventory:
            return

        else:
            verb = descriptor[4].lower()
            self.data.updateHistory(item,q,verb=verb)


    def handleConsommable(self,item):
        consomables = params.POSSIBLE_CONSUMABLES_DICT
        steps_gained = consomables.get(item).get("costs")
        self.addItem("steps_left",steps_gained)
      

   



    def removeItems(self,item,q,keep_item=False,showHistory=True):
       

       
        if self.isPlayerInventory:
            keep_item = True
        else:
            keep_item = False
        if(item not in self.items):
            raise TypeError("Can't remove remove what's not there!")
        else:
            self.items[item] -=q


            if(self.items[item]<=0):
                if not keep_item:
                    self.items.pop(item, None)
                else:
                    self.items[item] = 0 # keeps in inventory at 0
            
        descriptor = params.ITEMS_DESCRIPTION_DICT[item]

        if(self.isPlayerInventory):
            verb = descriptor[5].lower()
            self.data.updateHistory(item,q,verb=verb)     
 

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

    def __init__(self, items_dict,actions_dict,data):
        super().__init__(items_dict,data)
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