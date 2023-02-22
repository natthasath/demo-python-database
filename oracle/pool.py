import cx_Oracle
import threading
from queue import Queue

class OracleConnectionPool:
    def __init__(self, username, password, dsn, min_connections=1, max_connections=10):
        self.username = username
        self.password = password
        self.dsn = dsn
        self.min_connections = min_connections
        self.max_connections = max_connections
        self._connections = Queue(maxsize=max_connections)
        self._lock = threading.Lock()

    def _create_connection(self):
        connection = cx_Oracle.connect(self.username, self.password, self.dsn)
        return connection

    def _initialize_pool(self):
        for _ in range(self.min_connections):
            connection = self._create_connection()
            self._connections.put(connection)

    def get_connection(self):
        if not self._connections.full() and self._connections.qsize() == 0:
            with self._lock:
                if self._connections.qsize() == 0:
                    self._initialize_pool()
        return self._connections.get()

    def return_connection(self, connection):
        self._connections.put(connection)

    def execute_query(self, query, bind_vars=None):
        with self.get_connection() as connection:
            cursor = connection.cursor()
            if bind_vars:
                cursor.execute(query, bind_vars)
            else:
                cursor.execute(query)
            rows = cursor.fetchall()
            cursor.close()
            return rows

    def execute_update(self, query, bind_vars=None):
        with self.get_connection() as connection:
            cursor = connection.cursor()
            if bind_vars:
                cursor.execute(query, bind_vars)
            else:
                cursor.execute(query)
            connection.commit()
            cursor.close()

    def execute_insert(self, table_name, column_values):
        columns = ', '.join(column_values.keys())
        values = tuple(column_values.values())
        placeholders = ', '.join([':%d' % (i+1) for i in range(len(values))])
        query = 'INSERT INTO %s (%s) VALUES (%s)' % (table_name, columns, placeholders)
        self.execute_update(query, values)

    def execute_update_row(self, table_name, column_values, primary_key):
        updates = ', '.join(['%s=:%d' % (col, i+1) for i, col in enumerate(column_values.keys())])
        query = 'UPDATE %s SET %s WHERE %s' % (table_name, updates, primary_key)
        values = tuple(column_values.values())
        self.execute_update(query, values)

    def execute_delete(self, table_name, primary_key):
        query = 'DELETE FROM %s WHERE %s' % (table_name, primary_key)
        self.execute_update(query)
