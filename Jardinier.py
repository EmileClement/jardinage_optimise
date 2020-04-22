# -*- coding: utf-8 -*-
"""
Created on Mon Apr 20 11:51:41 2020

@author: Leopold
"""
class Climat():
    pass

class Jardin():
    def __init__(self, len_x: int, len_y: int):
        self.emplacement = [[Emplacement(self) for i in range(len_x)] for i in range(len_y)]
        
class Emplacement():
    def __init__(self, jardin):
        self.jardin = jardin
        

class Plante():
    pass


    