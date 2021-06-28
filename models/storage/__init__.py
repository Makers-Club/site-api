from models.storage.mysql_client import MySQLClient
from os import getenv


def credentials():

    credentials = {
        'drivername': 'mysql+pymysql',
        'username': getenv('MYSQL_USER'),
        'password': getenv('MYSQL_PWD'),
        'query': None
    }

    if getenv('PRODUCTION'):
        def query():
            socket_directory = '/cloudsql'  # getenv('DB_SOCKET_DIR')
            connection_name = 'maker-teams-site:us-central1:mt-mysql-db' # getenv('DB_CONNECTION_NAME')
            return {'unix_socket': f'{socket_directory}/{connection_name}'}
        credentials['database'] = getenv('MYSQL_PRODUCTION_DB')
        credentials['host'] = ''
        credentials['query'] = query()
    else:
        credentials['database'] = 'development'
        credentials['host'] = 'localhost'
    
    return credentials



mysql_client = MySQLClient(credentials())
mysql_client.reload()

DB = mysql_client