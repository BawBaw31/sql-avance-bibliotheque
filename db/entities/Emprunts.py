import datetime

from psycopg2 import DatabaseError

from ..Database import Database
from .Membres import Membres


class Emprunts():
    # id: int
    # id_membre: int
    # isbn: int
    # date_emprunt: datetime.date
    # date_rendu: datetime.date | None

    # def __init__(self, id, id_membre, isbn, date_emprunt, date_rendu) -> None:
    #     self.id = id
    #     self.id_membre = id_membre
    #     self.isbn = isbn
    #     self.date_emprunt = date_emprunt
    #     self.date_rendu = date_rendu

    @staticmethod
    def mes_emprunts(membre: Membres, db: Database):
        try:
            print(membre.id)
            db.cur.execute(
                "SELECT id, isbn, date_emprunt, quantite FROM emprunts WHERE id_membre = %s AND date_rendu IS NULL", (membre.id,))
            return db.cur.fetchall()
        except (Exception, DatabaseError) as error:
            db.conn.rollback()
            raise error

    @staticmethod
    def mon_historique(membre: Membres, db: Database):
        try:
            print(membre.id)
            db.cur.execute(
                "SELECT id, isbn, date_emprunt, date_rendu, quantite FROM emprunts WHERE id_membre = %s AND date_rendu IS NOT NULL", (membre.id,))
            return db.cur.fetchall()
        except (Exception, DatabaseError) as error:
            db.conn.rollback()
            raise error

    @staticmethod
    def emprunts_encours(db: Database):
        try:
            db.cur.execute(
                "SELECT id, id_membre, isbn, date_emprunt, quantite FROM emprunts WHERE date_rendu IS NULL")
            return db.cur.fetchall()
        except (Exception, DatabaseError) as error:
            db.conn.rollback()
            raise error
        
    @staticmethod
    def rendre_livre(id: int, db: Database):
        try:
            db.cur.execute(
                "UPDATE emprunts SET date_rendu = %s WHERE id = %s", (datetime.date.today(), id))
            db.cur.execute(
                "UPDATE livres SET quantite_disponible = quantite_disponible + (SELECT quantite FROM emprunts WHERE id = %s) WHERE isbn = (SELECT isbn FROM emprunts WHERE id = %s)", (id, id))
            db.conn.commit()
        except (Exception, DatabaseError) as error:
            db.conn.rollback()
            raise error
