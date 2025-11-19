# models
from src.exceptions import LivreNonTrouveErreur

class Livre:
    def __init__(self, titre, auteur, ISBN):
        self.titre = titre
        self.auteur = auteur
        self.ISBN = ISBN
    
    def to_dict(self):
        return {
            "type" : "Livre",
            "titre" : self.titre,
            "auteur" : self.auteur,
            "ISBN" : self.ISBN
        }

class LivreNumerique(Livre):
    def __init__(self, titre, auteur, ISBN, taille_fichier):
        super().__init__(titre, auteur, ISBN)
        self.taille_fichier = taille_fichier
    
    def to_dict(self):
        base = super().to_dict()
        base["type"] = "Livre Numerique"
        base["taille_fichier"] = self.taille_fichier
        return base

class Bibliotheque:
    def __init__(self, nom):
        self.nom = nom
        self.livres = []
    
    def ajouter_livre(self, livre):
        self.livres.append(livre)
    
    def supprimer_livre(self, ISBN):
        for livre in self.livres:
            if livre.ISBN == ISBN:
                self.livres.remove(livre)
                return
            raise LivreNonTrouveErreur(ISBN) # Lève l'exception personnalisée
    
    def recherche_par_titre(self, titre):
        resultats = [livre for livre in self.livres if livre.titre == titre]
        return resultats
    
    def recherche_par_auteur(self, auteur):
        resultats = [livre for livre in self.livres if livre.auteur.lower() == auteur.lower()]
        return resultats