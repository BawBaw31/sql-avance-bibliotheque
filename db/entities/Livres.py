
import datetime

from psycopg2 import DatabaseError

from .Membres import Membres

from ..Database import Database


class Livres:
    isbn: int
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

    def ajouter_livres(self, db: Database):
        try:
            db.cur.execute(
                "INSERT INTO livres VALUES (%s,%s,%s, %s, %s, %s, %s)", (self.ISBN, self.titre, self.quantite_disponible, self.auteur,
                                                                         self.edition, self.date_parution, self.nom_categorie))
            db.conn.commit()
        except (Exception, DatabaseError) as error:
            db.conn.rollback()
            raise error

    @staticmethod
    def afficher_livres(db: Database, auteur: str = '', categorie: str = '', annee: int = 0):
        try:
            if annee:
                db.cur.execute("SELECT * FROM livres WHERE auteur LIKE %s AND nom_categorie LIKE %s AND date_parution BETWEEN to_date('%s-01-01','YYYY-MM-DD') AND to_date('%s-12-31','YYYY-MM-DD')",
                               (f'%{auteur}%', f'%{categorie}%', annee, annee))
            else:
                db.cur.execute("SELECT * FROM livres WHERE auteur LIKE %s AND nom_categorie LIKE %s",
                               (f'%{auteur}%', f'%{categorie}%'))
            return db.cur.fetchall()
        except (Exception, DatabaseError) as error:
            db.conn.rollback()
            raise error

    @staticmethod
    def emprunter_livres(db: Database, membre: Membres, isbn: int, quantite: int = 1):
        try:
            db.cur.execute("SELECT * FROM livres WHERE isbn = %s", (isbn,))
            livre = db.cur.fetchone()
            if livre[2] >= quantite:
                db.cur.execute("INSERT INTO emprunts (id_membre, isbn, date_emprunt, quantite) VALUES (%s, %s, %s, %s)",
                               (membre.id, isbn, datetime.date.today(), quantite))
                db.cur.execute("UPDATE livres SET quantite_disponible = %s WHERE isbn = %s",
                               (livre[2] - quantite, isbn))
                db.conn.commit()
            else:
                raise Exception("Quantité insuffisante")
        except (Exception, DatabaseError) as error:
            db.conn.rollback()
            raise error