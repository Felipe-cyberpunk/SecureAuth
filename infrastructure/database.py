import pyodbc
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

def get_connection():
    connection_string = (
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=localhost,1433;"
        "DATABASE=SecureAuthDB;"
        "UID=sTu_usuario;"
        "PWD=Tu_contraseña"
        "TrustServerCertificate=yes;"
    )
    return pyodbc.connect(connection_string, timeout=30)



# Defi∫nimos la base declarativa que tus modelos necesitan importar
Base = declarative_base()

# Configuramos el motor usando el conector nativo de pyodbc
engine = create_engine(
    "mssql+pyodbc://", 
    creator=get_connection,
    connect_args={},
    isolation_level="READ COMMITTED"
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)