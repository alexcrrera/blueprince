# src/handler_base.py
from abc import ABC, abstractmethod
import pygame
import sys
import os
import time
from collections import defaultdict


class BaseHandler(ABC):
    """
    Classe abstraite servant de base commune à tous les gestionnaires du projet.

    Chaque Handler :
        - reçoit une référence à HandleData (self.data)
        - doit implémenter la méthode update()
        - peut être utilisé comme élément générique dans d’autres handlers

    Cette classe définit l’interface minimale que doivent respecter
    les gestionnaires d’UI, d’audio, d’entrée clavier, de grille, etc.
    """

    def __init__(self,data=None):
        """
        Initialise un handler générique.

        Args:
            data: Objet HandleData contenant le contexte global du jeu.
                  Peut être None si le handler n’a pas besoin de données globales.
        """
        self.data = data

    @abstractmethod
    def update(self):
        """
        Méthode appelée à chaque frame par le moteur de jeu.
        Doit être définie par les classes filles.
        """
        pass
    
    def __repr__(self):
        """
        Retourne un nom lisible pour le débugging.

        Returns:
            str: Le nom de la classe entre chevrons (ex: <HandleInputs>)
        """
        return f"<{self.__class__.__name__}>"


class Handlerception(BaseHandler):
    """
    Un gestionnaire permettant d’agréger plusieurs handlers et
    de les mettre à jour dans un ordre déterminé.

    Cette classe est utilisée comme "super-handler" capable
    d'orchestrer plusieurs sous-composants :
        - HandleScreen
        - HandleGridUI
        - HandleInputs
        - HandleText
        - etc.

    Le nom “Handlerception” provient du fait qu’il contient des handlers
    dans un handler. "A dream within a dream"
    """
   
    def __init__(self, data):
        """
        Initialise la liste des sous-handlers.

        Args:
            data: Référence HandleData transmise aux handlers enfants.
        """
        super().__init__(data)
        self.handlingFunctions = list()

    def addHandler(self,handler):
        """
        Ajoute un handler enfant qui sera mis à jour automatiquement.

        Args:
            handler: Instance dérivée de BaseHandler.
        """
        self.handlingFunctions.append(handler)

    def update(self):
        """
        Met à jour l'ensemble des handlers enfants dans l'ordre où ils ont été ajoutés.
        """
        for hanlder in self.handlingFunctions:
            hanlder.update()
