import pymongo

class MongoDB:
    def __init__(self, host, port, database, collection, username, password):
        self.client = pymongo.MongoClient(f"mongodb://{username}:{password}@{host}:{port}/")
        self.db = self.client[database]
        self.collection = self.db[collection]

    def insert_document(self, document):
        self.collection.insert_one(document)

    def find_all_documents(self):
        return list(self.collection.find({}))

    def close(self):
        self.client.close()