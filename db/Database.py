import datetime
import psycopg2
from .config import config


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

    def creer_membre(self, nom: str, date_de_naissance: tuple[int, int, int], peut_emprunter: bool):
        try:
            self.cur.execute("INSERT INTO membres (nom, date_de_naissance, peut_emprunter) VALUES (%s, %s, %s)",
                             (nom, datetime.date(date_de_naissance), peut_emprunter))
            self.cur.execute("INSERT INTO roles (role, id_membre) VALUES (%s, %s)",
                             ("emprunteur", self.cur.fetchone()[0]))
            self.conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            self.conn.rollback()

    def test(self):
        print("test")
