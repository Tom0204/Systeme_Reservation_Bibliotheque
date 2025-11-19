# exceptions

class ErreurBibliotheque(Exception):
    def __init__(self, message="Une erreur de bibliothèque s'est produite."):
        self.message = message
        super().__init__(self.message)

class LivreNonTrouveErreur(ErreurBibliotheque):
    def __init__(self, ISBN):
        self.message = f"Livre avec l'ISBN '{ISBN}' non trouvé."
        super().__init__(self.message)