from src.exceptions import LivreNonTrouveErreur
import hashlib
from datetime import datetime, timedelta
from collections import deque


class Livre:
    CATEGORIES_VALIDES = {"Roman", "Science-fiction", "Histoire", "Biographie", "Philosophie", "Art"}

    def __init__(self, titre, auteur, isbn, categorie=None):
        if categorie and categorie not in Livre.CATEGORIES_VALIDES:
            raise ValueError(f"Catégorie invalide : {categorie}")
        self.titre = titre
        self.auteur = auteur
        self.ISBN = isbn
        self.categorie = categorie

        self.emprunteur = None  # User ou None
        self.historique_emprunts = []  # List of tuples (user.username, date_emprunt, date_retour)
        self.file_attente_reservations = deque()  # Queue of User instances who reserved

        self.avis = []  # List of tuples (username, note, commentaire, date)
        self.date_limite_retour = None

    def est_disponible(self):
        return self.emprunteur is None

    def emprunter(self, user, duree_max_jours=14):
        if not self.est_disponible():
            raise Exception("Livre déjà emprunté")
        self.emprunteur = user
        date_emprunt = datetime.now().date()
        self.date_limite_retour = date_emprunt + timedelta(days=duree_max_jours)
        self.historique_emprunts.append((user.username, date_emprunt, None))

    def retourner(self):
        if self.est_disponible():
            raise Exception("Livre non emprunté")
        date_retour = datetime.now().date()
        for i in reversed(range(len(self.historique_emprunts))):
            username, date_emprunt, date_retour_init = self.historique_emprunts[i]
            if username == self.emprunteur.username and date_retour_init is None:
                self.historique_emprunts[i] = (username, date_emprunt, date_retour)
                break
        self.emprunteur = None
        self.date_limite_retour = None

    def reserver(self, user):
        if user.username in [u.username for u in self.file_attente_reservations]:
            raise Exception("Vous avez déjà réservé ce livre")
        self.file_attente_reservations.append(user)

    def annuler_reservation(self, user):
        try:
            self.file_attente_reservations.remove(user)
        except ValueError:
            raise Exception("Réservation introuvable")

    def livre_disponible_apres_retour(self, notifier=None):
        if self.file_attente_reservations:
            prochain_utilisateur = self.file_attente_reservations.popleft()
            self.emprunteur = prochain_utilisateur
            self.historique_emprunts.append((prochain_utilisateur.username, datetime.now().date(), None))
            if notifier:
                notifier(prochain_utilisateur, f"Le livre '{self.titre}' est disponible pour vous.")
            return prochain_utilisateur
        else:
            self.emprunteur = None
            return None

    def ajouter_avis(self, username, note, commentaire):
        if not (1 <= note <= 5):
            raise Exception("Note doit être entre 1 et 5")
        self.avis.append((username, note, commentaire, datetime.now().date()))

    def moyenne_notes(self):
        if not self.avis:
            return None
        total = sum(note for _, note, _, _ in self.avis)
        return total / len(self.avis)


class LivreNumerique(Livre):
    def __init__(self, titre, auteur, isbn, taille_fichier):
        super().__init__(titre, auteur, isbn)
        self.taille_fichier = taille_fichier

    def to_dict(self):
        base = super().to_dict()
        base["type"] = "Livre Numerique"
        base["taille_fichier"] = self.taille_fichier
        return base


