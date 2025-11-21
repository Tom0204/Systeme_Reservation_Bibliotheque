import tkinter as tk
from tkinter import ttk, messagebox
from src.models import User
from src.user_manager import UserManager

class FenetreInscription(tk.Toplevel):
    def __init__(self, master, user_manager):
        super().__init__(master)
        self.title("Inscription utilisateur")
        self.user_manager = user_manager

        ttk.Label(self, text="Nom d'utilisateur :").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.entry_username = ttk.Entry(self)
        self.entry_username.grid(row=0, column=1, padx=10, pady=5)

        ttk.Label(self, text="Mot de passe :").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.entry_mdp = ttk.Entry(self, show="*")
        self.entry_mdp.grid(row=1, column=1, padx=10, pady=5)

        ttk.Label(self, text="Confirmer mot de passe :").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.entry_mdp_confirm = ttk.Entry(self, show="*")
        self.entry_mdp_confirm.grid(row=2, column=1, padx=10, pady=5)

        # Checkbox "Administrateur"
        self.admin_var = tk.BooleanVar()
        self.checkbox_admin = ttk.Checkbutton(self, text="Administrateur", variable=self.admin_var)
        self.checkbox_admin.grid(row=3, column=0, columnspan=2, pady=5)

        self.btn_valider = ttk.Button(self, text="Créer le compte", command=self.creer_utilisateur)
        self.btn_valider.grid(row=3, column=0, columnspan=2, pady=10)

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
            new_user = User(username, mdp, admin=est_admin)
            self.user_manager.add_user(new_user)
            messagebox.showinfo("Succès", "Utilisateur créé avec succès !")
            self.destroy()  # Ferme la fenêtre d'inscription
        except Exception as e:
            messagebox.showerror("Erreur", str(e))