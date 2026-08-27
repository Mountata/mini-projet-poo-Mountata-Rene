class MediathequeError(Exception):
    """Classe de base pour toutes les erreurs de la médiathèque."""
    pass


class DocumentIndisponible(MediathequeError):
    """Levée quand on tente d'emprunter un document déjà emprunté."""

    def __init__(self, code):
        self.code = code
        message = f"Le document {code} est déjà emprunté."
        super().__init__(message)


class TropDEmprunts(MediathequeError):
    """Levée quand un adhérent tente d'emprunter un 4e document."""

    def __init__(self, numero_adherent, maximum=3):
        self.numero_adherent = numero_adherent
        self.maximum = maximum
        message = (
            f"L'adhérent {numero_adherent} a déjà atteint "
            f"le maximum de {maximum} emprunts."
        )
        super().__init__(message)


class DocumentInconnu(MediathequeError):
    """Levée quand on cherche un document par un code qui n'existe pas."""

    def __init__(self, code):
        self.code = code
        message = f"Aucun document ne correspond au code {code}."
        super().__init__(message)