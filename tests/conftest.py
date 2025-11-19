import pytest
from src.models import Livre, LivreNumerique, Bibliotheque

@pytest.fixture
def biblio_vide():
    return Bibliotheque("BiblioTest")

@pytest.fixture
def livre_exemple():
    return Livre("1984", "Orwell", "ISBN123")

@pytest.fixture
def livre_num_exemple():
    return LivreNumerique("Python Book", "Dan Brown", "ISBN789", "2MB")