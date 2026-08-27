import pytest
from mediatheque.mediatheque import Mediatheque
from mediatheque.documents import Livre, DVD
from mediatheque.erreurs import (
    DocumentIndisponible,
    TropDEmprunts,
    DocumentInconnu,
    MediathequeError,
)


# Tests obligatoires (6 minimum)


def test_emprunt_rend_le_document_indisponible():
    """Test 1 : un emprunt rend le document indisponible.
    Test 2 : un second emprunt sur le même document lève DocumentIndisponible."""
    media = Mediatheque("Test")
    livre = Livre("Titre", 2020, "L001", auteur="X", nb_pages=100)
    media.ajouter_document(livre)
    awa = media.inscrire("Awa")

    media.emprunter(awa.numero, "L001")

    assert not livre.disponible
    with pytest.raises(DocumentIndisponible):
        media.emprunter(awa.numero, "L001")


def test_quatrieme_emprunt_leve_trop_demprunts():
    """Test 3 : un adhérent ne peut pas emprunter plus de 3 documents."""
    media = Mediatheque("Test")
    awa = media.inscrire("Awa")

    for i in range(4):
        livre = Livre(f"Livre {i}", 2020, f"L00{i}", auteur="X", nb_pages=100)
        media.ajouter_document(livre)

    for i in range(3):
        media.emprunter(awa.numero, f"L00{i}")

    with pytest.raises(TropDEmprunts):
        media.emprunter(awa.numero, "L003")


def test_rendre_remet_le_document_en_circulation():
    """Test 4 : rendre un document le remet disponible."""
    media = Mediatheque("Test")
    livre = Livre("Titre", 2020, "L001", auteur="X", nb_pages=100)
    media.ajouter_document(livre)
    awa = media.inscrire("Awa")

    media.emprunter(awa.numero, "L001")
    assert not livre.disponible

    media.rendre(awa.numero, "L001")
    assert livre.disponible


def test_duree_pret_livre_et_dvd():
    """Test 5 : duree_pret() vaut 21 pour un livre, 7 pour un DVD."""
    livre = Livre("Titre", 2020, "L001", auteur="X", nb_pages=100)
    dvd = DVD("Titre", 2020, "D001", realisateur="Y", duree_min=90)

    assert livre.duree_pret() == 21
    assert dvd.duree_pret() == 7


def test_rechercher_est_insensible_a_la_casse():
    """Test 6 : rechercher trouve un document malgré la casse."""
    media = Mediatheque("Test")
    livre = Livre("L'Aventure ambiguë", 1961, "L001", auteur="X", nb_pages=100)
    media.ajouter_document(livre)

    resultats = media.rechercher("aventure")
    assert len(resultats) == 1
    assert resultats[0] == livre

    resultats = media.rechercher("AVENTURE")
    assert len(resultats) == 1
    assert resultats[0] == livre


# Tests supplémentaires (au-delà des 6 obligatoires)


def test_emprunter_document_inconnu_leve_exception():
    """Test 7 : emprunter un code inconnu lève DocumentInconnu."""
    media = Mediatheque("Test")
    awa = media.inscrire("Awa")

    with pytest.raises(DocumentInconnu):
        media.emprunter(awa.numero, "X001")


def test_rendre_document_non_emprunte_leve_exception():
    """Test 8 : rendre un document que l'adhérent n'a pas emprunté lève MediathequeError."""
    media = Mediatheque("Test")
    livre = Livre("Titre", 2020, "L001", auteur="X", nb_pages=100)
    media.ajouter_document(livre)
    awa = media.inscrire("Awa")
    # Awa n'a pas emprunté L001

    with pytest.raises(MediathequeError):
        media.rendre(awa.numero, "L001")


def test_emprunter_avec_adherent_inconnu_leve_exception():
    """Test 9 : emprunter avec un numéro d'adhérent inconnu lève MediathequeError."""
    media = Mediatheque("Test")
    livre = Livre("Titre", 2020, "L001", auteur="X", nb_pages=100)
    media.ajouter_document(livre)
    # Aucun adhérent inscrit

    with pytest.raises(MediathequeError):
        media.emprunter("Z999", "L001")


def test_rendre_avec_adherent_inconnu_leve_exception():
    """Test 10 : rendre avec un adhérent inconnu lève MediathequeError."""
    media = Mediatheque("Test")
    livre = Livre("Titre", 2020, "L001", auteur="X", nb_pages=100)
    media.ajouter_document(livre)

    with pytest.raises(MediathequeError):
        media.rendre("Z999", "L001")


def test_documents_disponibles_retourne_seulement_disponibles():
    """Test 11 : documents_disponibles ne retourne que les documents non empruntés."""
    media = Mediatheque("Test")
    livre1 = Livre("L1", 2020, "L001", auteur="X", nb_pages=100)
    livre2 = Livre("L2", 2020, "L002", auteur="Y", nb_pages=200)
    media.ajouter_document(livre1)
    media.ajouter_document(livre2)
    awa = media.inscrire("Awa")
    media.emprunter(awa.numero, "L001")

    dispo = media.documents_disponibles()
    assert len(dispo) == 1
    assert dispo[0] == livre2


def test_emprunts_de_retourne_la_liste_des_emprunts():
    """Test 12 : emprunts_de retourne les emprunts d'un adhérent."""
    media = Mediatheque("Test")
    livre1 = Livre("L1", 2020, "L001", auteur="X", nb_pages=100)
    livre2 = Livre("L2", 2020, "L002", auteur="Y", nb_pages=200)
    media.ajouter_document(livre1)
    media.ajouter_document(livre2)
    awa = media.inscrire("Awa")
    media.emprunter(awa.numero, "L001")
    media.emprunter(awa.numero, "L002")

    emprunts = media.emprunts_de(awa.numero)
    assert len(emprunts) == 2
    assert livre1 in emprunts
    assert livre2 in emprunts


def test_emprunter_apres_avoir_rendu_est_possible():
    """Test 13 : après avoir rendu, on peut ré-emprunter le même document."""
    media = Mediatheque("Test")
    livre = Livre("Titre", 2020, "L001", auteur="X", nb_pages=100)
    media.ajouter_document(livre)
    awa = media.inscrire("Awa")

    media.emprunter(awa.numero, "L001")
    media.rendre(awa.numero, "L001")
    media.emprunter(awa.numero, "L001")  # ne doit pas lever d'exception
    assert not livre.disponible


def test_str_des_documents():
    """Test 14 : vérifier que les __str__ des documents sont corrects."""
    livre = Livre("Titre", 2020, "L001", auteur="X", nb_pages=100)
    dvd = DVD("Film", 2021, "D001", realisateur="Y", duree_min=120)

    assert str(livre) == 'Livre "Titre" (2020) - disponible, auteur : X - à rendre sous 21 jours'
    assert str(dvd) == 'DVD "Film" (2021) - disponible, réalisateur : Y - à rendre sous 7 jours'


def test_eq_des_documents():
    """Test 15 : deux documents avec le même code sont égaux."""
    livre1 = Livre("Titre A", 2020, "L001", auteur="X", nb_pages=100)
    livre2 = Livre("Titre B", 2021, "L001", auteur="Y", nb_pages=200)
    dvd = DVD("Film", 2020, "D001", realisateur="Z", duree_min=90)

    assert livre1 == livre2  # même code
    assert livre1 != dvd
    assert livre1 != "une chaîne"