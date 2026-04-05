from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.declarative import declarative_base
import os
from dotenv import load_dotenv



load_dotenv()

db_user = os.getenv("USER")
db_password = os.getenv("PASSWORD")
db_host = os.getenv("HOST")
db_port = os.getenv("PORT")
db_name = os.getenv("NAME")

DATABASE_URL = f"postgresql+asyncpg://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"

engine = create_async_engine(DATABASE_URL, echo=True)
Base = declarative_base()


