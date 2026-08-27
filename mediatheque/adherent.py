from .erreurs import TropDEmprunts

MAX_EMPRUNTS = 3


class Adherent:
    """Un adhérent de la médiathèque."""

    def __init__(self, nom, numero):
        self.nom = nom
        self.numero = numero
        self._emprunts = []

    def emprunter(self, document):
        if len(self) >= MAX_EMPRUNTS:
            raise TropDEmprunts(self.numero, MAX_EMPRUNTS)
        self._emprunts.append(document)

    def rendre(self, document):
        self._emprunts.remove(document)

    def emprunts_en_cours(self):
        return list(self._emprunts)

    def __len__(self):
        return len(self._emprunts)

    def __str__(self):
        return f"{self.nom} (n°{self.numero}) - {len(self)} emprunt(s) en cours"