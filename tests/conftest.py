import pytest
import time
import psycopg2
import os

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
            time.sleep(delay)
    raise Exception("PostgreSQL is not ready after several attempts")

@pytest.fixture(scope='session', autouse=True)
def wait_for_db():
    host = os.getenv('POSTGRES_HOST', 'localhost')
    port = int(os.getenv('POSTGRES_PORT', 5432))
    user = os.getenv('POSTGRES_USER', 'myuser')
    password = os.getenv('POSTGRES_PASSWORD', 'mypassword')
    dbname = os.getenv('POSTGRES_DB', 'mydatabase')
    wait_for_postgres(host, port, user, password, dbname)

@pytest.fixture(scope='session')
def db_url():
    return f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB')}"

@pytest.fixture(scope='session')
def app(db_url):
    from app import create_app  # Adjust the import according to your app's structure
    app = create_app({
        'SQLALCHEMY_DATABASE_URI': db_url,
        'TESTING': True,
    })
    return app
