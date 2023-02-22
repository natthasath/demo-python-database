import psycopg2
import queue
import threading

class ConnectionPool:
    def __init__(self, max_connections, host, port, dbname, username, password):
        self.max_connections = max_connections
        self.host = host
        self.port = port
        self.dbname = dbname
        self.username = username
        self.password = password
        self.connections = queue.Queue(maxsize=max_connections)
        self.lock = threading.Lock()
        self._create_connections(max_connections)
    
    def _create_connections(self, num_connections):
        for i in range(num_connections):
            self._create_connection()

    def _create_connection(self):
        try:
            conn = psycopg2.connect(
                host=self.host,
                port=self.port,
                dbname=self.dbname,
                user=self.username,
                password=self.password
            )
            self.connections.put(conn)
        except Exception as e:
            print(f"Failed to create connection: {e}")
    
    def get_connection(self):
        connection = None
        if self.connections.qsize() > 0:
            connection = self.connections.get()
        else:
            with self.lock:
                if self.connections.qsize() < self.max_connections:
                    self._create_connection()
                    connection = self.connections.get()
        return connection
    
    def release_connection(self, connection):
        self.connections.put(connection)
    
    def create_record(self, table_name, columns, values):
        conn = self.get_connection()
        cursor = conn.cursor()
        placeholders = ','.join(['%s'] * len(values))
        query = f"INSERT INTO {table_name} ({','.join(columns)}) VALUES ({placeholders})"
        cursor.execute(query, values)
        record_id = cursor.fetchone()[0]
        conn.commit()
        cursor.close()
        self.release_connection(conn)
        return record_id
    
    def read_records(self, table_name, columns=None, where=None, order_by=None, limit=None):
        conn = self.get_connection()
        cursor = conn.cursor()
        if not columns:
            columns = ['*']
        query = f"SELECT {','.join(columns)} FROM {table_name}"
        if where:
            query += f" WHERE {where}"
        if order_by:
            query += f" ORDER BY {order_by}"
        if limit:
            query += f" LIMIT {limit}"
        cursor.execute(query)
        records = cursor.fetchall()
        cursor.close()
        self.release_connection(conn)
        return records
    
    def update_records(self, table_name, set_dict, where):
        conn = self.get_connection()
        cursor = conn.cursor()
        set_clause = ','.join([f"{k} = %s" for k in set_dict])
        values = list(set_dict.values())
        query = f"UPDATE {table_name} SET {set_clause} WHERE {where}"
        cursor.execute(query, values)
        num_updated = cursor.rowcount
        conn.commit()
        cursor.close()
        self.release_connection(conn)
        return num_updated
    
    def delete_records(self, table_name, where):
        conn = self.get_connection()
        cursor = conn.cursor()
        query = f"DELETE FROM {table_name} WHERE {where}"
        cursor.execute(query)
        num_deleted = cursor.rowcount
        conn.commit()
        cursor.close()
        self.release_connection(conn)
        return num_deleted
