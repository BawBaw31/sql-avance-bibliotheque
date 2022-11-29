import datetime

import psycopg2

from .entities.Livres import Livres

from .config import config
from .entities.Membres import Membres


class Database:
    def __init__(self):
        self.conn = self.connect()
        self.cur = self.conn.cursor()

    def connect(self):
        """ Connect to the PostgreSQL database server """
        conn = None
        try:
            # read connection parameters
            params = config()

            # connect to the PostgreSQL server
            print('Connecting to the PostgreSQL database...')
            conn = psycopg2.connect(**params)

            # create a cursor
            cur = conn.cursor()

            # execute a statement
            print('PostgreSQL database version:')
            cur.execute('SELECT version()')

            # display the PostgreSQL database server version
            db_version = cur.fetchone()
            print(db_version)

            # close the communication with the PostgreSQL
            cur.close()
            return conn
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    def close_connection(self):
        self.cur.close()
        self.conn.close()

    def login(self, nom: str):
        try:
            self.cur.execute("SELECT * FROM membres WHERE nom = %s", (nom,))
            membre = Membres(*self.cur.fetchone())
            self.cur.execute(
                "SELECT * FROM roles WHERE id_membre = %s", (membre.id,))
            for role in self.cur.fetchall():
                membre.roles.append(role[0])
            print(self.cur.fetchall())
            return membre
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    def creer_membre(self, nom: str, date_de_naissance: datetime.date):
        try:
            self.cur.execute("INSERT INTO membres (nom, date_de_naissance, peut_emprunter) VALUES (%s, %s, %s) RETURNING id",
                             (nom, date_de_naissance, True))
            self.cur.execute("INSERT INTO roles (role, id_membre) VALUES (%s, %s)",
                             ("emprunteur", self.cur.fetchone()[0]))
            self.conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            self.conn.rollback()
            raise error

    def ajouter_livres(self, livres: list[Livres]):
        values = map(lambda x: (x.ISBN, x.titre, x.auteur,
                     x.date_parution, x.edition, x.nom_categorie), livres)
        try:
            args = ','.join(self.cur.mogrify("(%s,%s,%s, %s, %s, %s, %s)", i).decode('utf-8')
                            for i in values)
            self.cur.execute(
                "INSERT INTO livres (isbn, titre, auteur, date_parution, quantite_disponible, edition, nom_categorie) VALUES " + args)
            self.conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            self.conn.rollback()
            raise error