class Exemplaire:
    def __init__(self, id_exemplaire, statut="disponible"):
        self.id_exemplaire = id_exemplaire
        self.statut = statut  # "disponible", "emprunte", "endommage", "perdu"
        self.emprunteur = None


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
        raise LivreNonTrouveErreur(ISBN)

    def recherche_par_titre(self, titre):
        return [livre for livre in self.livres if livre.titre == titre]

    def recherche_par_auteur(self, auteur):
        return [livre for livre in self.livres if livre.auteur.lower() == auteur.lower()]

    def recherche_par_categorie(self, categorie):
        return [livre for livre in self.livres if livre.categorie and livre.categorie.lower() == categorie.lower()]

    def trouver_livre_par_isbn(self, isbn):
        for livre in self.livres:
            if livre.ISBN == isbn:
                return livre
        return None

    def emprunter_livre(self, isbn, user):
        livre = self.trouver_livre_par_isbn(isbn)
        if livre is None:
            raise Exception("Livre non trouvé")
        if not livre.est_disponible():
            raise Exception("Livre déjà emprunté")
        livre.emprunter(user)
        user.emprunter(isbn)

    def retourner_livre(self, isbn, user, notifier=None):
        livre = self.trouver_livre_par_isbn(isbn)
        if livre is None:
            raise Exception("Livre non trouvé")
        if livre.emprunteur != user:
            raise Exception("Vous ne pouvez pas retourner ce livre")
        livre.retourner()
        user.retourner(isbn)
        user.penalites_impayees = user.calculer_penalites()
        livre.livre_disponible_apres_retour(notifier)

    def reserver_livre(self, isbn, user):
        livre = self.trouver_livre_par_isbn(isbn)
        if livre.est_disponible():
            raise Exception("Livre disponible, pas besoin de réserver.")
        user.reserver(isbn)
        livre.reserver(user)

    def recommander_livres(self, user, max_reco=5):
        pref_categories = user.categories_preferees(self)
        livres_recommandes = []
        for cat in pref_categories:
            livres_cat = [livre for livre in self.livres if livre.categorie == cat and livre.est_disponible()]
            livres_recommandes.extend(livres_cat)
            if len(livres_recommandes) >= max_reco:
                break
        return livres_recommandes[:max_reco]

    def livres_populaires(self, top_n=5):
        compte_emprunts = {}
        for livre in self.livres:
            compte_emprunts[livre.ISBN] = len(livre.historique_emprunts)
        sorted_livres = sorted(self.livres, key=lambda l: compte_emprunts[l.ISBN], reverse=True)
        return sorted_livres[:top_n]

    def utilisateurs_actifs(self, user_manager, top_n=5):
        compte_emprunts = []
        for user in user_manager.users:
            compte_emprunts.append((user, len(user.historique_emprunts)))
        compte_emprunts.sort(key=lambda x: x[1], reverse=True)
        return compte_emprunts[:top_n]

class Abonnement:
    def __init__(self, nom, max_emprunts, duree_emprunt_jours, tarif_penalite_par_jour, date_expiration):
        self.nom = nom  # Exemple : "basique", "premium", "VIP"
        self.max_emprunts = max_emprunts
        self.duree_emprunt_jours = duree_emprunt_jours
        self.tarif_penalite_par_jour = tarif_penalite_par_jour
        self.date_expiration = date_expiration  # datetime.date
    def est_valide(self):
        return datetime.now().date() <= self.date_expiration

