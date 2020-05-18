# -*- coding: utf-8 -*-
"""
Created on Fri May  8 11:31:42 2020

@author: Leopold
"""
import random as rd

from simulateur import *
from herbier import *

class Gene():
    decodeur_espece = dict_herbier
    
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
                        calendrier[iterateur + time_chunk] = Jachere()
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
        self.fit = None
    
    @classmethod
    def from_file(cls, adn, fit, len_x, len_y):
        """
        reconstruit le gene à partir des informations contenues dans le fichier de sauvgarde

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

    def jardin(self) -> Jardin:
        """
        Créer le jardin corespondant à ce gene
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
                    allele = self.ADN[(x + (y * self.len_x)) * 365 + N_bit_espece*jour :
                                      (x + (y * self.len_x)) * 365 + N_bit_espece*jour
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
                            plante.planter(emplacement, idx_depart, idx_fin,x,y,jar)
                        except ValueError:
                            pass
        return jar

    def fitness(self):
        """
        met a jour la caractéristique fit du gene

        Returns
        -------
        fit : float
            le rendement du gene.

        """
        fit = self.jardin().rendement(True)
        self.fit = fit
        return fit


class Generation():

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
                genes.append(Gene.from_file(adn, fit, len_x, len_y))
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
        gene_de_base = self.genes
        self._selection()
        self._croisement()
        gen_suivante = Generation(self._mutation())
        self.genes = gene_de_base
        return gen_suivante

    def evaluation(self):
        """
        Permet de trier la liste des genes dans l'odre décroissant de qualité

        Returns
        -------
        None.

        """
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
        self.genes = self.genes[:(len(self.genes)//10)]
    
    def _mutation(self) -> list:
        """
        Permet de faire muter la liste des genes. Chaque gene a 2/5 chances de muter

        Returns
        -------
        List.
        
        """
        population = self.genes
        len_x, len_y = population[0].len_x, population[0].len_y
        rendu = []
        for gene in population:
            aleatoire1 = rd.randint(1, 50)
            if aleatoire1 > 30:
                nbr_caractere_a_muter_aleatoire = rd.randint(1, int(0.3*len(gene.ADN)))
                place_caractere_aleatoire = rd.randint(0, int(len(gene.ADN)-nbr_caractere_a_muter_aleatoire)-1)
                inverse = ""
                for bit in gene.ADN[place_caractere_aleatoire:place_caractere_aleatoire+nbr_caractere_a_muter_aleatoire]:
                    if bit == "0":
                        inverse += "1"
                    else:
                        inverse += "0"
                if (len(gene.ADN[0:place_caractere_aleatoire] + inverse + gene.ADN[place_caractere_aleatoire + nbr_caractere_a_muter_aleatoire  : len(gene.ADN)])) != len(gene.ADN):
                    gene2 = gene
                else:
                    gene2 =Gene(len_x, len_y , gene.ADN[0:place_caractere_aleatoire] + inverse + gene.ADN[place_caractere_aleatoire + nbr_caractere_a_muter_aleatoire: len(gene.ADN)] )
            else:
                gene2 =gene
            rendu.append(gene2)
        return rendu

    def _croisement(self) -> list:
        """
        Permet de croiser les genes.

        Returns
        -------
        None.
        
        """
        
        population_depart = self.genes
        len_x, len_y = population_depart[0].len_x, population_depart[0].len_y
        liste_gene = []
        for pop_index in range(5):
            population = population_depart[pop_index*(len(population_depart)//5) :(pop_index+1)*(len(population_depart)//5)]
            for index in population:
                for multi in range(10):
                    ADN = ""
                    for i in range(5):
                        ADN += population[rd.randint(0, len(population)-1)].ADN[int(len(population[0].ADN)/5)*i:(i+1)*int(len(population[0].ADN)/5)]
                    liste_gene.append(Gene(len_x, len_y, ADN))
        self.genes = liste_gene
    
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
    def __init__(self, len_x, len_y, taille_pop, overright = False):
        """
        créé un nouvel essai.

        Parameters
        ----------
        len_x : int
            longueur du jardin selon X.
        len_y : int
            longueur du jardin selon Y.
        taille_pop : int
            nombre de membre de la pop, mettre au moins 100
        overright : bool, optional
            mettre à True pour controler la pop de départ. The default is False.

        Returns
        -------
        None.

        """
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
                        calendrier[iterateur + time_chunk] = Jachere()
                        ADN[iterateur + time_chunk] = N_bit_espece*"0"
                        iterateur += time_chunk + 1
                    else:
                        calendrier[iterateur:365] = [plante_aléatoire()]*(364-iterateur +1)
                        ADN[iterateur:365] = [identificateur]*(364-iterateur +1)
                        iterateur = 365
            return "".join(ADN)
        self.generations = []
        if not overright:
            liste_gene = [Gene(len_x, len_y)
                          for i in range(taille_pop)]
            self.generations.append(Generation(liste_gene))

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
        sauvegarde l'essai dans l'emplacement voulu, avec le nom voulu.

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
    
    def evolution_statistique(self):
        from matplotlib import pyplot as plt
        distribution = []
        X = []
        for n, generation in enumerate(self.generations):
            distribution.append(generation.get_fitness())
            X.append(n)
        plt.violinplot(distribution, X)
        plt.title("Evolution de la repartition statistique du rendement en fonction des generations")
        plt.xlabel("generation")
        plt.ylabel("rendement")
        return plt