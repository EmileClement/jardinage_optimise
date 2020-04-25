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

    def rendement(self, biais=False) -> float:
        """
        Renvoie le rendement du jardin, permet l'évaluation de la qualité de l'arrangement

        Parameters
        ----------
        biais : bool, optional
            Mettre True pour prendre en compte la biomasse. The default is False.

        Returns
        -------
        float
            Masse produite par le jardin. La biomasse permet de prendre en compte les plantes qui ne sont pas arrivées a maturité

        """
        masse = 0
        for ligne in self.emplacement:
            for case in ligne:
                masse += case.rendement(biais)
        return masse

class Emplacement():
    def __init__(self, jardin):
        self.jardin = jardin
        self.calendrier = [Jachere() for i in range(365)]

    def __repr__(self):
        return "Emplacement: " + "\n ".join([str(i) + ": " + elem.__repr__()
                                             for i, elem in
                                             enumerate(self.calendrier)]) + ";"

    def libre(self, debut, fin) -> bool:
        """
        Peut-on placer une plante sur cette plage de temps

        Parameters
        ----------
        debut : int
            Jour de la plantation.
        fin : int
            Jour de la récolte.

        Returns
        -------
        bool
            Ce laps de temps est il-libre.

        """
        libre = True
        for elem in self.calendrier[debut:fin]:
            libre &= isinstance(elem, Jachere)
        return libre

    def rendement(self, biais=False) -> float:
        """
        Renvoie la masse produite par cet emplacement

        Parameters
        ----------
        biais : bool, optional
            Mettre True pour prendre en compte la biomasse. The default is False.

        Returns
        -------
        float
            Masse produite, la biomasse permet de prendre en compte les plantes qui ne sont pas arrivées à maturité.

        """
        plantes = set()
        for jour in self.calendrier:
            if isinstance(jour, Plante):
                plantes.add(jour)
        masse = 0
        for elem in plantes:
            masse += elem.recolte_masse(elem.jour_recolte, biais)
        return masse

class Occupant():
    def __init__(self):
        assert 0, "Not implemeted"

class Jachere(Occupant):
    def __init__(self):
        self.time_chunk = 0

    def __repr__(self):
        return "Jachère"

class Plante(Occupant):
    def __init__(self):
        self.plantage = [False]*365
        self.time_chunk = 0
        self.masse_produite = 0
        self.jour_semis = None
        self.jour_recolte = None
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
        try:
            return self.plantage[jour]
        except IndexError:
            return False
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
        try:
            return self.plantage[jour]
        except IndexError:
            return False

    def recolte_masse(self, jour, biais=False) -> float:
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
        if (jour - self.jour_semis >= self.time_chunk) and (self.deja_recolte == False):
            self.deja_recolte = True
            return self.masse_produite

        return biais * (self.jour_semis-self.jour_recolte)** 2 / 365 ** 2

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
            0 si la tentative de planter echoue.

        """
        if self.plantable(debut) and emplacement.libre(debut, fin):
            for i in range(debut, fin):
                emplacement.calendrier[i] = self
            self.jour_semis = debut
            self.jour_recolte = fin
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
        self.plantage = [True] * 360 #[True] * 90 + [False] * 153 + [False] * (122)
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
        "10" : Poireau
        }
    def __init__(self, len_x, len_y, ADN=""):
        self.len_x = len_x
        self.len_y = len_y
        if ADN:
            self.ADN = ADN
        else:
            self.ADN = ""
            for x in range(len_x):
                for y in range(len_y):
                    self.ADN = self.ADN + generateur_aleatoire_mais_pas_trop()
                    print(self.ADN)

                    

    def __str__(self):
        return self.ADN

    def __repr__(self):
        n = int(self.ADN, 2)
        return "gene : {}".format(hex(n))

    def jardin(self) -> Jardin:
        """
        Créer le jardin corespondant à ce géne
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
                    allele = self.ADN[(x + (y * self.len_x)) * 365 + jour :
                                      (x + (y * self.len_x)) * 365 + jour
                                      + N_bit_espece]
                    ebauche += [Gene.decodeur_espece[allele]]
                idx_exploration = 0
                while idx_exploration < 365:
                    type_actuel = ebauche[idx_exploration]
                    if type_actuel == Jachere:
                        idx_exploration += 1
                    else:
                        idx_depart = idx_exploration
                        while (idx_exploration < 365) and ebauche[idx_exploration] == type_actuel:
                            idx_exploration += 1
                        idx_fin = idx_exploration
                        plante = type_actuel()
                        try:
                            plante.planter(emplacement, idx_depart, idx_fin)
                        except ValueError:
                            pass
        return jar
    
def generateur_aleatoire_mais_pas_trop():
    decodeur_espece = {
    "00" : Jachere,
    "01" : Patate,
    "11" : Tomate,
    "10" : Poireau
    }
    calendrier = [0]*365
    ADN = [0]*365
    iterateur = 0
    
    while iterateur <365:
        identificateur = str(rd.randint(0,1)) + str(rd.randint(0,1))
        plante_aléatoire = decodeur_espece[str(rd.randint(0,1)) + str(rd.randint(0,1))]

        
        if identificateur == "00":
            ADN[iterateur] = "00"
            iterateur += 1
        else:
            time_chunk = plante_aléatoire().time_chunk
            if iterateur + time_chunk < 363:
                calendrier[iterateur:iterateur + time_chunk] = [plante_aléatoire()]*time_chunk
                ADN[iterateur:iterateur + time_chunk] = [identificateur]*time_chunk
                calendrier[iterateur + time_chunk] = Jachere()
                ADN[iterateur + time_chunk] = "00"
                iterateur += time_chunk + 1
                
            else:
                calendrier[iterateur:365] = [plante_aléatoire()]*(364-iterateur +1)
                ADN[iterateur:365] = [identificateur]*(364-iterateur +1)
                iterateur = 365
    
    return "".join(ADN)



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
