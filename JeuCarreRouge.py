## -*- coding: utf8 -*-
from tkinter import *
from timeit import default_timer
"""
Fenetre = Tk()

def updatetime():
    now = default_timer - start 
    minutes, seconds = divmod(now, 60)
    hours, minutes = divmod(now,60)
    str_time = "%d:%02d:%02d" % (hours, minutes, seconds)
    canvas.itemconfigure(text_clock, text=str_time)
    Fenetre.after(1000, updatetime)
"""
class Pion():
    def __init__(self,x,y,sizex,sizey,dirx,diry):
        self.x=x
        self.y=y
        self.sizex=sizex/2
        self.sizey=sizey/2
        self.dirx=dirx
        self.diry=diry
        self.vitesse=2
        
    def deplacer(self):
        self.x += self.dirx * self.vitesse
        self.y += self.diry * self.vitesse
        
        if self.x < 0 + self.sizex:
            self.dirx = 1
        elif self.x > 450 - self.sizex:
            self.dirx = -1
            
        if self.y < 0 + self.sizey:
            self.diry = 1
        elif self.y > 450 - self.sizey:
            self.diry = -1

       


class CarreRouge():
    def __init__(self,x,y):
        self.x=x
        self.y=y
        self.sizex=40/2
        self.sizey=40/2
        self.isAlive=True
        
    def deplacer(self,x,y):
        self.x=x
        self.y=y
        
        if self.x < 50 + self.sizex:
            self.x=50 + self.sizex
            self.isAlive=False
        elif self.x > 400 - self.sizex:
            self.x=400 - self.sizex
            self.isAlive=False
            
        if self.y < 50 + self.sizey:
            self.y=50 + self.sizey
            self.isAlive=False
        elif self.y > 400 - self.sizey:
            self.y=400 - self.sizey
            self.isAlive=False


class Modele():
    def __init__(self):
        self.hauteur=450
        self.largeur=450
        self.pions=[]
        self.pions.append(Pion(100,100,60,60,1,1))
        self.pions.append(Pion(300,85,60,50,-1,1))
        self.pions.append(Pion(85,350,30,60,1,-1))
        self.pions.append(Pion(355,340,100,20,-1,-1))
        self.carreRouge=CarreRouge(225,225)
    
    def demandeDeplacementPions(self):
        for i in self.pions:
            i.deplacer()
            
    def testerCollision(self):     
        for i in self.pions:
            if i.y+i.sizey > self.carreRouge.y-self.carreRouge.sizey and \
               i.x-i.sizex < self.carreRouge.x+self.carreRouge.sizex and \
               i.x+i.sizex > self.carreRouge.x-self.carreRouge.sizex and \
               i.y-i.sizey < self.carreRouge.y+self.carreRouge.sizey:
                self.carreRouge.isAlive=False


                


class Vue():
    def __init__(self, parent, modele):
        self.parent=parent
        self.modele=modele
        self.root=Tk()
        self.root.title('JEU DU CARRÉ ROUGE')
        self.root.wm_attributes('-topmost', 1) #Fenêtre de jeu en 1er plan
        self.aireDeJeu()
        menu = Menu(self.root)
        self.root.config(menu=menu)
        
        # ********* Menu **************
        subMenu = Menu(menu)
        menu.add_cascade(label="Fichier", menu=subMenu)
        subMenu.add_command(label="Nouvelle partie")
        subMenu.add_command(label="Scores")
        subMenu.add_separator()
        subMenu.add_command(label="Quiter", command=self.root.quit)
        
        # ********* Status Bar **************
        self.status=Label(self.root, text="Status...", bd=1, relief=SUNKEN, anchor=W)
        self.status.pack(side=BOTTOM, fill=X)
    
    def aireDeJeu(self):    
        self.canvas=Canvas(self.root,width=450, height=450, bg='black')
        self.canvas.pack()
        self.canvas.bind("<Button-1>",self.debuter)
        
    def debuter(self,evt):                                      # cette fonctione lance la capacite de suivi
        t=self.canvas.gettags("current")                        # on obtient les tags du dessin (un seul) sous la souris
        if "CarreRouge" in t:                                   # le tuple de tags doit contenir la chaine de texte "carre" qui indique que
            self.canvas.bind("<B1-Motion>",self.deplacer)       # on lie l'evenement movement a une fonction pour deplacer le carre
            self.canvas.bind("<ButtonRelease-1>",self.relacher) # on lie l'evenement relache du clic a une fonction pour cesser le suivi de la souris par le carre
            self.parent.demandeDeplacement()
        
    def deplacer(self,evt):
        self.parent.deplacer(evt.x,evt.y)                   # on avertit le parent des coordonnees actuelles de la souris
        
    def relacher(self,evt):    
        self.canvas.unbind("<B1-Motion>")                  # on annule l'evenement de mouvement (on cesse de l'ecouter)
        
    def afficheAireDeJeu(self):
        self.canvas.delete(ALL)                                         # Efface tout le contenu de l'aire de jeu
        self.canvas.create_rectangle(50,50,400,400,fill='white')        # Affiche l'aire de jeu du carre rouge
        for i in self.modele.pions:
            self.canvas.create_rectangle(i.x-i.sizex,
                                         i.y-i.sizey,
                                         i.x+i.sizex,
                                         i.y+i.sizey,
                                         fill="blue",
                                         tags=("Pion", str(i.x),str(i.y)))
        self.canvas.create_rectangle(self.modele.carreRouge.x-self.modele.carreRouge.sizex,
                                     self.modele.carreRouge.y-self.modele.carreRouge.sizey,
                                     self.modele.carreRouge.x+self.modele.carreRouge.sizex,
                                     self.modele.carreRouge.y+self.modele.carreRouge.sizey,
                                     fill="red",
                                     tags=("CarreRouge"))



class Controleur():
    def __init__(self):
        self.modele=Modele()
        self.vue=Vue(self, self.modele)
        self.vue.afficheAireDeJeu()
        self.vue.root.mainloop()

    def demandeDeplacement(self):
        self.modele.demandeDeplacementPions()
        self.modele.testerCollision()
        self.vue.afficheAireDeJeu()
        if self.modele.carreRouge.isAlive:
            self.vue.root.after(10, self.demandeDeplacement)

    def deplacer(self,x,y):                                 # fonction appelee par la vue lorsqu'un mouvement de souris est detecte
        self.modele.carreRouge.deplacer(x,y)                # on requiert cette action aupres du modele
        self.vue.afficheAireDeJeu()                         # on requiert cette action aupres de la vue apres les modifs au modele

if __name__ == '__main__':
    c=Controleur()
    print("Fin programme")
    


