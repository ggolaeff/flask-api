from sqlalchemy import create_engine

DB_USER = 'postgres'
DB_PASSWORD = '2718281828'
DB_HOST = 'localhost'
DB_PORT = '5432'
DB_NAME = 'projects_db'

db_string = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

engine = create_engine(db_string)


