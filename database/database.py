import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from config import mysql_config
# Configuración de la conexión a MySQL
host = mysql_config['host']
port = mysql_config['port']
username = mysql_config['username']
password = mysql_config['password']
database_name = mysql_config['database']

# Crear la URL de conexión a MySQL
database_url = f"mysql+mysqlconnector://{username}:{password}@{host}:{port}/{database_name}"

# Crear el motor de la base de datos
engine = create_engine(database_url, echo=True)

# Crear la sesión
Session = sessionmaker(bind=engine)

# Crear la base de datos declarativa
Base = declarative_base()
