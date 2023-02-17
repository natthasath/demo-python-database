import cx_Oracle

class Oracle:
    def __init__(self, host, port, service_name, user, password, client_library_path):
        cx_Oracle.init_oracle_client(lib_dir=client_library_path)
        self.conn = cx_Oracle.connect(
            user=user,
            password=password,
            dsn=cx_Oracle.makedsn(host, port, service_name=service_name)
        )
        self.cursor = self.conn.cursor()

    def execute(self, query):
        self.cursor.execute(query)
        self.conn.commit()

    def fetch_all(self, query):
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def close(self):
        self.cursor.close()
        self.conn.close()
