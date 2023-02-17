from decouple import config
from mongodb.mongodb import MongoDB

host = config("MONGODB_HOST")
port = config("MONGODB_PORT")
username = config("MONGODB_USER")
password = config("MONGODB_PASS")
database = config("MONGODB_NAME")

mongodb = MongoDB(host, port, database, "users", username, password)
document = {"name": "Alan", "surname": "Turing"}
mongodb.insert_document(document)
docs = mongodb.find_all_documents()
for doc in docs:
    print(doc)
mongodb.close()