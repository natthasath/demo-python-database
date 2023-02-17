from decouple import config
from oracle.oracle import Oracle

host = config("ORACLE_HOST")
port = config("ORACLE_PORT")
username = config("ORACLE_USER")
password = config("ORACLE_PASS")
database = config("ORACLE_NAME")
instant_client = config("ORACLE_INSTANT_CLIENT")

oracle = Oracle(host, port, database, username, password, instant_client)
oracle.execute("CREATE TABLE users (id NUMBER PRIMARY KEY, name VARCHAR2(50), age NUMBER)")
oracle.execute("INSERT INTO users (id, name, age) VALUES (1, 'Alan Turing', 30)")
rows = oracle.fetch_all("SELECT * FROM users")
for row in rows:
    print(row)
oracle.close()