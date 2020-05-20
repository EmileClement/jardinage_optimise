# -*- coding: utf-8 -*-
"""
Created on Fri May  8 11:30:45 2020

@author: Leopold
"""
import random as rd

class Jardin():
    def __init__(self, len_x: int, len_y: int):
        self.emplacement = [[Emplacement(self,i,j) for i in range(len_x)] for j in range(len_y)]

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
    def __init__(self,jardin,x,y):
        self.jardin = jardin
        self.calendrier = [Jachere() for i in range(365)]
        #self.voisin = self.voisin(jardin,x,y)
        self.x = x
        self.y = y


    def __repr__(self):
        return "Emplacement: " + "\n ".join([str(i) + ": " + elem.__repr__()
                                             for i, elem in
                                             enumerate(self.calendrier)]) + ";"
    def voisin(jardin,x,y) -> list:
        """
        donne les coordonées [x,y] des voisins existants 

        Parameters
        ----------
        jardin : Jardin

        Returns
        -------
        list
            [[x1,y1],[x2,y2]...]

        """
        voisins = []
        if x > 0:
            if y > 0:
                voisins.append[x-1,y-1]
            if y < len(jardin.emplacement)-1:
                voisins.append[x-1,y+1]
        if x < len(jardin.emplacement[0])-1:
            if y > 0:
                voisins.append[x+1,y-1]
            if y < len(jardin.emplacement)-1:
                voisins.append[x+1,y+1]
        return voisins
            

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
        if debut<=fin:
            for elem in self.calendrier[debut:fin]:
                libre &= isinstance(elem, Jachere)
        else:
            for elem in self.calendrier[:fin]:
                libre &= isinstance(elem, Jachere)
            for elem in self.calendrier[debut:]:
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
        self.id = 0

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
        self.multiplicateur = 1

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
        if (((jour - self.jour_semis)%365) >= self.time_chunk) and (self.deja_recolte == False):
            self.deja_recolte = True
            return self.masse_produite#*self.multiplicateur
        return biais * (self.jour_semis-self.jour_recolte)** 2 / 365 ** 2

    def planter(self, emplacement, debut, fin): #,x,y,jard):
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
            0 si la tentative de planter reussi.
        """
        if self.plantable(debut) and emplacement.libre(debut, fin):
            # for coordonee in emplacement.voisin:
            #     plante_id_reel = int(jar.emplacement[coordonee[1]][coordonee[0]].calendrier[debut].id)
            #     multiplicateur *= table_associations[self.id][plante_id_reel]
                
            if debut<= fin:
                for i in range(debut-1, fin):
                    emplacement.calendrier[i] = self
            else:
                for i in list(range(debut-1, 365)) + list(range(0, fin + 1)):
                    emplacement.calendrier[i] = self
            self.jour_semis = debut
            self.jour_recolte = fin
            return 0
        raise ValueError
        
        
        
J = Jardin(1,1)
empl = J.emplacement[0][0]