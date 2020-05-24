# -*- coding: utf-8 -*-
"""
Created on Fri May  8 11:31:42 2020

@author: Leopold & Thomas
"""
import random as rd
import threading


import herbier
simulateur = herbier.simulateur
N_bit_espece = herbier.N_bit_espece

class Gene():
    """Class abstraite pour l'encapsulation des diférents types de gènes"""
    decodeur_espece = herbier.dict_herbier

    def __init__(self, *args):
        assert 0, "not implemented"

    def jardin(self) -> simulateur.Jardin:
        """renvoie le `simulateur.Jardin` corespondant au gène"""
        assert 0, "not implemented"
        
    @property
    def fitness(self) -> float:
        """ permet de ne calculer la production du gene que une seul fois"""
        if self._fit == None:
            _fit = self.jardin().rendement(True)
            self._fit = _fit
        return self.fit

    def __mul__(self, other):
        """enjambement de deux gène"""
        assert 0, "not implemented"

    def mutation(self):
        """fait muter le gène"""
        assert 0, "not implemented"

class Gene_naif(Gene):
    """Implementation de la representation naive, le gène est une chaine de caractère"""
    taux_mutation_carra = 0.05
    pourcentage_max_mutation = 0.3

    def __init__(self, len_x, len_y, ADN=""):
        def generateur_aleatoire_mais_pas_trop():
            decodeur_espece = Gene.decodeur_espece
            calendrier = [0]*365
            ADN = [0]*365
            iterateur = 0
            while iterateur < 365:
                identificateur = ""
                for i in range(N_bit_espece):
                    identificateur += str(rd.randint(0,1))
                plante_aléatoire = decodeur_espece[identificateur]
                if identificateur == N_bit_espece*"0":

                    ADN[iterateur] =  N_bit_espece*"0"
                    iterateur += 1
                else:
                    time_chunk = plante_aléatoire().time_chunk
                    if iterateur + time_chunk < 363:
                        calendrier[iterateur:iterateur + time_chunk] = [plante_aléatoire()]*time_chunk
                        ADN[iterateur:iterateur + time_chunk] = [identificateur]*time_chunk
                        calendrier[iterateur + time_chunk] = simulateur.Jachere()
                        ADN[iterateur + time_chunk] = N_bit_espece*"0"
                        iterateur += time_chunk + 1
                    else:
                        calendrier[iterateur:365] = [plante_aléatoire()]*(364-iterateur +1)
                        ADN[iterateur:365] = [identificateur]*(364-iterateur +1)
                        iterateur = 365
            return "".join(ADN)
        self.len_x = len_x
        self.len_y = len_y
        if ADN:
            self.ADN = ADN
        else:
            self.ADN = ""
            for x in range(len_x):
                for y in range(len_y):
                    self.ADN += generateur_aleatoire_mais_pas_trop()
                    #print(self.ADN)
        self._fit = None

    @classmethod
    def from_file(cls, adn, fit, len_x, len_y):
        """
        reconstruit le gene à partir des informations contenues dans le fichier de sauvegarde

        Parameters
        ----------
        cls : type
            DESCRIPTION.
        adn : str
            chaine binaire du gene
        fit : float or None
            fitness du gene
        len_x : int
            DESCRIPTION.
        len_y : int
            DESCRIPTION.

        Returns
        -------
        gene : Gene
            gene reconstruit

        """
        gene = cls(len_x, len_y, adn)
        gene.fit = fit
        return gene

    def __str__(self):
        return "{};{}".format(self.fit, hex(int(self.ADN, 2)))

    def __repr__(self):
        n = int(self.ADN, 2)
        return "gene : {}".format(hex(n))

    def jardin(self) -> simulateur.Jardin:
        jar = simulateur.Jardin(self.len_x, self.len_y)
        for x in range(self.len_x):
            for y in range(self.len_y):
                emplacement = jar.emplacement[y][x]
                ebauche = []
                for jour in range(365):
                    allele = self.ADN[(x + (y * self.len_x)) * 365 + N_bit_espece*jour :
                                      (x + (y * self.len_x)) * 365 + N_bit_espece*jour
                                      + N_bit_espece]
                    try:
                        ebauche += [Gene.decodeur_espece[allele]]
                    except KeyError:
                        ebauche += [simulateur.Jachere]
                idx_exploration = 0
                while idx_exploration < 365:
                    type_actuel = ebauche[idx_exploration]
                    if type_actuel == simulateur.Jachere:
                        idx_exploration += 1
                    else:
                        idx_depart = idx_exploration
                        while (idx_exploration < 365) and ebauche[idx_exploration] == type_actuel:
                            idx_exploration += 1
                        idx_fin = idx_exploration
                        plante = type_actuel()
                        try:
                            plante.planter(emplacement, idx_depart, idx_fin, jar) #,x,y,jar)
                        except ValueError:
                            pass
        return jar

    def __mul__(self, other):
        idx_coupe = rd.randint(0, len(self.ADN))
        return Gene_naif(self.len_x, self.len_y, self.ADN[:idx_coupe] + other.ADN[idx_coupe:])

    def mutation(self):
        if rd.random() < Gene_naif.taux_mutation_carra:
            nbr_caractere_a_muter = rd.randint(1, round(Gene_naif.pourcentage_max_mutation*len(self.ADN)))
            place_caractere = rd.randint(0, len(self.ADN)-nbr_caractere_a_muter-1)
            inverse = ""
            for bit in self.ADN[place_caractere:place_caractere+nbr_caractere_a_muter]:
                if bit == "0":
                    inverse += "1"
                else:
                    inverse += "0"
            if ((len(self.ADN[:place_caractere]
                    + inverse
                    + self.ADN[place_caractere
                               + nbr_caractere_a_muter:])) !=
                                                            len(self.ADN)):
                raise ValueError
            else:
                self.ADN = self.ADN[place_caractere] + inverse + self.ADN[place_caractere + nbr_caractere_a_muter:]

