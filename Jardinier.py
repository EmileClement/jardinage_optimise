# -*- coding: utf-8 -*-
"""
Created on Mon Apr 20 11:51:41 2020

@author: Leopold
"""
import random as rd

N_bit_espece = 2

#%% Def des classes
class Jardin():
    def __init__(self, len_x: int, len_y: int):
        self.emplacement = [[Emplacement(self) for i in range(len_x)] for i in range(len_y)]

    def __repr__(self):
        return "Jardin({},{})".format(len(self.emplacement[0]), len(self.emplacement))


class Emplacement():
    def __init__(self, jardin):
        self.jardin = jardin
        self.calendrier = [Jachere() for i in range(365)]

    def __repr__(self):
        return "Emplacement: " + ", ".join([str(i) + ":" + elem.__repr__()
                                            for i, elem in
                                            enumerate(self.calendrier)]) + ";"

    def libre(self, debut, fin):
        libre = True
        for elem in self.calendrier[debut:fin]:
            libre &= isinstance(elem, Jachere)
        return libre

class Occupant():
    def __init__(self):
        assert 0, "Not implemeted"

class Jachere(Occupant):
    def __init__(self):
        pass

    def __repr__(self):
        return "Jachère"

class Plante(Occupant):
    def __init__(self):
        self.plantage = [False]*365
        self.time_chunk = 0
        self.masse_produite = 0
        self.jour_semis = None

    def plantable(self, jour):
        """
        Peut on planter la plante pendant le jour cible

        Parameters
        ----------
        jour : int
            jour cible

        Returns
        -------
        bool
        """
        return self.plantage[jour]

    def recolte_masse(self, jour):
        """
        Quel quantité va ont recolter ce jour.

        Parameters
        ----------
        jour : int
            Jour de la récolte

        Returns
        -------
        float
            Masse de produit

        """
        if jour - self.jour_semis >= self.time_chunk:
            return self.masse_produite
        return 0

    def planter(self, emplacement, debut, fin):
        """
        Permet de planter l'objet dans l'emplacement désigné entre les deux
        semaines données.

        Parameters
        ----------
        emplacement : Emplacement
            Emplacement où l'on veux placer la plante.
        debut : int
            Numéro du jour de plantation.
        fin : int
            Numéro du jour de récolte.

        Raises
        ------
        ValueError
            Si on ne peut pas planter.

        Returns
        -------
        int
            0 si tentative de planter echou.

        """
        if self.plantable(debut) and emplacement.libre(debut, fin):
            for jour in emplacement.calendrier[debut:fin]:
                jour = self
            self.jour_semis = debut
            return 0
        raise ValueError

#%% type démo
class Patate(Plante):
    def __init__(self):
        self.plantage = [False] * 100 + [True] * 100 + [False] * (165)
        self.time_chunk = 30
        self.masse_produite = 5
        self.jour_semis = None

#%% Gene:

class Gene():
    decodeur_espece = {
        "00" : Jachere,
        "01" : Patate,
        "11" : Tomate,
        "10" : Poireaux
        }
    def __init__(self, len_x, len_y, ADN=""):
        self.len_x = len_x
        self.len_y = len_y
        if ADN:
            self.ADN = ADN
        else:
            self.ADN = "".join([str(rd.randint(0,1)) for i in
                                range(len_x * len_y * 365 * N_bit_espece)])
    
    def __str__(self):
        return self.ADN
            
#%% Herbier
# herbier = {}
# def ajout_espece(nom, plantage, time_chunk, masse_produite):
#     class New_espece(Plante):
#         def __init__(self):
#             self.plantage = plantage
#             self.time_chunk = time_chunk
#             self.masse_produite = masse_produite
#     New_espece.__qualname__ = nom
#     New_espece.__name__ = nom
#     herbier[nom] = New_espece
#     return 0

