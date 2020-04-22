# -*- coding: utf-8 -*-
"""
Created on Mon Apr 20 11:51:41 2020

@author: Leopold
"""
#%% Def des classes
class Jardin():
    def __init__(self, len_x: int, len_y: int):
        self.emplacement = [[Emplacement(self) for i in range(len_x)] for i in range(len_y)]

    def __repr__(self):
        return "Jardin({},{})".format(len(self.emplacement[0]), len(self.emplacement))


class Emplacement():
    def __init__(self, jardin):
        self.jardin = jardin
        self.calendrier = [Jachere() for i in range(52)]

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
        self.plantage = [False]*52
        self.time_chunk = 0
        self.masse_produite = 0
        self.semaine_semis = None

    def plantable(self, semaine):
        """
        Peut on planter la plante pendant la semaine cible

        Parameters
        ----------
        semaine : int
            Semaine cible

        Returns
        -------
        bool
        """
        return self.plantage[semaine]

    def recolte_masse(self, semaine):
        """
        Quel quantité va ont recolter cet semaine

        Parameters
        ----------
        semaine : int
            Semaine de la récolte

        Returns
        -------
        float


        """
        if semaine - self.semaine_semis >= self.time_chunk:
            return self.masse_produite
        return 0

    def planter(self, emplacement, debut, fin):
        if self.plantable(debut) and emplacement.libre(debut, fin):
            for semmaine in emplacement.calendrier[debut:fin]:
                semmaine = self
            self.semaine_semis = debut
            return 0
        raise ValueError


#%% Herbier
herbier = {}
def ajout_espece(nom, plantage, time_chunk, masse_produite):
    class New_espece(Plante):
        def __init__(self):
            self.plantage = plantage
            self.time_chunk = time_chunk
            self.masse_produite = masse_produite
    New_espece.__qualname__ = nom
    New_espece.__name__ = nom
    herbier[nom] = New_espece
    return 0
