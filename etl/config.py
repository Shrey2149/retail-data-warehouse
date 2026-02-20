from sqlalchemy import create_engine

DB_CONFIG = {
    "username": "postgres",
    "password": "shreythegreat",
    "host": "localhost",
    "port": "5432",
    "database": "retail_dw"
}

def get_engine():
    return create_engine(
        f"postgresql+psycopg2://{DB_CONFIG['username']}:{DB_CONFIG['password']}@"
        f"{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}"
    )