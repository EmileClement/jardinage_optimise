# -*- coding: utf-8 -*-
"""
Created on Fri May  8 11:27:10 2020

@author: Leopold
"""
from simulateur import *

class Patate(Plante):
    def __init__(self):
        self.plantage = [False] * 52 + [True] * 253 + [False] * (365 - 305)
        self.time_chunk = 100
        self.masse_produite = 2.
        self.jour_semis = None
        self.deja_recolte = False
        self.color = "#b28310"
        self.id = 1

    def __repr__(self):
        return "Patate"
    def __str__(self):
        return "Patate"

class Tomate(Plante):
    def __init__(self):
        self.plantage = [False] * 121 + [True] * 60 + [False] * (365 - 171)
        self.time_chunk = 134
        self.masse_produite = 10.
        self.jour_semis = None
        self.deja_recolte = False
        self.color = "#eb4b3d"
        self.id = 2

    def __repr__(self):
        return "Tomate"
    def __str__(self):
        return "Tomate"


class Poireau(Plante):
    def __init__(self):
        self.plantage = [True] * 90 + [False] * 153 + [True] * (122)
        self.time_chunk = 30
        self.masse_produite = 4.
        self.jour_semis = None
        self.deja_recolte = False
        self.color = "#80c44a"
        self.id = 3
    def __repr__(self):
        return "Poireau"
    def __str__(self):
        return "Poireau"

class Epinards(Plante):
    def __init__(self):
        self.plantage = [True] * 80 + [False] *147  + [True] * (138)
        self.time_chunk = 60
        self.masse_produite = 1.5
        self.jour_semis = None
        self.deja_recolte = False
        self.color = "#80c44a"
        self.id = 4
    def __repr__(self):
        return "Epinards"
    def __str__(self):
        return "Epinards"
    
class Radis(Plante):
    def __init__(self):
        self.plantage = [False] * 50 + [True] * 91 + [False] * (224)
        self.time_chunk = 30
        self.masse_produite = 2.1
        self.jour_semis = None
        self.deja_recolte = False
        self.color = "#80c44a"
        self.id = 3
    def __repr__(self):
        return "Radis"
    def __str__(self):
        return "Radis"

class Choux(Plante):
    def __init__(self):
        self.plantage = [False] * 60 + [True] * 60 + [False] * (245)
        self.time_chunk = 120
        self.masse_produite = 1.2
        self.jour_semis = None
        self.deja_recolte = False
        self.color = "#80c44a"
        self.id = 3
    def __repr__(self):
        return "Choux"
    def __str__(self):
        return "Choux"

class Navets(Plante):
    def __init__(self):
        self.plantage = [False] * 182 + [True] * 90 + [False] * (93)
        self.time_chunk = 90
        self.masse_produite = 2.
        self.jour_semis = None
        self.deja_recolte = False
        self.color = "#80c44a"
        self.id = 3
    def __repr__(self):
        return "Navets"
    def __str__(self):
        return "Navets"

N_bit_espece = 3

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
