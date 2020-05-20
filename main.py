# -*- coding: utf-8 -*-
"""
Created on Fri May  8 11:32:38 2020

@author: Leopold
"""
from simulateur import *
from herbier import *
from genetique import *

def demo(nom, n_gen=15, n_pop=200):
    E = Essai.composee_vide(2, 3, n_pop)
    try:
        for i in range(n_gen):
            print("generation {}".format(i))
            E.generation_suivante()
    except KeyboardInterrupt:
        pass
    E.save(nom)
    E.evolution_statistique(5)
    generation = E.generations[-1]
    generation.evaluation()
    return generation.genes[0]

E = demo('profiler', 50, 150)
