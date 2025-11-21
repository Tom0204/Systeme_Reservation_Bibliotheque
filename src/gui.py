import tkinter as tk
from tkinter import ttk, messagebox
from src.models import Livre, Bibliotheque, User, Abonnement
from src.file_manager import BibliothequeAvecFichier
from src.user_manager import UserManager
from datetime import datetime, timedelta

class ApplicationBibliotheque(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Application Bibliothèque")
        self.geometry("1920x1080")

        self.path_json = "data/bib.json"
        self.path_csv = "data/catalogue.csv"

        self.biblio = BibliothequeAvecFichier(Bibliotheque("Ma bibliothèque"))
        self.user_manager = UserManager()

        try:
            self.biblio.charger(self.path_json)
        except Exception as e:
            messagebox.showwarning("Attention", f"Erreur au chargement du JSON : {e}")

        self.btn_inscription = ttk.Button(self, text="S'inscrire", command=self.ouvrir_fenetre_inscription)
        self.btn_inscription.pack(pady=10)

        self.frame_abonnement = ttk.Label(self)
        self.frame_abonnement.pack(pady = 5)
        self.lbl_abonnement = ttk.Label(self.frame_abonnement, text="Abonnement : ")  # Label enfant du frame
        self.lbl_abonnement.pack(side="left")

        self.btn_renouveler = ttk.Button(self.frame_abonnement, text="Renouveler abonnement", command=self.renouveler_abonnement)
        self.btn_renouveler.pack(side="left", padx=5)

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

        self.frame_recherche = ttk.Frame(self)
        self.frame_recherche.pack(padx=10, pady=5, fill="x")

        ttk.Label(self.frame_recherche, text="Recherche par auteur :").pack(side="left")
        self.entry_rech_auteur = ttk.Entry(self.frame_recherche, width=20)
        self.entry_rech_auteur.pack(side="left")

        self.btn_recherche = ttk.Button(self.frame_recherche, text="Rechercher", command=self.rechercher_par_auteur)
        self.btn_recherche.pack(side="left", padx=5)

        self.frame_liste = ttk.Frame(self)
        self.frame_liste.pack(fill="both", expand=True, padx=10, pady=10)

        self.tree = ttk.Treeview(self.frame_liste, columns=("Titre", "Auteur", "ISBN", "Disponible"), show="headings", selectmode="extended")
        self.tree.heading("Titre", text="Titre")
        self.tree.heading("Auteur", text="Auteur")
        self.tree.heading("ISBN", text="ISBN")
        self.tree.heading("Disponible", text="Disponible")
        self.tree.pack(fill="both", expand=True)


        self.frame_actions = ttk.Frame(self)
        self.frame_actions.pack(fill="x", padx=10, pady=(0, 10))

        self.btn_save = ttk.Button(self.frame_actions, text="Sauvegarder", command=self.sauvegarder_bibliotheque)
        self.btn_save.pack(side="left", padx=5)

        self.btn_delete = ttk.Button(self.frame_actions, text="Supprimer le livre sélectionné", command=self.supprimer_livre_selectionne)
        self.btn_delete.pack(side="left", padx=5)

        self.btn_emprunter = ttk.Button(self.frame_actions, text="Emprunter livre sélectionné", command=self.emprunter_livre_selectionne)
        self.btn_emprunter.pack(side="left", padx=5)

        self.btn_retourner = ttk.Button(self.frame_actions, text="Retourner livre emprunté", command=self.retourner_livre_utilisateur)
        self.btn_retourner.pack(side="left", padx=5)

        self.btn_historique = ttk.Button(self.frame_actions, text="Afficher historique emprunt", command=self.afficher_historique_utilisateur)
        self.btn_historique.pack(side="left", padx=5)

        self.btn_reserver = ttk.Button(self.frame_actions, text="Réserver livre sélectionné", command=self.reserver_livre_selectionne)
        self.btn_reserver.pack(side="left", padx=5)

        self.btn_annuler_resa = ttk.Button(self.frame_actions, text="Annuler réservation", command=self.annuler_reservation_livre_selectionne)
        self.btn_annuler_resa.pack(side="left", padx=5)

        self.btn_file_attente = ttk.Button(self.frame_actions, text="Afficher file attente", command=self.afficher_file_attente_livre_selectionne)
        self.btn_file_attente.pack(side="left", padx=5)

        self.utilisateur_courant = None
        if self.user_manager.users:
            self.utilisateur_courant = self.user_manager.users[0]
        self.actualiser_liste()
        self.actualiser_affichage_abonnement()

        self.btn_connexion = ttk.Button(self, text="Se connecter", command=self.ouvrir_fenetre_connexion)
        self.btn_connexion.pack(pady=5)

        self.btn_deconnexion = ttk.Button(self, text="Se déconnecter", command=self.se_deconnecter)
        self.btn_deconnexion.pack(pady=5)
        self.btn_deconnexion.config(state="disabled")

    def ouvrir_fenetre_connexion(self):
        FenetreConnexion(self, self.user_manager, self.utilisateur_connecte)

    def utilisateur_connecte(self, user):
        self.utilisateur_courant = user
        self.actualiser_affichage_abonnement()
        self.btn_deconnexion.config(state="normal")
        self.btn_connexion.config(state="disabled")
        # Notification si réservations disponibles
        self.verifier_notifications_reservations()
    
    def se_connecter(self):
        username = self.entry_username.get().strip()
        mdp = self.entry_mdp.get()
        user = self.user_manager.get_user_by_username(username)
        if user and user.check_password(mdp):
            self.on_connexion(user)  # notifier la fenêtre principale
            self.destroy()
        else:
            messagebox.showerror("Erreur", "Nom d'utilisateur ou mot de passe incorrect.")


    def se_deconnecter(self):
        self.utilisateur_courant = None
        self.actualiser_affichage_abonnement()
        self.btn_deconnexion.config(state="disabled")
        self.btn_connexion.config(state="normal")
        messagebox.showinfo("Déconnexion", "Vous êtes déconnecté.")

    def verifier_notifications_reservations(self):
        if self.utilisateur_courant is None:
            return
        messages = []
        for livre in self.biblio.bibliotheque.livres:
            if livre.file_attente_reservations and livre.file_attente_reservations[0].username == self.utilisateur_courant.username:
                messages.append(f"Le livre '{livre.titre}' est maintenant disponible.")
        if messages:
            messagebox.showinfo("Notifications", "\n".join(messages), parent=self)
    
    def actualiser_affichage_abonnement(self):
        if self.utilisateur_courant is None or self.utilisateur_courant.abonnement is None:
            texte = "Aucun abonnement"
        else:
            abo = self.utilisateur_courant.abonnement
            texte = f"{abo.nom} (expire le {abo.date_expiration})"
        self.lbl_abonnement.config(text=texte)

    def renouveler_abonnement(self):
        if self.utilisateur_courant is None or self.utilisateur_courant.abonnement is None:
            messagebox.showerror("Erreur", "Pas d'abonnement à renouveler.")
            return
        try:
            self.utilisateur_courant.renouveler_abonnement()
            self.user_manager.save()
            self.actualiser_affichage_abonnement()
            messagebox.showinfo("Succès", "Abonnement renouvelé avec succès.")
        except Exception as e:
            messagebox.showerror("Erreur", str(e))

    def ouvrir_fenetre_inscription(self):
        FenetreInscription(self, self.user_manager, self.utilisateur_connecte)

    def ajouter_livre(self):
        titre = self.entry_titre.get().strip()
        auteur = self.entry_auteur.get().strip()
        isbn = self.entry_isbn.get().strip()
        if titre and auteur and isbn:
            livre = Livre(titre, auteur, isbn)
            self.biblio.bibliotheque.ajouter_livre(livre)
            self.actualiser_liste()
            self.entry_titre.delete(0, tk.END)
            self.entry_auteur.delete(0, tk.END)
            self.entry_isbn.delete(0, tk.END)
        else:
            messagebox.showerror("Erreur", "Veuillez remplir tous les champs.")

    def supprimer_livre_selectionne(self):
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Aucun livre", "Veuillez sélectionner au moins un livre à supprimer.")
            return
        if not messagebox.askyesno("Confirmer", "Voulez-vous vraiment supprimer le(s) livre(s) sélectionné(s) ?"):
            return
        for item in selection:
            values = self.tree.item(item, "values")
            isbn = values[2]
            self.biblio.bibliotheque.supprimer_livre(isbn)
        self.actualiser_liste()

    def sauvegarder_bibliotheque(self):
        try:
            self.biblio.sauvegarder(self.path_json)
            self.biblio.export_csv(self.path_csv)
            self.user_manager.save()
            messagebox.showinfo("Succès", "Bibliothèque et utilisateurs sauvegardés !")
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de la sauvegarde : {e}")

    def actualiser_liste(self, livres=None):
        for row in self.tree.get_children():
            self.tree.delete(row)
        if livres is None:
            livres = self.biblio.bibliotheque.livres
        for livre in livres:
            dispo = "Oui" if livre.est_disponible() else "Non"
            self.tree.insert("", "end", values=(livre.titre, livre.auteur, livre.ISBN, dispo))

    def rechercher_par_auteur(self):
        auteur = self.entry_rech_auteur.get().strip()
        if not auteur:
            self.actualiser_liste()
        else:
            livres = self.biblio.bibliotheque.recherche_par_auteur(auteur)
            self.actualiser_liste(livres)

    def emprunter_livre_selectionne(self):
        if self.utilisateur_courant is None:
            messagebox.showerror("Erreur", "Aucun utilisateur connecté.")
            return
        if self.utilisateur_courant.penalites_impayees > 0:
            messagebox.showerror("Erreur", f"Emprunt refusé, vous avez {self.utilisateur_courant.penalites_impayees:.2f}€ de pénalités impayées.")
            return
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Aucune sélection", "Veuillez sélectionner un livre à emprunter.")
            return
        isbn = self.tree.item(selection[0], "values")[2]
        try:
            self.biblio.bibliotheque.emprunter_livre(isbn, self.utilisateur_courant)
            self.user_manager.save()
            self.actualiser_liste()
            messagebox.showinfo("Succès", f"Le livre {isbn} a été emprunté.")
        except Exception as e:
            messagebox.showerror("Erreur", str(e))

    def retourner_livre_utilisateur(self):
        if self.utilisateur_courant is None:
            messagebox.showerror("Erreur", "Aucun utilisateur connecté.")
            return
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Aucune sélection", "Veuillez sélectionner un livre à retourner.")
            return
        isbn = self.tree.item(selection[0], "values")[2]
        try:
            self.biblio.retourner_livre(isbn, self.utilisateur_courant, notifier=self.notifier_utilisateur)
            self.user_manager.save()
            self.actualiser_liste()
            messagebox.showinfo("Succès", f"Le livre {isbn} a été retourné.")
        except Exception as e:
            messagebox.showerror("Erreur", str(e))

    def afficher_historique_utilisateur(self):
        if self.utilisateur_courant is None:
            messagebox.showerror("Erreur", "Aucun utilisateur connecté.")
            return
        penalites = self.utilisateur_courant.calculer_penalites()
        historique = self.utilisateur_courant.historique_emprunts
        if not historique:
            messagebox.showinfo("Historique", "Aucun emprunt effectué.")
            return
        msg = f"Pénalités impayées : {penalites:.2f}€\n\n"
        for isbn, date_emprunt, date_retour in historique:
            msg += f"ISBN: {isbn} | Emprunté: {date_emprunt} | Retourné: {date_retour or 'Pas encore'}\n"
        messagebox.showinfo("Historique Emprunts", msg)

    def reserver_livre_selectionne(self):
        if self.utilisateur_courant is None:
            messagebox.showerror("Erreur", "Aucun utilisateur connecté.")
            return
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Aucune sélection", "Veuillez sélectionner un livre à réserver.")
            return
        isbn = self.tree.item(selection[0], "values")[2]
        try:
            self.biblio.bibliotheque.reserver_livre(isbn, self.utilisateur_courant)
            self.user_manager.save()
            messagebox.showinfo("Succès", f"Le livre {isbn} a été réservé.")
        except Exception as e:
            messagebox.showerror("Erreur", str(e))

    def annuler_reservation_livre_selectionne(self):
        if self.utilisateur_courant is None:
            messagebox.showerror("Erreur", "Aucun utilisateur connecté.")
            return
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Aucune sélection", "Veuillez sélectionner un livre dont vous voulez annuler la réservation.")
            return
        isbn = self.tree.item(selection[0], "values")[2]
        livre = self.biblio.bibliotheque.trouver_livre_par_isbn(isbn)
        if not livre:
            messagebox.showerror("Erreur", "Livre non trouvé.")
            return
        try:
            livre.annuler_reservation(self.utilisateur_courant)
            self.utilisateur_courant.annuler_reservation(isbn)
            self.user_manager.save()
            messagebox.showinfo("Succès", "Réservation annulée.")
        except Exception as e:
            messagebox.showerror("Erreur", str(e))

    def afficher_file_attente_livre_selectionne(self):
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Aucune sélection", "Veuillez sélectionner un livre.")
            return
        isbn = self.tree.item(selection[0], "values")[2]
        livre = self.biblio.trouver_livre_par_isbn(isbn)
        if not livre:
            messagebox.showerror("Erreur", "Livre non trouvé.")
            return
        file_attente = livre.file_attente_reservations
        if not file_attente:
            messagebox.showinfo("File d'attente", "Pas de réservations pour ce livre.")
            return
        msg = "File d'attente des réservations :\n"
        msg += "\n".join([user.username for user in file_attente])
        messagebox.showinfo("File d'attente", msg)

    def notifier_utilisateur(self, user: User, message: str):
        messagebox.showinfo(f"Notification pour {user.username}", message, parent=self)



class FenetreConnexion(tk.Toplevel):
    def __init__(self, master, user_manager, on_connexion):
        super().__init__(master)
        self.title("Connexion")
        self.user_manager = user_manager
        self.on_connexion = on_connexion

        ttk.Label(self, text="Nom d'utilisateur :").grid(row=0, column=0, padx=10, pady=5)
        self.entry_username = ttk.Entry(self)
        self.entry_username.grid(row=0, column=1, padx=10, pady=5)

        ttk.Label(self, text="Mot de passe :").grid(row=1, column=0, padx=10, pady=5)
        self.entry_mdp = ttk.Entry(self, show="*")
        self.entry_mdp.grid(row=1, column=1, padx=10, pady=5)

        btn_connexion = ttk.Button(self, text="Se connecter", command=self.se_connecter)
        btn_connexion.grid(row=2, column=0, columnspan=2, pady=10)

    def se_connecter(self):
        username = self.entry_username.get().strip()
        mdp = self.entry_mdp.get()
        user = self.user_manager.get_user(username)
        if user and user.check_password(mdp):
            self.on_connexion(user)
            self.destroy()
        else:
            messagebox.showerror("Erreur", "Nom d'utilisateur ou mot de passe incorrect.")



class FenetreInscription(tk.Toplevel):
    def __init__(self, master, user_manager, on_connexion):
        super().__init__(master)
        self.title("Connexion")
        self.user_manager = user_manager
        self.on_connexion = on_connexion    

        ttk.Label(self, text="Nom d'utilisateur :").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.entry_username = ttk.Entry(self)
        self.entry_username.grid(row=0, column=1, padx=10, pady=5)

        ttk.Label(self, text="Mot de passe :").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.entry_mdp = ttk.Entry(self, show="*")
        self.entry_mdp.grid(row=1, column=1, padx=10, pady=5)

        ttk.Label(self, text="Confirmer mot de passe :").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.entry_mdp_confirm = ttk.Entry(self, show="*")
        self.entry_mdp_confirm.grid(row=2, column=1, padx=10, pady=5)

        self.admin_var = tk.BooleanVar()
        self.chk_admin = ttk.Checkbutton(self, text="Administrateur", variable=self.admin_var)
        self.chk_admin.grid(row=3, column=0, columnspan=2, pady=5)

        self.btn_valider = ttk.Button(self, text="Créer le compte", command=self.creer_utilisateur)
        self.btn_valider.grid(row=4, column=0, columnspan=2, pady=10)

    def creer_utilisateur(self):
        username = self.entry_username.get().strip()
        mdp = self.entry_mdp.get()
        mdp_confirm = self.entry_mdp_confirm.get()
        est_admin = self.admin_var.get()

        if not username or not mdp or not mdp_confirm:
            messagebox.showerror("Erreur", "Tous les champs doivent être remplis.")
            return

        if mdp != mdp_confirm:
            messagebox.showerror("Erreur", "Les mots de passe ne correspondent pas.")
            return

        try:
            abo_defaut = Abonnement(
            nom="basique",
            max_emprunts=1,
            duree_emprunt_jours=14,
            tarif_penalite_par_jour=0.50,
            date_expiration=datetime.now().date() + timedelta(days=365)
        )
            new_user = User(username, mdp, admin=est_admin, abonnement=abo_defaut)
            self.user_manager.add_user(new_user)
            messagebox.showinfo("Succès", "Utilisateur créé avec succès !")
            if self.on_connexion:
                self.on_connexion(new_user)
            self.destroy()
        except Exception as e:
            messagebox.showerror("Erreur", str(e))


if __name__ == "__main__":
    app = ApplicationBibliotheque()
    app.mainloop()