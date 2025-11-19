# file_manager
import json
import csv
from src.models import Livre, LivreNumerique
from src.exceptions import ErreurBibliotheque

class BibliothequeAvecFichier:
    def __init__(self, bibliotheque):
        self.bibliotheque = bibliotheque
    
    def sauvegarder(self, filepath):
        try:
            data = [livre.to_dict() for livre in self.bibliotheque.livres]
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            raise ErreurBibliotheque(f"Erreur lors de la sauvegarde : {e}")

    def charger(self, filepath):
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
            self.bibliotheque.livres.clear()
            for livre_dic in data:
                if livre_dic["type"] == "LivreNumerique":
                    livre = LivreNumerique(livre_dic["titre"], livre_dic["auteur"], livre_dic["ISBN"], livre_dic["taille_fichier"])
                else:
                    livre = Livre(livre_dic["titre"], livre_dic["auteur"], livre_dic["ISBN"])
                self.bibliotheque.livres.append(livre)
        except FileNotFoundError:
            raise ErreurBibliotheque(f"Fichier '{filepath}' inexistant.")
        except json.JSONDecodeError:
            raise ErreurBibliotheque("Format JSON invalide.")
        except Exception as e:
            raise ErreurBibliotheque(f"Erreur lors du chargement : {e}")

    def export_csv(self, filepath):
        try:
            with open(filepath, "w", encoding="utf-8", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["type", "titre", "auteur", "ISBN", "taille_fichier"])
                for livre in self.bibliotheque.livres:
                    d = livre.to_dict()
                    writer.writerow([d["type"], d["titre"], d["auteur"], d["ISBN"], d.get("taille_fichier", "")])
        except IOError:
            raise ErreurBibliotheque("Permissions insuffisantes ou chemin inaccessible.")
        except Exception as e:
            raise ErreurBibliotheque(f"Erreur lors de l'export CSV : {e}")