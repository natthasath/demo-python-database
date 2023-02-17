import psycopg2

class PostgreSQL:
    def __init__(self, host, port, database, user, password):
        self.conn = psycopg2.connect(
            host=host,
            port=port,
            database=database,
            user=user,
            password=password
        )
        self.cursor = self.conn.cursor()

    def execute(self, query, args=None):
        self.cursor.execute(query, args)
        self.conn.commit()

    def fetch_all(self, query, args=None):
        self.cursor.execute(query, args)
        return self.cursor.fetchall()

    def close(self):
        self.cursor.close()
        self.conn.close()