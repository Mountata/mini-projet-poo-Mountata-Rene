from .erreurs import DocumentIndisponible, DocumentInconnu, MediathequeError


class Mediatheque:
    """Gère les documents, les adhérents et les prêts."""

    def __init__(self, nom):
        self.nom = nom
        self._documents = {}   # code -> Document
        self._adherents = {}   # numero -> Adherent
        self._compteur_adherents = 0

    def ajouter_document(self, document):
        self._documents[document.code] = document

    def inscrire(self, nom):
        from .adherent import Adherent
        self._compteur_adherents += 1
        numero = f"A{self._compteur_adherents:03d}"
        adherent = Adherent(nom, numero)
        self._adherents[numero] = adherent
        return adherent

    def _get_document(self, code):
        if code not in self._documents:
            raise DocumentInconnu(code)
        return self._documents[code]

    def _get_adherent(self, numero):
        if numero not in self._adherents:
            raise MediathequeError(f"Adhérent inconnu : {numero}")
        return self._adherents[numero]

    def emprunter(self, numero, code):
        document = self._get_document(code)
        adherent = self._get_adherent(numero)

        if not document.disponible:
            raise DocumentIndisponible(code)

        adherent.emprunter(document)
        document.disponible = False
        return document

    def rendre(self, numero, code):
        document = self._get_document(code)
        adherent = self._get_adherent(numero)

        adherent.rendre(document)
        document.disponible = True
        return document

    def rechercher(self, mot):
        mot = mot.lower()
        return [
            doc for doc in self._documents.values()
            if mot in doc.titre.lower()
        ]

    def documents_disponibles(self):
        return [doc for doc in self._documents.values() if doc.disponible]

    def emprunts_de(self, numero):
        adherent = self._get_adherent(numero)
        return adherent.emprunts_en_cours()

    def __str__(self):
        return f"Médiathèque {self.nom} ({len(self._documents)} documents, {len(self._adherents)} adhérents)"
    def obtenir_document(self, code):
        """Retourne le document correspondant au code (accès public, sûr)."""
        return self._get_document(code)

    def tous_les_documents(self):
        """Retourne la liste de tous les documents (disponibles ou non)."""
        return list(self._documents.values())