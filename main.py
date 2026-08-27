from mediatheque.mediatheque import Mediatheque
from mediatheque.documents import Livre, DVD
from mediatheque.erreurs import (
    MediathequeError,
    DocumentIndisponible,
    TropDEmprunts,
    DocumentInconnu,
)


def afficher_separateur(titre: str = ""):
    """Affiche un séparateur pour la lisibilité."""
    print("\n" + "=" * 60)
    if titre:
        print(f" {titre} ".center(60, "="))
    else:
        print("=" * 60)


def main():
    # 1. Création de la médiathèque
    mediatheque = Mediatheque("Médiathèque de Dakar")
    print(f"Bienvenue à la {mediatheque.nom}\n")

    # 2. Ajout de nombreux documents (livres et DVD)
    documents_ajoutes = [
        Livre("L'Aventure ambiguë", 1961, "L001",
              auteur="Cheikh Hamidou Kane", nb_pages=191),
        Livre("Une si longue lettre", 1979, "L002",
              auteur="Mariama Bâ", nb_pages=163),
        Livre("Les soleils des indépendances", 1968, "L003",
              auteur="Ahmadou Kourouma", nb_pages=208),
        Livre("Xala", 1973, "L004",
              auteur="Sembène Ousmane", nb_pages=176),
        Livre("L'Enfant noir", 1953, "L005",
              auteur="Camara Laye", nb_pages=224),
        DVD("Camp de Thiaroye", 1988, "D001",
            realisateur="Sembène Ousmane", duree_min=147),
        DVD("Moolaadé", 2004, "D002",
            realisateur="Sembène Ousmane", duree_min=124),
        DVD("Timbuktu", 2014, "D003",
            realisateur="Abderrahmane Sissako", duree_min=97),
        DVD("Atlantique", 2019, "D004",
            realisateur="Mati Diop", duree_min=104),
    ]

    for doc in documents_ajoutes:
        mediatheque.ajouter_document(doc)

    print(f"{len(documents_ajoutes)} documents ont été ajoutés à la médiathèque.")

    # 3. Inscription de plusieurs adhérents
    adherants = [
        mediatheque.inscrire("Awa Diop"),
        mediatheque.inscrire("Mamadou Diallo"),
        mediatheque.inscrire("Fatou Sow"),
        mediatheque.inscrire("Ibrahima Ndiaye"),
    ]

    print(f"\n{len(adherants)} adhérents inscrits :")
    for adh in adherants:
        print(f"  - {adh.nom} (n°{adh.numero})")

    # 4. Affichage de l'ensemble des documents avec leur disponibilité
    afficher_separateur("État initial des documents")
    for doc in mediatheque.tous_les_documents():
        statut = "Disponible" if doc.disponible else "Emprunté"
        print(f"{doc} - {statut}")

    # 5. Emprunts par Awa (3 emprunts)
    afficher_separateur("Awa emprunte 3 documents")
    awa = adherants[0]
    emprunts_awa = ["L001", "D001", "L003"]
    for code in emprunts_awa:
        doc = mediatheque.emprunter(awa.numero, code)
        print(f"Awa a emprunté : {doc} (rendre sous {doc.duree_pret()} jours)")

    print(f"\nAwa a maintenant {len(awa)} emprunts :")
    for doc in awa.emprunts_en_cours():
        print(f"  - {doc}")

    # 6. Tentative d'emprunt d'un document déjà emprunté (par Awa)
    afficher_separateur("Tentative d'emprunt d'un document indisponible")
    try:
        mediatheque.emprunter(awa.numero, "L001")
    except DocumentIndisponible as err:
        print(f"Erreur : {err}")

    # 7. Tentative d'emprunt d'un document inconnu
    try:
        mediatheque.emprunter(awa.numero, "X999")
    except DocumentInconnu as err:
        print(f"Erreur : {err}")

    # 8. Mamadou emprunte 2 documents
    afficher_separateur("Mamadou emprunte 2 documents")
    mamadou = adherants[1]
    mediatheque.emprunter(mamadou.numero, "L002")
    mediatheque.emprunter(mamadou.numero, "D002")
    print("Mamadou a emprunté :")
    for doc in mamadou.emprunts_en_cours():
        print(f"  - {doc}")

    # 9. Fatou essaie d'emprunter 4 documents (test de la limite)
    afficher_separateur("Test de la limite de 3 emprunts (Fatou)")
    fatou = adherants[2]
    codes_fatou = ["L004", "L005", "D003", "D004"]  # 4 documents
    for i, code in enumerate(codes_fatou, 1):
        try:
            doc = mediatheque.emprunter(fatou.numero, code)
            print(f"Fatou a emprunté : {doc}")
        except TropDEmprunts as err:
            print(f"Erreur pour le {i}e emprunt : {err}")
            break
        except MediathequeError as err:
            print(f"Autre erreur : {err}")
    print(f"Fatou a finalement {len(fatou)} emprunts.")

    # 10. Restitution d'un document par Awa
    afficher_separateur("Awa rend un document (L001)")
    mediatheque.rendre(awa.numero, "L001")
    print("Awa a rendu 'L'Aventure ambiguë'.")
    print(f"Ce document est maintenant disponible : {mediatheque.obtenir_document('L001').disponible}")
    print(f"Awa a maintenant {len(awa)} emprunts.")

    # 11. Ibrahima emprunte le document rendu
    afficher_separateur("Ibrahima emprunte le document rendu")
    ibrahima = adherants[3]
    doc = mediatheque.emprunter(ibrahima.numero, "L001")
    print(f"Ibrahima a emprunté : {doc}")

    # 12. Recherche de documents par mot-clé (insensible à la casse)
    afficher_separateur("Recherche par mot-clé")
    mots_recherche = ["aventure", "soleil", "sembène", "thiaroye"]
    for mot in mots_recherche:
        resultats = mediatheque.rechercher(mot)
        print(f"Recherche '{mot}' : {len(resultats)} résultat(s)")
        for doc in resultats:
            print(f"  - {doc}")

    # 13. Affichage des documents disponibles (polymorphisme à l'œuvre)
    afficher_separateur("Documents actuellement disponibles")
    disponibles = mediatheque.documents_disponibles()
    if disponibles:
        for doc in disponibles:
            print(doc)  # __str__ de Livre ou DVD appelé automatiquement
    else:
        print("Aucun document disponible.")

    # 14. Affichage des emprunts de chaque adhérent
    afficher_separateur("Récapitulatif des emprunts par adhérent")
    for adh in adherants:
        print(f"{adh.nom} (n°{adh.numero}) : {len(adh)} emprunt(s)")
        for doc in adh.emprunts_en_cours():
            print(f"  - {doc} (à rendre sous {doc.duree_pret()} jours)")

    # 15. Tentative de rendre un document non emprunté (gestion d'erreur)
    afficher_separateur("Tentative de restitution d'un document non emprunté")
    try:
        mediatheque.rendre(awa.numero, "D004")  # Awa n'a pas D004
    except ValueError:
        print("Erreur : Awa n'a pas emprunté ce document.")
    except MediathequeError as err:
        print(f"Erreur : {err}")

    print("\nFin de la démonstration.")


if __name__ == "__main__":
    main()