def test_ajout_livre(biblio_vide, livre_exemple):
    biblio_vide.ajouter_livre(livre_exemple)
    assert biblio_vide.livres[0].titre == "1984"

def test_supprimer_livre(biblio_vide, livre_exemple):
    biblio_vide.ajouter_livre(livre_exemple)
    biblio_vide.supprimer_livre("ISBN123")
    assert len(biblio_vide.livres) == 0

def test_ajout_livre_numerique(biblio_vide, livre_num_exemple):
    biblio_vide.ajouter_livre(livre_num_exemple)
    assert biblio_vide.livres[0].taille_fichier == "2MB"