class Composant():
    """implementation des composants des genes composes"""
    next_id = 0

    taux_mutation_date = 0.3
    ecart_type_mutation_date = 10
    taux_mutation_position = 0.00
    taux_mutation_activite = 0.05

    def __init__(self, espece, date_plantaison, date_recolte, position, actif = True, idx = None):
        if idx == None:
            self.id = Composant.next_id
            Composant.next_id += 1
        else:
            self.id = idx

        self.position = position
        self.actif = actif
        self.espece = espece
        self.plantage = date_plantaison
        self.recolte = date_recolte

    def __repr__(self):
        return "{0}:{1}@{2},{3}->{4},{5}".format(self.id, self.espece, self.position,
                                        self.plantage, self.recolte, self.actif)
    def copy(self):
        """permet de creer une copie du composant avec le meme numero d'innovation"""
        x, y = self.position
        espece = self.espece
        date_plantaison = self. plantage
        date_recolte = self.recolte
        actif = self.actif
        id = self.id
        return Composant(espece, date_plantaison, date_recolte, (x,y), actif, id)

    @classmethod
    def random(cls, len_x, len_y):
        """permet de creer un nouvau composant aleatoire avec un nouveau numero d'innovation"""
        return cls(rd.choice(herbier.list_espece),
                   rd.randint(0, 364),
                   rd.randint(0, 364),
                   (rd.randint(0,len_x-1), rd.randint(0, len_y-1)))

    def __or__(self, other):
        return rd.choice([self, other])

    def mutation(self):
        """Mutation des carractéristique du composant"""
        if rd.random()<=Composant.taux_mutation_date:
            self.plantage += round(rd.gauss(0, Composant.ecart_type_mutation_date))
            self.plantage %= 365
        if rd.random()<=Composant.taux_mutation_date:
            self.recolte += round(rd.gauss(0, Composant.ecart_type_mutation_date))
            self.recolte %= 365
        if rd.random() <= Composant.taux_mutation_activite:
            self.actif = not self.actif

