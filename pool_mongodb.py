from decouple import config
from mongodb.pool import ConnectionPool

host = config("MONGODB_HOST")
port = config("MONGODB_PORT")
username = config("MONGODB_USER")
password = config("MONGODB_PASS")
database = config("MONGODB_NAME")

pool = ConnectionPool(5, f'mongodb://{host}:{port}/', username, password, database)
conn = pool.get_connection()

# Create a document
document = {'name': 'Jane Smith', 'age': 25}
document_id = pool.create_document('users', document)
print(f"Created document with ID {document_id}")

# Read documents
query = {'age': {'$gt': 25}}
documents = pool.read_documents('users', query)
print(f"Found {len(documents)} documents matching query {query}")

# Update documents
query = {'name': 'Jane Smith'}
update = {'$set': {'age': 30}}
num_updated = pool.update_documents('users', query, update)
print(f"Updated {num_updated} documents")

# Delete documents
query = {'age': {'$gte': 40}}
num_deleted = pool.delete_documents('users', query)
print(f"Deleted {num_deleted} documents")

pool.release_connection(conn)