
import datetime


class Livres:
    ISBN: int
    titre: str
    quantite_disponible: int
    auteur: str
    edition: str
    date_parution: datetime.date
    nom_categorie: str

    def __init__(self, ISBN: int, titre: str, auteur: str, edition: str, date_parution: datetime.date,
                 nom_categorie: str, quantite_disponible: int = 1) -> None:
        self.ISBN = ISBN
        self.titre = titre
        self.auteur = auteur
        self.edition = edition
        self.date_parution = date_parution
        self.nom_categorie = nom_categorie
        self.quantite_disponible = quantite_disponible
