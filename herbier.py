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
        self.masse_produite = 1.
        self.jour_semis = None
        self.deja_recolte = False
        self.color = "#b28310"

    def __repr__(self):
        return "Patate"
    def __str__(self):
        return "Patate"

class Tomate(Plante):
    def __init__(self):
        self.plantage = [False] * 121 + [True] * 60 + [False] * (365 - 171)
        self.time_chunk = 134
        self.masse_produite = 2.5
        self.jour_semis = None
        self.deja_recolte = False
        self.color = "#eb4b3d"

    def __repr__(self):
        return "Tomate"
    def __str__(self):
        return "Tomate"


class Poireau(Plante):
    def __init__(self):
        self.plantage = [True] * 360 #[True] * 90 + [False] * 153 + [False] * (122)
        self.time_chunk = 30
        self.masse_produite = 0.150
        self.jour_semis = None
        self.deja_recolte = False
        self.color = "#80c44a"
    def __repr__(self):
        return "Poireau"
    def __str__(self):
        return "Poireau"

N_bit_espece = 3

list_espece = [Patate, Tomate, Poireau]
dict_herbier = {
        "000" : Jachere,
        "001" : Patate,
        "011" : Tomate,
        "010" : Poireau
        }
