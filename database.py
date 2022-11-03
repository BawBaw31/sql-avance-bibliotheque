import datetime
import psycopg2

# Connect to an existing database
conn = psycopg2.connect("dbname=bibliotheque user=postgres")

# Open a cursor to perform database operations
cur = conn.cursor()

# Execute a command: this creates a new table
# cur.execute("CREATE TABLE test (id serial PRIMARY KEY, num integer, data varchar);")

# Pass data to fill a query placeholders and let Psycopg perform
# the correct conversion (no more SQL injections!)
cur.execute("INSERT INTO membres (nom, date_de_naissance, peut_emprunter) VALUES (%s, %s, %s)",
            ("John", datetime.date(1990, 1, 1), True))
# Query the database and obtain data as Python objects
cur.execute("SELECT * FROM membres;")
membres = cur.fetchone()
print(membres)

# Make the changes to the database persistent
conn.commit()

# Close communication with the database
cur.close()
conn.close()
