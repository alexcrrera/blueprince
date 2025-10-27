# src/handler_base.py
from abc import ABC, abstractmethod
import pygame
import sys
import os
import time
from collections import defaultdict




class BaseHandler(ABC):
    """
    Classe abstraite servant de modèle pour tous les gestionnaires (UI, son, entrée, etc.)
    """

    def __init__(self,data=None):
        """
        :param data: référence à l'objet HandleData (facultatif)
        """
        self.data = data


    @abstractmethod
    def update(self):
        """
        Méthode appelée à chaque frame.
        Chaque gestionnaire doit implémenter sa logique de mise à jour ici.
        """
        pass
    
    def __repr__(self):
        """Nom lisible pour debug."""
        return f"<{self.__class__.__name__}>"



class Handlerception(BaseHandler):
    """Fonction principale qui appelle tous les handlers
    
    """
    def __init__(self, data):
        super().__init__(data)
        self.handlingFunctions = list()



    def update(self):
        for h in self.handlingFunctions:
            h.update()
   