# -*- coding: utf-8 -*-
"""
Created on Fri May  8 11:27:10 2020

@author: Leopold
"""
from simulateur import *

class Patate(Plante):
    def __init__(self):
        self.plantage = [False] * 52 + [True] * 253 + [False] * (365 - 305)
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
        if (self.deja_recolte == False):
            self.deja_recolte = True
            return 10/(1 + 10**((- (jour - self.jour_semis - self.time_chunk))/20))
        else:
            return 0.

class Tomate(Plante):
    def __init__(self):
        self.plantage = [False] * 121 + [True] * 60 + [False] * (365 - 171)
        self.time_chunk = 119
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
        if (self.deja_recolte == False):
            self.deja_recolte = True
            return 10/(1 + 9**((15- (jour - self.jour_semis - self.time_chunk))/10))
        else:
            return 0.


class Poireau(Plante):
    def __init__(self):
        self.plantage = [True] * 90 + [False] * 153 + [True] * (122)
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
        if (self.deja_recolte == False):
            self.deja_recolte = True
            return 4/(1 + 10**((10- (jour - self.jour_semis - self.time_chunk))/5))
        else:
            return 0.

class Epinards(Plante):
    def __init__(self):
        self.plantage = [True] * 80 + [False] *147  + [True] * (138)
        self.time_chunk = 30

        self.jour_semis = None
        self.deja_recolte = False
        self.color = "#80c44a"
        self.id = 4
        self.multiplicateur = 1.
    def __repr__(self):
        return "Epinards"
    def __str__(self):
        return "Epinards"

    def masse_produite(self,jour):
        if (self.deja_recolte == False):
            self.deja_recolte = True
            return 1.5/(1 + 10**((self.jour_semis-jour + self.time_chunk)/5))
        else:
            return 0.
    

class Radis(Plante):
    def __init__(self):
        self.plantage = [False] * 50 + [True] * 91 + [False] * (224)
        self.time_chunk = 20
        self.jour_semis = None
        self.deja_recolte = False
        self.color = "#80c44a"
        self.id = 3
        self.multiplicateur = 1.
    def __repr__(self):
        return "Radis"
    def __str__(self):
        return "Radis"
    def masse_produite(self,jour):
        if (self.deja_recolte == False):
            self.deja_recolte = True
            return 2.1/(1 + 10**((self.jour_semis-jour + self.time_chunk)/5))
        else:
            return 0.

class Choux(Plante):
    def __init__(self):
        self.plantage = [False] * 60 + [True] * 60 + [False] * (245)
        self.time_chunk = 90
        self.jour_semis = None
        self.deja_recolte = False
        self.color = "#80c44a"
        self.id = 3
        self.multiplicateur = 1.
    def __repr__(self):
        return "Choux"
    def __str__(self):
        return "Choux"
    def masse_produite(self,jour):
        if (self.deja_recolte == False):
            self.deja_recolte = True
            return 1.2/(1 + 10**((self.jour_semis-jour + self.time_chunk)/30))
        else:
            return 0.

class Navets(Plante):
    def __init__(self):
        self.plantage = [False] * 182 + [True] * 90 + [False] * (93)
        self.time_chunk = 75
        self.jour_semis = None
        self.deja_recolte = False
        self.color = "#80c44a"
        self.id = 3
        self.multiplicateur = 1.
    def __repr__(self):
        return "Navets"
    def __str__(self):
        return "Navets"
    def masse_produite(self,jour):
        if (self.deja_recolte == False):
            self.deja_recolte = True
            return 2./(1 + 10**((self.jour_semis-jour + self.time_chunk)/15))
        else:
            return 0.

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

table_associations = [[1.1,1,1,1,1,1,1,1],
                      [1,1.1,1,1,1,1,1,1],
                      [1,1,1.1,1,1,1,1,1],
                      [1,1,1,1.1,1,1,1,1],
                      [1,1,1,1,1.1,1,1,1],
                      [1,1,1,1,1,1.1,1,1],
                      [1,1,1,1,1,1,1.1,1],
                      [1,1,1,1,1,1,1,1.1]]
