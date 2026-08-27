from abc import ABC, abstractmethod


class Document(ABC):
    """Classe de base abstraite pour tous les documents de la médiathèque."""

    def __init__(self, titre, annee, code):
        self._titre = titre
        self._code = code
        self.annee = annee
        self.disponible = True

    @property
    def titre(self):
        return self._titre

    @property
    def code(self):
        return self._code

    @abstractmethod
    def duree_pret(self):
        """Nombre de jours de prêt autorisé. Dépend du type de document."""
        pass

    def __str__(self):
        etat = "disponible" if self.disponible else "emprunté"
        return f'"{self._titre}" ({self.annee}) - {etat}'

    def __eq__(self, other):
        if not isinstance(other, Document):
            return NotImplemented
        return self._code == other._code

class Livre(Document):
    """Un livre : prêté pour 21 jours."""

    def __init__(self, titre, annee, code, auteur, nb_pages):
        super().__init__(titre, annee, code)
        self.auteur = auteur
        self.nb_pages = nb_pages

    def duree_pret(self):
        return 21

    def __str__(self):
        base = super().__str__()
        return f"Livre {base}, auteur : {self.auteur} - à rendre sous {self.duree_pret()} jours"


class DVD(Document):
    """Un DVD : prêté pour 7 jours."""

    def __init__(self, titre, annee, code, realisateur, duree_min):
        super().__init__(titre, annee, code)
        self.realisateur = realisateur
        self.duree_min = duree_min

    def duree_pret(self):
        return 7

    def __str__(self):
        base = super().__str__()
        return f"DVD {base}, réalisateur : {self.realisateur} - à rendre sous {self.duree_pret()} jours"