## -*- coding: utf8 -*-
from tkinter import *

class CarreRouge():
    def __init__(self,posx,posy):
        self.posx=posx
        self.posy=posy 
        self.couleur='red'

        
class Pion():
    def __init__(self,parent,posx,posy,sizex,sizey):
        self.parent=parent
        self.posx=posx
        self.posy=posy
        self.sizex=sizex
        self.sizey=sizey
        self.vitesse=1
        self.couleur='blue'
    
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!    
    def deplacer(self):
           
        self.posx-=self.vitesse
        #self.posx+=self.vitesse   
        self.posy-=self.vitesse
        #self.posy+=self.vitesse
        
    

class Vue():
    def __init__(self, parent, modele):
        self.parent=parent
        self.modele=modele
        self.root=Tk()
        self.fenetre()

        
    def fenetre(self):
        self.root.title('JEU CARRÉ ROUGE')
        self.root.resizable(0, 0) # Empeche le resize de la fenetre
        self.root.wm_attributes('-topmost', 1) # La fenetre est en 1er plan de tout
        self.canvas=Canvas(self.root,width=450,height=450, bg="black")
        self.canvas.pack()
        self.canvas.bind("<Button-1>",self.demandeDeplacement)

        
    def demandeDeplacement(self, evt):
        self.parent.demandeDeplacement()
        print('demandeDeplacement')

        
    def afficheFenetre(self):
        self.canvas.delete(ALL)
        self.canvas.create_rectangle(50,50,400,400,fill='white') #Création du carré blanc
        self.canvas.create_rectangle(205,205,245,245,fill='red')
        for i in self.modele.pions:
            self.canvas.create_rectangle(i.posx-(i.sizex/2),
                                         i.posy-(i.sizey/2),
                                         i.posx+(i.sizex/2),
                                         i.posy+(i.sizey/2),
                                         fill="blue",
                                         tags=("Pion", str(i.posx),str(i.posy)))
        
    
class Modele():
    def __init__(self,parent):
        self.largeur=450 #Largeur de l'aire de jeu
        self.hauteur=450 #Hauteur de l'aire de jeu
        #carreRouge=CarreRouge(self,225,225,40,40)
        self.pions=[]
        self.pions.append(Pion(self,100,100,60,60))
        self.pions.append(Pion(self,300,85,60,50))
        self.pions.append(Pion(self,85,350,30,60))
        self.pions.append(Pion(self,355,340,100,20))
    
     
    def demandeDeplacement(self):
        for i in self.pions:
            i.deplacer()

    
class Controleur():
    def __init__(self):
        self.modele=Modele(self)
        self.vue=Vue(self, self.modele)
        self.vue.afficheFenetre()
        self.vue.root.mainloop()

    def demandeDeplacement(self):
        self.modele.demandeDeplacement()
        self.vue.afficheFenetre()
        self.vue.root.after(5, self.demandeDeplacement) #Pilote automatique



if __name__ == '__main__':
    c=Controleur()
    print("Fin programme")
