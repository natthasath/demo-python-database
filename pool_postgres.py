from decouple import config
from postgres.pool import ConnectionPool

host = config("POSTGRES_HOST")
port = config("POSTGRES_PORT")
username = config("POSTGRES_USER")
password = config("POSTGRES_PASS")
database = config("POSTGRES_NAME")

pool = ConnectionPool(5, host, port, database, username, password)

# Create a record
columns = ['name', 'email']
values = ['John Doe', 'john.doe@example.com']
record_id = pool.create_record('users', columns, values)
print(f"Created record with ID {record_id}")

# Read records
columns = ['name', 'email']
where = "name LIKE 'J%'"
order_by = "name ASC"
limit = 10
records = pool.read_records('users', columns, where, order_by, limit)
print(f"Found {len(records)} records matching query")

# Update records
set_dict = {'email': 'newemail@example.com'}
where = "name = 'John Doe'"
num_updated = pool.update_records('users', set_dict, where)
print(f"Updated {num_updated} records")

# Delete records
where = "name LIKE 'J%'"
num_deleted = pool.delete_records('users', where)
print(f"Deleted {num_deleted} records")