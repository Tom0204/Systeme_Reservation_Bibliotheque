from src.file_manager import BibliothequeAvecFichier
from src.models import Livre, Bibliotheque

def test_sauvegarde_et_chargement(tmp_path):
    fichier = tmp_path / "save_test.json"
    biblio = Bibliotheque("Test")
    biblio.ajouter_livre(Livre("TestLivre", "Auteur", "ISBNX"))
    manager = BibliothequeAvecFichier(biblio)
    manager.sauvegarder(fichier)
    assert fichier.exists()

    biblio2 = Bibliotheque("Vide")
    manager2 = BibliothequeAvecFichier(biblio2)
    manager2.charger(fichier)
    assert biblio2.livres[0].titre == "TestLivre"

def test_export_csv(tmp_path):
    fichier = tmp_path / "export.csv"
    biblio = Bibliotheque("Test")
    biblio.ajouter_livre(Livre("TestLivre", "Auteur", "ISBNY"))
    manager = BibliothequeAvecFichier(biblio)
    manager.export_csv(fichier)
    assert fichier.exists()