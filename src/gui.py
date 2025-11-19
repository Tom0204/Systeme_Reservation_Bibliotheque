import tkinter as tk
from tkinter import ttk, messagebox
from src.models import Livre, Bibliotheque

class ApplicationBibliotheque(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Application Bibliothèque")
        self.geometry("600x400")

        self.biblio = Bibliotheque("Ma bibliothèque")

        # ajout livre
        self.frame_ajout = ttk.Frame(self)
        self.frame_ajout.pack(padx=10, pady=10, fill="x")

        ttk.Label(self.frame_ajout, text="Titre :").pack(side="left")
        self.entry_titre = ttk.Entry(self.frame_ajout, width=20)
        self.entry_titre.pack(side="left", padx=(0, 10))

        ttk.Label(self.frame_ajout, text="Auteur :").pack(side="left")
        self.entry_auteur = ttk.Entry(self.frame_ajout, width=20)
        self.entry_auteur.pack(side="left", padx=(0, 10))

        ttk.Label(self.frame_ajout, text="ISBN :").pack(side="left")
        self.entry_isbn = ttk.Entry(self.frame_ajout, width=15)
        self.entry_isbn.pack(side="left", padx=(0, 10))

        self.btn_ajouter = ttk.Button(self.frame_ajout, text="Ajouter le livre", command=self.ajouter_livre)
        self.btn_ajouter.pack(side="left", padx=5)

        # recherche par auteur
        self.frame_recherche = ttk.Frame(self)
        self.frame_recherche.pack(padx=10, pady=5, fill="x")

        ttk.Label(self.frame_recherche, text="Recherche par auteur :").pack(side="left")
        self.entry_rech_auteur = ttk.Entry(self.frame_recherche, width=20)
        self.entry_rech_auteur.pack(side="left")
        self.btn_recherche = ttk.Button(self.frame_recherche, text="Rechercher", command=self.rechercher_par_auteur)
        self.btn_recherche.pack(side="left", padx=5)

        # Affichage
        self.frame_liste = ttk.Frame(self)
        self.frame_liste.pack(fill="both", expand=True, padx=10, pady=10)
        self.tree = ttk.Treeview(self.frame_liste, columns=("Titre", "Auteur", "ISBN"), show="headings")
        self.tree.heading("Titre", text="Titre")
        self.tree.heading("Auteur", text="Auteur")
        self.tree.heading("ISBN", text="ISBN")
        self.tree.pack(fill="both", expand=True)

        self.actualiser_liste()

    def ajouter_livre(self):
        titre = self.entry_titre.get().strip()
        auteur = self.entry_auteur.get().strip()
        isbn = self.entry_isbn.get().strip()
        if titre and auteur and isbn:
            livre = Livre(titre, auteur, isbn)
            self.biblio.ajouter_livre(livre)
            self.actualiser_liste()
            self.entry_titre.delete(0, tk.END)
            self.entry_auteur.delete(0, tk.END)
            self.entry_isbn.delete(0, tk.END)
        else:
            messagebox.showerror("Erreur", "Veuillez remplir tous les champs.")

    def actualiser_liste(self, livres=None):
        for row in self.tree.get_children():
            self.tree.delete(row)
        if livres is None:
            livres = self.biblio.livres
        for livre in livres:
            self.tree.insert("", "end", values=(livre.titre, livre.auteur, livre.ISBN))

    def rechercher_par_auteur(self):
        auteur = self.entry_rech_auteur.get().strip()
        if not auteur:
            self.actualiser_liste()
        else:
            livres = self.biblio.recherche_par_auteur(auteur)
            self.actualiser_liste(livres)

if __name__ == "__main__":
    app = ApplicationBibliotheque()
    app.mainloop()
