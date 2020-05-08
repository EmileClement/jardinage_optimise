# -*- coding: utf-8 -*-
"""
Created on Fri May  8 11:32:38 2020

@author: Leopold
"""
from simulateur import *
from herbier import *
from genetique import *

def demo(nom):
    E = Essai(2, 3, 200)
    try:
        for i in range(15):
            E.generation_suivante()
    except KeyboardInterrupt:
        pass
    E.save(nom)
    E.evolution_statistique()
    generation = E.generations[-1]
    generation.evaluation()
    return generation.genes[0]        


