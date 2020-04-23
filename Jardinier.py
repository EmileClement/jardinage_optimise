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
        return "Emplacement: " + "\n ".join([str(i) + ": " + elem.__repr__()
                                            for i, elem in
                                            enumerate(self.calendrier)]) + ";"

    def libre(self, debut, fin) -> bool:
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
        self.deja_recolte = False

    def plantable(self, jour) -> bool:
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

    def recolte_masse(self, jour) -> float:
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
        if (jour - self.jour_semis >= self.time_chunk) and (self.deja_recolte == False ):
            self.deja_recolte = True
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
            for i in range(debut, fin):
                emplacement.calendrier[i] = self
            self.jour_semis = debut
            return 0
        raise ValueError

#%% type démo
class Patate(Plante):
    def __init__(self):
        self.plantage = [False] * 52 + [True] * 253 + [False] * (365 - 305)
        self.time_chunk = 100
        self.masse_produite = 1.
        self.jour_semis = None
        self.deja_recolte = False

class Tomate(Plante):
    def __init__(self):
        self.plantage = [False] * 121 + [True] * 60 + [False] * (365 - 171)
        self.time_chunk = 134
        self.masse_produite = 2.5
        self.jour_semis = None
        self.deja_recolte = False

class Poireau(Plante):
    def __init__(self):
        self.plantage = [True] * 90 + [False] * 153 + [False] * (122)
        self.time_chunk = 30
        self.masse_produite = 0.150
        self.jour_semis = None
        self.deja_recolte = False

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
    
    def jardin(self) -> Jardin:
        """
        Créer le jardin corespondant a ce géne

        Returns
        -------
        Jardin
            Jardin correspondant.

        """
        jar = Jardin(self.len_x, self.len_y)
        for x in range(self.len_x):
            for y in range(self.len_y):
                emplacement = jar.emplacement[y][x]
                ebauche = [] 
                for jour in range(365):
                    allele = self.ADN[(x * y) * 365 + jour :
                                  (x * y) * 365 + jour + N_bit_espece]
                    ebauche += [Gene.decodeur_espece[allele]]
                plantes_a_planter = []
                idx_exploration = 0
                while idx_exploration < 365:
                    type_actuel = ebauche[idx_exploration]
                    if type_actuel == Jachere:
                        idx_exploration +=1
                    else:
                        idx_depart = idx_exploration
                        while (idx_exploration < 365) and ebauche[idx_exploration] == type_actuel:
                            idx_exploration += 1
                        idx_fin = idx_exploration
                        plante = type_actuel()
                        try:
                            plante.planter(emplacement, idx_depart, idx_fin)
                        except ValueError:
                            print("Erreur de plantation")
                 
        return jar, ebauche
            
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

