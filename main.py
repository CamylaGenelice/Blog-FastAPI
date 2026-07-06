#uvicorn serve:app --reload
import os
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from supabase import create_client, Client

app = FastAPI(title='Meu Blog API')
load_dotenv()

SUPABASE_URL = os.getenv("ARMAZENAMENTO_IMAGENS_SUPABASE_URL")
SUPABASE_KEY = os.getenv('ARMAZENAMENTO_IMAGENS_SUPABASE_ANON_KEY')

if SUPABASE_URL and SUPABASE_KEY:
    supabase: Client = create_client(SUPABASE_URL,SUPABASE_KEY)
else:
    raise RuntimeError('As variáveis de ambiente do Supabase não foram encontradas.')

BUCKET_NAME = 'imagens'

origins = [
        "https://meu-front.vercel.app",
        "http://localhost:5500",
        "http://127.0.0.1:5500",
 ]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
    max_age=3600,
)

from src.routes.auth_routes import auth_router
from src.routes.posts_routes import post_router
from src.routes.comments_routes import comments_router
from src.routes.upload_images import upload_image_router

app.include_router(auth_router)
app.include_router(post_router)
app.include_router(comments_router)
app.include_router(upload_image_router)

@app.get("/")
def root():
    return {"mensagem": "API do Portfólio funcionando!"}