class Gene_compose(Gene):
    """implementation des genes composes"""
    taux_mutation_new_componant = 0.3

    def __init__(self, len_x, len_y, composants = 10):
        self.len_x = len_x
        self.len_y = len_y
        if isinstance(composants, int):
            self.composants = [Composant.random(len_x, len_y) for _ in range(composants)]
        else:
            self.composants = composants
        self._fit = None

    def __repr__(self):
        chaine = ""
        for elem in self.composants:
            chaine += "{}\n".format(elem.__repr__())
        return "gene compose ({0},{1}) :\n{2}".format(self.len_x, self.len_y, chaine)

    def mutation(self):
        for elem in self.composants:
            elem.mutation()

        if rd.random() <= Gene_compose.taux_mutation_new_componant:
            self.composants.append(Composant.random(self.len_x, self.len_y))

    def __mul__(self, other):
        parent_A = [None for _ in range(Composant.next_id)]
        parent_B = [None for _ in range(Composant.next_id)]
        for composant in self.composants:
            parent_A[composant.id] = composant
        for composant in other.composants:
            parent_B[composant.id] = composant
        fils = [None for _ in range(Composant.next_id)]
        for i in range(Composant.next_id):
            comp_a = parent_A[i]
            comp_b = parent_B[i]
            if (comp_a == None) and (comp_b == None):
                pass
            elif isinstance(comp_a, Composant) and isinstance(comp_b, Composant):
                fils[i] = (comp_a | comp_b).copy()
            elif isinstance(comp_a, Composant) and (comp_b == None):
                fils[i] = comp_a.copy()
            elif isinstance(comp_b, Composant) and (comp_a == None):
                fils[i] = comp_b.copy()
            else:
                raise ValueError
        gene = Gene_compose(self.len_x, self.len_y, [elem for elem in fils if elem != None])
        return gene

    def jardin(self):
        jar = simulateur.Jardin(self.len_x, self.len_y)
        for comp in self.composants:
            if comp.actif:
                try:
                    empl = jar.emplacement[comp.position[1]][comp.position[0]]
                    plante = comp.espece()
                    plante.planter(empl, comp.plantage, comp.recolte,jar)

                except ValueError:
                    pass
        return jar
    
    def recette(self):
        """permet de convertir le gene en un texte comprehensible pour l'utilisateur representant la plannification des cultures du jardin"""
        jar = simulateur.Jardin(self.len_x, self.len_y)
        liste_commande = []
        for comp in self.composants:
            if comp.actif:
                try:
                    empl = jar.emplacement[comp.position[1]][comp.position[0]]
                    plante = comp.espece()
                    plante.planter(empl, comp.plantage, comp.recolte, jar)
                    liste_commande.append("le jour {:0>3}, en ({},{}), planter des {}".format(comp.plantage, comp.position[1], comp.position[0], plante))
                    liste_commande.append("le jour {:0>3}, en ({},{}), recolter des {}".format(comp.recolte, comp.position[1], comp.position[0], plante))
                except ValueError:
                    pass
        liste_commande.sort()
        return "\n".join(liste_commande)


