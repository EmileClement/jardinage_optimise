# -*- coding: utf-8 -*-
"""
Created on Fri May  8 11:27:10 2020

@author: Leopold & Thomas
"""
from simulateur import *

class Patate(Plante):
    """Classe representant les pommes de Terres"""
    def __init__(self):
        self.plantage = [False] * 52 + [True] * 109 + [False] * 204
        self.time_chunk = 80
        self.jour_semis = None
        self.deja_recolte = False
        self.color = "#b28310"
        self.id = 1
        self.multiplicateur = 1.

    def __repr__(self):
        return "Patate"
    def __str__(self):
        return "Patate"
    def masse_produite(self,jour):
        """
        Renvoie la masse produite par le légume à un jour donné de l'année

        Parameters
        ----------
        jour : int

        Returns
        -------
        float
            Masse produite par le légume

        """

        return 5*(1/(1 + 10**((- ((jour - self.jour_semis)%365 - self.time_chunk))/20)) - 1/(1 + 10**((100- ((jour - self.jour_semis)%365 - self.time_chunk))/15)))


class Tomate(Plante):
    """Classe representant les Tomates"""
    def __init__(self):
        self.plantage = [False] * 92 + [True] * 90 + [False] * (183)
        self.time_chunk = 80
        self.jour_semis = None
        self.deja_recolte = False
        self.color = "#eb4b3d"
        self.id = 2
        self.multiplicateur = 1.

    def __repr__(self):
        return "Tomate"
    def __str__(self):
        return "Tomate"
    def masse_produite(self,jour):
        """
        Renvoie la masse produite par le légume à un jour donné de l'année

        Parameters
        ----------
        jour : int

        Returns
        -------
        float
            Masse produite par le légume

        """
        return 10*(1/(1 + 9**(( -((jour - self.jour_semis)%365 - self.time_chunk))/20)) - 1/(1 + 9**((100- ((jour - self.jour_semis)%365 - self.time_chunk))/20)))
        


class Poireau(Plante):
    """Classe representant les Poireau"""
    def __init__(self):
        self.plantage = [False] *245  + [True] * 90 + [False] * (30)
        self.time_chunk = 20
        self.jour_semis = None
        self.deja_recolte = False
        self.color = "#80c44a"
        self.id = 3
        self.multiplicateur = 1.
    def __repr__(self):
        return "Poireau"
    def __str__(self):
        return "Poireau"
    def masse_produite(self,jour):
        """
        Renvoie la masse produite par le légume à un jour donné de l'année

        Parameters
        ----------
        jour : int

        Returns
        -------
        float
            Masse produite par le légume

        """

        return 4*(1/(1 + 10**((10- ((jour - self.jour_semis)%365 - self.time_chunk))/10)) -1/(1 + 10**((150 -((jour - self.jour_semis)%365 - self.time_chunk))/20)))


class Epinards(Plante):
    """Classe representant les Epinards"""
    def __init__(self):
        self.plantage = [True] * 80 + [False] *147  + [True] * (138)
        self.time_chunk = 30

        self.jour_semis = None
        self.deja_recolte = False
        self.color = "#26661d"
        self.id = 4
        self.multiplicateur = 1.
    def __repr__(self):
        return "Epinards"
    def __str__(self):
        return "Epinards"

    def masse_produite(self,jour):
        """
        Renvoie la masse produite par le légume à un jour donné de l'année

        Parameters
        ----------
        jour : int

        Returns
        -------
        float
            Masse produite par le légume

        """

        return 1.5/(1 + 10**((-((jour - self.jour_semis)%365) + self.time_chunk)/15))

    

class Radis(Plante):
    """Classe representant les Radis"""
    def __init__(self):
        self.plantage = [False] * 50 + [True] * 91 + [False] * (224)
        self.time_chunk = 20
        self.jour_semis = None
        self.deja_recolte = False
        self.color = "#f07f77"
        self.id = 5
        self.multiplicateur = 1.
    def __repr__(self):
        return "Radis"
    def __str__(self):
        return "Radis"
    def masse_produite(self,jour):
        """
        Renvoie la masse produite par le légume à un jour donné de l'année

        Parameters
        ----------
        jour : int

        Returns
        -------
        float
            Masse produite par le légume

        """

        return 2.1*(1/(1 + 10**((-((jour - self.jour_semis)%365) + self.time_chunk)/10)) - 1/(1 + 10**((130-((jour - self.jour_semis)%365) + self.time_chunk)/30)))


class Choux(Plante):
    """Classe representant les Choux"""
    def __init__(self):
        self.plantage = [False] * 60 + [True] * 60 + [False] * (245)
        self.time_chunk = 90
        self.jour_semis = None
        self.deja_recolte = False
        self.color = "#7e9e71"
        self.id = 6
        self.multiplicateur = 1.
    def __repr__(self):
        return "Choux"
    def __str__(self):
        return "Choux"
    def masse_produite(self,jour):
        """
        Renvoie la masse produite par le légume à un jour donné de l'année

        Parameters
        ----------
        jour : int

        Returns
        -------
        float
            Masse produite par le légume

        """

        return 1.2/(1 + 10**((-((jour - self.jour_semis)%365) + self.time_chunk)/30))


class Navets(Plante):
    """Classe representant les Navets"""
    def __init__(self):
        self.plantage = [False] * 182 + [True] * 90 + [False] * (93)
        self.time_chunk = 30
        self.jour_semis = None
        self.deja_recolte = False
        self.color = "#c8d4a9"
        self.id = 7
        self.multiplicateur = 1.
    def __repr__(self):
        return "Navets"
    def __str__(self):
        return "Navets"
    def masse_produite(self,jour):
        """
        Renvoie la masse produite par le légume à un jour donné de l'année

        Parameters
        ----------
        jour : int

        Returns
        -------
        float
            Masse produite par le légume

        """

        return 2.*(1/(1 + 10**((-((jour - self.jour_semis)%365) + self.time_chunk)/25)) -1/(1 + 10**((100-((jour - self.jour_semis)%365) + self.time_chunk)/15)))


N_bit_espece = 3

list_espece = [Patate, Tomate, Poireau, Epinards, Radis, Choux, Navets]
dict_herbier = {
        "000" : Jachere,
        "001" : Patate,
        "011" : Tomate,
        "010" : Poireau,
        "100" : Epinards,
        "101" : Radis,
        "110" : Choux,
        "111" : Navets
        }

def graphe_production(plante,jour_semis):
    """ Permet de tracer la production des esepces en fonctions du temps suivant leur jour de plantation. Attention: ne prend pas en compte la saisonnalité des plantes"""
    import matplotlib.pyplot as plt
    levert = plante()
    levert.jour_semis = jour_semis
    prod = []
    for i in range(365):
        prod.append(levert.masse_produite(i))
    plt.plot(range(365),prod)
