from os import replace

from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.declarative import declarative_base
import os
from dotenv import load_dotenv

load_dotenv()

vercel_url = os.getenv("ARMAZENA_DADOS_POSTGRES_URL")

# Converte para o driver assíncrono (asyncpg) de forma segura
if not vercel_url:
    raise ValueError("A variável ARMAZENA_DADOS_POSTGRES_URL não foi encontrada nas variáveis de ambiente!")

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
    DATABASE_URL = vercel_url



engine = create_async_engine(DATABASE_URL, echo=True, connect_args={'ssl': 'require'})
Base = declarative_base()


