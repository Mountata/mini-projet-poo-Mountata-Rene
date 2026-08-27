from mediatheque.documents import Livre, DVD

l = Livre("L'Aventure ambiguë", 1961, "L001", auteur="Cheikh Hamidou Kane", nb_pages=191)
print(l)
print(l.duree_pret())

d = DVD("Camp de Thiaroye", 1988, "D001", realisateur="Sembene Ousmane", duree_min=147)
print(d)
print(d.duree_pret())

from mediatheque.erreurs import MediathequeError, DocumentIndisponible, TropDEmprunts, DocumentInconnu

try:
    raise DocumentIndisponible("L001")
except MediathequeError as e:
    print("Erreur attrapée :", e)

try:
    raise TropDEmprunts("A001")
except MediathequeError as e:
    print("Erreur attrapée :", e)