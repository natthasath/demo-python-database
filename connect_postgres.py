from decouple import config
from postgres.postgres import PostgreSQL

host = config("POSTGRES_HOST")
port = config("POSTGRES_PORT")
username = config("POSTGRES_USER")
password = config("POSTGRES_PASS")
database = config("POSTGRES_NAME")

postgresql = PostgreSQL(host, port, database, username, password)
postgresql.execute("CREATE TABLE users (id SERIAL PRIMARY KEY, name VARCHAR(50), age INTEGER)")
postgresql.execute("INSERT INTO users (name, age) VALUES (%s, %s)", ("Alan Turing", 30))
rows = postgresql.fetch_all("SELECT * FROM users")
for row in rows:
    print(row)
postgresql.close()