from src.models import Livre, LivreNumerique, Bibliotheque
from src.file_manager import BibliothequeAvecFichier
from src.exceptions import ErreurBibliotheque

def main():
    livre1 = Livre("1984", "George Orwell", "ISBN123")
    livre2 = Livre("Les Misérables", "Victor Hugo", "ISBN456")
    livre3 = Livre("Le Petit Prince", "Antoine de Saint-Exupéry", "ISBN789")
    livre4 = LivreNumerique("Digital Fortress", "Dan Brown", "ISBN101", "2MB")

    biblio = Bibliotheque("La Bible aux Tchèques")
    biblio.ajouter_livre(livre1)
    biblio.ajouter_livre(livre2)
    biblio.ajouter_livre(livre3)
    biblio.ajouter_livre(livre4)

    manager = BibliothequeAvecFichier(biblio)

    try:
        manager.sauvegarder("data/bib.json")
        manager.export_csv("data/catalogue.csv")
        manager.charger("data/bib.json")
    except ErreurBibliotheque as e:
        print(f"Erreur gérée : {e}")

if __name__ == "__main__":
    main()