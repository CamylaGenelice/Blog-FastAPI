from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.declarative import declarative_base
import os
from dotenv import load_dotenv

load_dotenv()

vercel_url = os.getenv("ARMAZENA_DADOS_POSTGRES_URL")
db_user = os.getenv("USER")
db_password = os.getenv("PASSWORD")
db_host = os.getenv("HOST")
db_port = os.getenv("PORT")
db_name = os.getenv("NAME")

# verifica se a conexão com o banco de dados esta rodando no localhost ou no vercel
# existem 2 bancos de dados, um na nuvem e outro local

if vercel_url:
    DATABASE_URL = vercel_url.replace('postgres://', 'postgresql+asyncpg://')

else:
    DATABASE_URL = f"postgresql+asyncpg://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"

engine = create_async_engine(DATABASE_URL, echo=True)
Base = declarative_base()


