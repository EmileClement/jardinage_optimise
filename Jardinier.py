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
        self.emplacement = [[Emplacement(self) for i in range(len_x)] for j in range(len_y)]

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
    
    def representation_interactive(self):
        """
        Enregistre un fichier html avec la représentation graphique du jardin et l'ouvre dans le navigateur
        

        Returns
        -------
        None.

        """
        
        import plotly.graph_objects as go
        from plotly.offline import plot
        jard = self
        fig = go.Figure()
        for jour in range(365):
            for yy in range(len(jard.emplacement)):
                for xx in range(len(jard.emplacement[yy])):
                    fig.add_trace(
                        go.Scatter(
                            visible=False,
                            mode = 'markers',
                            marker = dict(color=jard.emplacement[yy][xx].calendrier[jour].color,size = 100),
                            name = jour,
                            hovertemplate = str(jard.emplacement[yy][xx].calendrier[jour]),
                            x=[xx],
                            y=[yy]))
        steps = []
        for jour in range(365):
            step = dict(
                method="update",
                args=[{"visible": [False] * len(fig.data)},
                      {"title": "Jour " + str(jour)}],  # layout attribute
            )
            for i in range(len(fig.data)):
                if int(fig.data[i]['name']) == jour:
                    step["args"][0]["visible"][i] = True  # Toggle i'th trace to "visible"
                    
            steps.append(step)
        
        sliders = [dict(
            active=0,
            pad={"t": 50},
            steps=steps
        )]
        
        fig.update_layout(
            sliders=sliders
        )
        
        plot(fig)

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
        self.color = "#000000"

    def __repr__(self):
        return "Jachère"
    def __str__(self):
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

    def recolte_masse(self, jour, biais=False) -> float:
        """
        Quel quantité va on récolter ce jour.


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
                    allele = self.ADN[(x + (y * self.len_x)) * 365 + 2*jour :
                                      (x + (y * self.len_x)) * 365 + 2*jour
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
        # import sp
        # def parser():
        #     """Renvoie le Parser complilé"""
        #     blancs = sp.R(r'\s+')

        #     adn = sp.R(r'[0-9a-fx]+') / (lambda x: int(x, 16))
        #     vide = sp.R('None') / (lambda x: None)
        #     nombre = sp.R(r'[0-9]+ . [0-9]+') / (lambda x: int(x))
        #     vrai = sp.R('True') / (lambda x: True)
        #     faux = sp.R('False') / (lambda x: False)
            
        #     with sp.Separator(blancs):
        #         valeur = sp.Rule()
        #         gene = sp.Rule()
        #         entete = sp.Rule()
        #         generation = sp.Rule()
        #         boolean = sp.Rule()

        #         boolean |= vrai | faux
        #         entete |= boolean & ":\n"
        #         valeur |= vide | nombre
        #         gene |= valeur & ";" & adn 
        #         generation |= entete[1:1] & gene[1::"\n"] & "\n"
                
        #     return generation
        # try:
        #     decodeur = parser()
        # except SyntaxError as erreur:
        #     print(erreur)
        # return decodeur(data)
        

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
        self.generations = []
        if not overright:
            liste_gene = [Gene(len_x, len_y,
                               "".join([generateur_aleatoire_mais_pas_trop()
                                        for j in range(len_x * len_y)]))
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


def generateur_aleatoire_mais_pas_trop():
    decodeur_espece = Gene.decodeur_espece
    calendrier = [0]*365
    ADN = [0]*365
    iterateur = 0
    while iterateur < 365:
        identificateur = str(rd.randint(0, 1)) + str(rd.randint(0, 1))
        plante_aléatoire = decodeur_espece[str(rd.randint(0, 1)) + str(rd.randint(0, 1))]
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



#def test_optimisation_1(nombre_population, nombre_iteration, x_len, y_len) -> list:
#    population = []
#    res = []
#    for i in range(nombre_population):
#        population.append(Gene(x_len, y_len))
##        if ((100*i)//nombre_population)%10 == 0 and (10*i)//nombre_population>= 1:
##            print((100*i)//nombre_population)
#    check = selection(population)
#    res.append((selection(population)[-1].jardin().rendement()))
#    print(check[-1].jardin().rendement())
#    for i in range(nombre_iteration):
#        population = selection(population)
#        population = croisement(population)
#        population = mutation(population)
##        if (100*i//nombre_iteration)%10 == 0 and (10*i)//nombre_iteration>= 1:
##            print((100*i)//nombre_iteration)
#        res.append((selection(population)[-1].jardin().rendement()))
#
#    return population,res

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
