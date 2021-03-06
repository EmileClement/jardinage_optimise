# -*- coding: utf-8 -*-
"""
Created on Fri May  8 11:32:38 2020

@author: Leopold
"""

import genetique
herbier = genetique.herbier
simulateur = herbier.simulateur
Essai = genetique.Essai

def demo_naif(n_gen=30, n_pop=200):
    """pour faire un essaie simple avec les `genetique.Gene_naif`"""
    from matplotlib import pyplot as plt
    E = Essai.naif_non_random(2, 3, n_pop)
    try:
        for i in range(n_gen):
            print("generation {}".format(i))
            E.generation_suivante()
    except KeyboardInterrupt:
        pass
    E.evolution_statistique(plt, 5)
    generation = E.generations[-1]
    generation.evaluation()
    return generation.genes[0]

def demo_composee(n_gen=30, n_pop=200):
    """pour faire un essaie simple avec les `genetique.Gene_compose`"""
    from matplotlib import pyplot as plt
    E = Essai.composee_vide(2, 3, n_pop)
    try:
        for i in range(n_gen):
            print("generation {}".format(i))
            E.generation_suivante()
    except KeyboardInterrupt:
        pass
    E.evolution_statistique(plt, 5)
    generation = E.generations[-1]
    generation.evaluation()
    return generation.genes[0]

def comparateur_identique(n_concurents, n_gen=30, n_pop=200):
    """permet de comparer deux essais avec la representation composee, pour mettre en evidence la partie aleatoire"""
    concurents = [Essai.composee_vide(2, 3, n_pop) for _ in range(n_concurents)]
    try:
        for i in range(n_gen):
            print("generation {}".format(i))
            for elem in concurents:
                elem.generation_suivante()
    except KeyboardInterrupt:
        pass
    from matplotlib import pyplot as plt
    for elem in concurents:
        elem.evolution_statistique(plt, 5)
    return concurents

def comparateur_representation(n_gen=30, n_pop=200):
    """permet de comparer deux essais avec les deux representation"""
    concurents = [Essai.naif_non_random(2, 3, n_pop), Essai.composee_vide(2, 3, n_pop)]
    try:
        for i in range(n_gen):
            print("generation {}".format(i))
            for elem in concurents:
                elem.generation_suivante()
    except KeyboardInterrupt:
        pass
    from matplotlib import pyplot as plt
    concurents[0].evolution_statistique(plt, 5)
    concurents[1].evolution_statistique(plt, 5)
    return concurents

def comparateur_taille(n_gen=30, n_pop=200):
    """permet de comparer deux essais avec la representation composee mais avec deu"""
    concurents = [Essai.composee_vide(2, 3, n_pop)]
    concurents += [Essai.composee_vide(2,3, 2*n_pop)]
    try:
        for i in range(n_gen):
            print("generation {}".format(i))
            for elem in concurents:
                elem.generation_suivante()
    except KeyboardInterrupt:
        pass
    from matplotlib import pyplot as plt
    for elem in concurents:
        elem.evolution_statistique(plt, 5)
    return concurents
