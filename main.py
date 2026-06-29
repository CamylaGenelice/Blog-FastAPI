#uvicorn serve:app --reload
import os
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

app = FastAPI(title='Meu Blog API')
load_dotenv()

UPLOAD_DIR = 'uploads_images'

if not os.path.exists(UPLOAD_DIR):
    os.mkdir(UPLOAD_DIR)

# Diz ao FastAPI para servir os arquivos da pasta uploads_images
# na URL http://127.0.0.1:8000/static/.
app.mount("/static",StaticFiles(directory=UPLOAD_DIR), name="static")

origins = [
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

app.include_router(auth_router)
app.include_router(post_router)
app.include_router(comments_router)

@app.get("/")
def root():
    return {"mensagem": "API do Portfólio funcionando!"}

