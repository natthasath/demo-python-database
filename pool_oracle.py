from decouple import config
from oracle.pool import OracleConnectionPool

host = config("ORACLE_HOST")
port = config("ORACLE_PORT")
username = config("ORACLE_USER")
password = config("ORACLE_PASS")
database = config("ORACLE_NAME")
instant_client = config("ORACLE_INSTANT_CLIENT")

oracle_pool = OracleConnectionPool(username, password, database)

rows = oracle_pool.execute_query('SELECT * FROM my_table')
oracle_pool.execute_insert('my_table', {'col1': 'value1', 'col2': 'value2'})
oracle_pool.execute_update_row('my_table', {'col1': 'new_value'}, 'id=1')
oracle_pool.execute_delete('my_table', 'id=1')