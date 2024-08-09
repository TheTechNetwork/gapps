import os
import pytest
import time
import psycopg2

def wait_for_postgres(host, port, user, password, dbname, retries=30, delay=1):
    for i in range(retries):
        try:
            conn = psycopg2.connect(
                host=host,
                port=port,
                user=user,
                password=password,
                dbname=dbname
            )
            conn.close()
            return True
        except psycopg2.OperationalError as e:
            print(f"Waiting for PostgreSQL to be ready... ({i+1}/{retries})")
            print(f"Error: {e}")
            time.sleep(delay)
    raise Exception("PostgreSQL is not ready after several attempts")

@pytest.fixture(scope='session', autouse=True)
def wait_for_db():
    host = os.getenv('POSTGRES_HOST', 'localhost')  # Use the resolved container name
    port = 5432
    user = 'myuser'
    password = 'mypassword'
    dbname = 'mydatabase'
    
    print(f"Postgres connection details - Host: {host}, Port: {port}, User: {user}, Password: {password}, DB: {dbname}")
    
    wait_for_postgres(host, port, user, password, dbname)

@pytest.fixture(scope='session')
def db_url():
    host = os.getenv('POSTGRES_HOST', 'localhost')
    db_url = f"postgresql://myuser:mypassword@{host}:5432/mydatabase"
    print(f"DB URL: {db_url}")
    return db_url

@pytest.fixture(scope='session')
def app(db_url):
    from app import create_app  # Adjust the import according to your app's structure
    app = create_app({
        'SQLALCHEMY_DATABASE_URI': db_url,
        'TESTING': True,
    })
    return app