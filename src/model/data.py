from os import replace
from urllib.parse import urlparse, parse_qsl, urlencode, urlunparse
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.declarative import declarative_base
import os
from dotenv import load_dotenv

load_dotenv()

vercel_url = os.getenv("ARMAZENA_DADOS_POSTGRES_URL")
DATABASE_URL = str

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



engine = create_async_engine(DATABASE_URL, echo=True, connect_args={'ssl': 'require'})
Base = declarative_base()


