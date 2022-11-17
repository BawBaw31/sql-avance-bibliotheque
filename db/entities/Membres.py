import datetime


class Membres(object):
    id: int
    nom: str
    date_de_naissance: datetime.date
    peut_emprunter: bool
    roles: list[str] = []

    def __init__(self, id, nom, date_de_naissance, peut_emprunter=True) -> None:
        self.id = id
        self.nom = nom
        self.date_de_naissance = date_de_naissance
        self.peut_emprunter = peut_emprunter