class Generation():
    """objet permettant de representer une generation dans l'algorithme"""
    multithreading_actif = False
    
    @classmethod
    def from_file(cls, path):
        """
        reconstruit la generation a partir d'un fichier

        Parameters
        ----------
        cls : type
            DESCRIPTION.
        path : str
            chemin du fichier contenant la sauvegarde

        Raises
        ------
        IOError
            DESCRIPTION.
        Exception
            DESCRIPTION.

        Returns
        -------
        generation : Generation
            generation corespondant au fichier

        """
        try:
            file = open(path+".txt", "r")
            lines = file.readlines()
            file.close()
        except Exception:
            raise IOError("""le fichier "{}" ne s'ouvre pas""".format(path+".txt"))
        try:
            en_tete = lines.pop(0)
            en_tete = en_tete.split(";")
            len_x = int(en_tete[0])
            len_y = int(en_tete[1])
            evaluee = bool(int(en_tete[2]))
        except Exception:
            raise Exception("""Entete invalide""")
        try:
            genes = []
            for n, ligne in enumerate(lines):
                ligne = ligne.split(';')
                fit = ligne[0]
                adn = ligne[1][:-1]
                adn = bin(int(adn, 16))[2:]
                if evaluee:
                    fit = float(fit)
                else:
                    fit = None
                genes.append(Gene_naif.from_file(adn, fit, len_x, len_y))
        except Exception:
            Exception("""Contenu invalide ligne {}""".format(n))

        generation = cls(genes)
        generation.evaluee = evaluee
        return generation

    def __init__(self, genes):
        self.genes = []
        for elem in genes:
            if not isinstance(elem, Gene):
                raise TypeError("Ce n'est pas un gene")
            self.genes.append(elem)
        self.evaluee = False

    def generation_suivante(self):
        """
        calcule la génération suivante

        Returns
        -------
        Generation
            La generation suivante

        """
        N = len(self.genes)
        self.evaluation()
        gene = self._selection()

        new_gene = []
        while len(new_gene) <= N:
            g1 = rd.choice(gene)
            g2 = rd.choice(gene)
            g = (g1 * g2)
            g.mutation()
            new_gene.append(g)
        gen_suivante = Generation(new_gene)
        return gen_suivante

    def evaluation(self):
        """
        Permet de trier la liste des genes dans l'odre décroissant de qualité

        Returns
        -------
        None.

        """
        if Generation.multithreading_actif :
            liste_evaluateur = []
            for gene in self.genes:
                liste_evaluateur.append(Evaluateur(gene))
            
            for evaluateur in liste_evaluateur:
                evaluateur.start()
            
            for evaluateur in liste_evaluateur:
                evaluateur.join()
            
        self.genes.sort(key=Gene.fitness, reverse=True)
        self.evaluee = True

    def _selection(self) -> list:
        """
        Permet de selectionner les 10% meilleurs élements de la liste de genes, Cette dernière doit être triée du meilleur [0] au moins bon [-1].

        Returns
        -------
        None.

        """

        if self.evaluee == False:
            self.evaluation()
        selection = []
        selection += self.genes[:(len(self.genes)//10)]
        weight = [gene.fitness for gene in self.genes[(len(self.genes)//10):]]
        selection += rd.choices(self.genes[(len(self.genes)//10):], weight, k = len(selection))
        return selection

    def __str__(self):
        chaine = "{1};{2};{0}\n".format(int(self.evaluee), self.genes[0].len_x,  self.genes[0].len_y)
        for gene in self.genes:
            chaine += str(gene)+"\n"
        return chaine

    def save(self, nom, emplacement = "save"):
        """
        enregistre la géneration dans un fichier

        Parameters
        ----------
        nom : str
            nom de la sauvegarde
        emplacement : str, optional
            emplacement de la sauvegarde. The default is "save".

        Returns
        -------
        None.

        """
        file = open(emplacement + "/" + nom + '.txt', 'w')
        file.write(str(self))
        file.close()

    def get_fitness(self):
        """
        renvoit la liste des fitness de la generation

        Returns
        -------
        fitness : list[int]
            liste des fitness de la generation

        """
        if not self.evaluee:
            self.evaluation()
        fitness = []
        for gene in self.genes:
            fitness.append(gene.fit)
        return fitness


class Essai():
    """objet representant un simulation en entier"""
    def __init__(self, generation_initial):

        self.generations = []
        self.generations.append(generation_initial)

    @classmethod
    def naif_non_random(cls, len_x, len_y, taille):
        """permet d'initialiser une nouvelle simulation avec des `genetique.Gene_naif`, les genes ne sont pas entierement aleatoires"""
        genes = [Gene_naif(len_x, len_y) for _ in range(taille)]
        generation = Generation(genes)
        return cls(generation)

    @classmethod
    def composee_vide(cls, len_x, len_y, taille):
        """permet d'initialiser une nouvelle simulation avec des `genetique.Gene_compose`, les genes ne sont pas entierement aleatoires"""
        genes = [Gene_compose(len_x, len_y, 0) for _ in range(taille)]
        generation = Generation(genes)
        return cls(generation)

    def generation_suivante(self):
        """
        Rajoute la géneration suivante dans la liste des génerations

        Returns
        -------
        None.

        """
        self.generations.append(self.generations[-1].generation_suivante())

    def save(self, nom, emplacement = "save"):
        """
        sauvegarde l'essai dans l'emplacement voulu, avec le nom voulu. ne fonctionne que pour les gene_naif

        Parameters
        ----------
        nom : str
            nom de la save, "foo" pour obtenir "foo_0.txt"..."foo_n.txt"
        emplacement : str, optional
            emplacement des sauvegardes. The default is "save".

        Returns
        -------
        None.

        """
        for n, generation in enumerate(self.generations):
            generation.save("{0}_{1}".format(nom, n), emplacement)

    @classmethod
    def load_save(cls, nom, emplacement = "save"):
        """charge une sauvegarde d'essai, ne fonctionne que pour les genes naifs."""
        essai = cls(0, 0, 0, True)
        idx = 0
        essai.generations.append(Generation.from_file(
            "{}/{}_0".format(emplacement, nom)))
        while True:
            idx +=1
            try:
                essai.generations.append(Generation.from_file(
                    "{}/{}_{}".format(emplacement, nom, idx)))
            except Exception:
                break
        return essai

    def evolution_statistique(self, plt, n_mesure=10):
        """permet de tracer une evolution de la repartition de la fitness au cours du temps, utile pour voir l'evolution des genes."""
        import numpy as np
        liste_indice = np.linspace(0, len(self.generations)-1, n_mesure, dtype=int)
        distribution = []
        for n, generation in enumerate(self.generations):
            if n in liste_indice:
                distribution.append(generation.get_fitness())
        plt.violinplot(distribution, liste_indice,
                       widths = len(self.generations)/(2*n_mesure),
                       showmeans = True)
        plt.title("Evolution de la repartition statistique du\nrendement en fonction des generations")
        plt.xlabel("generation")
        plt.ylabel("rendement $kg/m^2$")
        return plt

class Evaluateur(threading.Thread):
    """classe permetant le calcul en parallele du rendement des genes, permet un gain de temps notable """
    def __init__(self, gene):
        threading.Thread.__init__(self)
        self.gene = gene
    
    def run(self):
        """declanche le calcule du rendement du jardin represente par le gene"""
        A = self.gene.fitness



