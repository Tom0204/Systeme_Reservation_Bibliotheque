import json
from src.models import User, Abonnement
from datetime import datetime
from collections import deque


class UserManager:
    def __init__(self, path='data/users.json'):
        self.path = path
        self.users = []
        self.load()

    def add_user(self, user):
        if any(u.username == user.username for u in self.users):
            raise Exception("Nom d'utilisateur déjà existant.")
        self.users.append(user)
        self.save()

    def save(self):
        data = []
        for u in self.users:
            abo_dict = None
            if u.abonnement is not None:
                abo_dict = {
                    "nom": u.abonnement.nom,
                    "max_emprunts": u.abonnement.max_emprunts,
                    "duree_emprunt_jours": u.abonnement.duree_emprunt_jours,
                    "tarif_penalite_par_jour": u.abonnement.tarif_penalite_par_jour,
                    "date_expiration": u.abonnement.date_expiration.isoformat(),
                }
            data.append({
                "username": u.username,
                "password_hash": u.password_hash,
                "admin": u.is_admin,
                "emprunts_en_cours": u.emprunts_en_cours,
                "historique_emprunts": [
                    (isbn, date_emprunt.isoformat(), date_retour.isoformat() if date_retour else None)
                    for isbn, date_emprunt, date_retour in u.historique_emprunts
                ],
                "reservations": list(u.reservations),
                "loan_count_this_month": u.loan_count_this_month,
                "last_reset_month": u.last_reset_month,  # <== virgule ajoutée ici
                "abonnement": abo_dict
            })
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)


    def load(self):
        try:
            with open(self.path, "r", encoding="utf-8") as f:
                data = json.load(f)
            self.users = []
            for u in data:
                user = User(u["username"], "", u["admin"])
                user.password_hash = u["password_hash"]
                user.emprunts_en_cours = u.get("emprunts_en_cours", [])
                user.loan_count_this_month = u.get("loan_count_this_month", 0)
                user.last_reset_month = u.get("last_reset_month", datetime.now().month)
                user.reservations = deque(u.get("reservations", []))

                # Convertir historique_emprunts (dates ISO vers date)
                user.historique_emprunts = []
                for isbn, dt_emprunt_str, dt_retour_str in u.get("historique_emprunts", []):
                    dt_emprunt = datetime.fromisoformat(dt_emprunt_str).date()
                    dt_retour = datetime.fromisoformat(dt_retour_str).date() if dt_retour_str else None
                    user.historique_emprunts.append((isbn, dt_emprunt, dt_retour))

                # Reconstruction de l'abonnement
                abo_data = u.get("abonnement")
                if abo_data:
                    user.abonnement = Abonnement(
                        abo_data["nom"],
                        abo_data["max_emprunts"],
                        abo_data["duree_emprunt_jours"],
                        abo_data["tarif_penalite_par_jour"],
                        datetime.fromisoformat(abo_data["date_expiration"]).date()
                    )
                else:
                    user.abonnement = None

                self.users.append(user)
        except FileNotFoundError:
            self.users = []


    def get_user(self, username):
        for u in self.users:
            if u.username == username:
                return u
        return None