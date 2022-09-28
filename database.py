from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

host = "localhost"
port = 5432
dbName = "sqlalchemy"
username = "postgres"
password = "Mkr225566"

DATABASE_URI = f'postgresql://{username}:{password}@{host}:{port}/{dbName}'


engine = create_engine(DATABASE_URI)
Session = sessionmaker(bind=engine)

Base = declarative_base()