from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from queue import Queue
from threading import Lock

class ConnectionPool:
    def __init__(self, max_connections, uri, username, password, database):
        self.max_connections = max_connections
        self.uri = uri
        self.username = username
        self.password = password
        self.database = database
        self.connections = Queue(maxsize=max_connections)
        self.lock = Lock()
        self._create_connections(max_connections)
    
    def _create_connections(self, num_connections):
        for i in range(num_connections):
            self._create_connection()

    def _create_connection(self):
        try:
            client = MongoClient(self.uri)
            db = client[self.database]
            db.authenticate(self.username, self.password)
            self.connections.put(db)
        except ConnectionFailure as e:
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
    
    def create_document(self, collection_name, document):
        conn = self.get_connection()
        result = conn[collection_name].insert_one(document)
        self.release_connection(conn)
        return result.inserted_id
    
    def read_documents(self, collection_name, query):
        conn = self.get_connection()
        result = conn[collection_name].find(query)
        self.release_connection(conn)
        return list(result)
    
    def update_documents(self, collection_name, query, update):
        conn = self.get_connection()
        result = conn[collection_name].update_many(query, update)
        self.release_connection(conn)
        return result.modified_count
    
    def delete_documents(self, collection_name, query):
        conn = self.get_connection()
        result = conn[collection_name].delete_many(query)
        self.release_connection(conn)
        return result.deleted_count