class User:
    def __init__(self, username, mdp, admin=False, abonnement = None):
        self.username = username
        self.password_hash = hashlib.sha256(mdp.encode()).hexdigest()
        self.is_admin = admin
        self.abonnement = abonnement

        self.emprunts_en_cours = []
        self.historique_emprunts = []
        self.reservations = deque()

        self.loan_count_this_month = 0
        self.last_reset_month = datetime.now().month

        self.penalites_impayees = 0.0
        self.exemplaires = []

        self.abonnement = abonnement if abonnement is not None else Abonnement(
            nom = "basique",
            max_emprunts=1,
            duree_emprunt_jours=14, 
            tarif_penalite_par_jour=0.50,
            date_expiration=datetime.now().date() + timedelta(days=365)
        )

    def check_password(self, mdp):
        return self.password_hash == hashlib.sha256(mdp.encode()).hexdigest()

    def reset_monthly_counter(self):
        current_month = datetime.now().month
        if self.last_reset_month != current_month:
            self.loan_count_this_month = 0
            self.last_reset_month = current_month

    def can_borrow(self):
        if not self.abonnement_valide():
            raise Exception("Abonnement expiré, merci de le renouveler.")
        self.reset_monthly_counter()
        # Utilise la limite d'emprunts de l'abonnement
        return len(self.emprunts_en_cours) < self.abonnement.max_emprunts and self.loan_count_this_month < self.abonnement.max_emprunts

    def emprunter(self, isbn):
        if self.penalites_impayees > 0:
            raise Exception(f"Emprunt impossible : vous avez {self.penalites_impayees:.2f}€ de pénalités impayées.")
        if not self.can_borrow():
            raise Exception("Limite d'emprunts atteinte ou livre déjà emprunté.")
        self.emprunts_en_cours.append(isbn)
        self.loan_count_this_month += 1
        self.historique_emprunts.append((isbn, datetime.now().date(), None))

    def retourner(self, isbn):
        if isbn not in self.emprunts_en_cours:
            raise Exception("Ce livre n'est pas emprunté par cet utilisateur.")
        self.emprunts_en_cours.remove(isbn)
        for i in reversed(range(len(self.historique_emprunts))):
            isbn_hist, date_emprunt, date_retour = self.historique_emprunts[i]
            if isbn_hist == isbn and date_retour is None:
                self.historique_emprunts[i] = (isbn_hist, date_emprunt, datetime.now().date())
                break

    def reserver(self, isbn):
        if isbn in self.reservations:
            raise Exception("Vous avez déjà réservé ce livre.")
        self.reservations.append(isbn)

    def annuler_reservation(self, isbn):
        try:
            self.reservations.remove(isbn)
        except ValueError:
            raise Exception("Réservation non trouvée.")

    def calculer_penalites(self):
        penalites = 0.0
        for isbn, date_emprunt, date_retour in self.historique_emprunts:
            date_fin = date_retour if date_retour else datetime.now().date()
            delta = (date_fin - date_emprunt).days
            retard = delta - self.abonnement.duree_emprunt_jours
            if retard > 0:
                penalites += retard * self.abonnement.tarif_penalite_par_jour
        return penalites

    def peut_emprunter(self, max_loans_per_month=1):
        if self.penalites_impayees > 0:
            return False
        return self.can_borrow(max_loans_per_month)

    def a_emprunte(self, isbn):
        return any(e[0] == isbn for e in self.historique_emprunts)

    def commenter_livre(self, livre, note, commentaire):
        if not self.a_emprunte(livre.ISBN):
            raise Exception("Vous devez avoir emprunté ce livre pour le commenter")
        livre.ajouter_avis(self.username, note, commentaire)

    def categories_preferees(self, bibliotheque):
        categories = {}
        for isbn, *_ in self.historique_emprunts:
            livre = bibliotheque.trouver_livre_par_isbn(isbn)
            if livre and livre.categorie:
                categories[livre.categorie] = categories.get(livre.categorie, 0) + 1
        return sorted(categories, key=categories.get, reverse=True)

    def ajouter_exemplaire(self, id_exemplaire):
        self.exemplaires.append(Exemplaire(id_exemplaire))

    def exemplaire_disponible(self):
        for exemplar in self.exemplaires:
            if exemplar.statut == "disponible":
                return exemplar
        return None

    def emprunter_exemplaire(self, user):
        exemplar = self.exemplaire_disponible()
        if exemplar is None:
            raise Exception("Aucun exemplaire disponible")
        exemplar.statut = "emprunte"
        exemplar.emprunteur = user
        self.emprunteur = user  # Optionnel
        self.historique_emprunts.append((user.username, datetime.now().date(), None))
        return exemplar

    def retourner_exemplaire(self, exemplar):
        exemplar.statut = "disponible"
        exemplar.emprunteur = None
        # Mettre à jour historique, emprunteur...
    
    def abonnement_valide(self):
        return self.abonnement is not None and self.abonnement.est_valide()
    
    def renouveler_abonnement(self, duree_jours=365):
        if self.abonnement is None:
            raise Exception("Aucun abonnement à renouveler.")
        self.abonnement.date_expiration = max(datetime.now().date(), self.abonnement.date_expiration) + timedelta(days=duree_jours)