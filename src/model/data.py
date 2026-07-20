from os import replace
from urllib.parse import urlparse, parse_qsl, urlencode, urlunparse
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.declarative import declarative_base
import os
from dotenv import load_dotenv

load_dotenv()

vercel_url = os.getenv("ARMAZENA_DADOS_POSTGRES_URL")
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_host = os.getenv("DB_HOST")
db_port = os.getenv("DB_PORT")
db_name = os.getenv("DB_NAME")

# verifica se a conexão com o banco de dados esta rodando no localhost ou no vercel
# existem 2 bancos de dados, um na nuvem e outro local

if vercel_url.startswith("postgres://"):
    DATABASE_URL = vercel_url.replace(
        "postgres://",
        "postgresql+asyncpg://",
        1
    )
elif vercel_url.startswith("postgresql://"):
    DATABASE_URL = vercel_url.replace(
        "postgresql://",
        "postgresql+asyncpg://",
        1
    )
else:
    DATABASE_URL = f"postgresql+asyncpg://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"

print(DATABASE_URL)
engine = create_async_engine(DATABASE_URL, echo=True, connect_args={'ssl': 'require'})
Base = declarative_base()


