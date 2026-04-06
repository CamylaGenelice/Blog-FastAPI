#uvicorn serve:app --reload
import os
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title='Meu Blog API')
load_dotenv()
def get_cors_origins():

    if os.getenv("ENVIRONMENT") == "development" or not os.getenv("RENDER"):
        return [
            "http://localhost:3000",
            "http://localhost:5500",
            "http://127.0.0.1:5500",
            "http://localhost:8000",
        ]
    frontend_url = os.getenv("FRONTEND_URL")

    origins = []

    if frontend_url:
        origins.append(frontend_url)

    render_url = os.getenv("RENDER_EXTERNAL_URL")
    if render_url:
        origins.append(render_url)

    if not origins:
        render_hostname = os.getenv("RENDER_HOSTNAME")
        if render_hostname:
            origins.append(f"https://{render_hostname}")

    return origins if origins else ["https://meudominio.onrender.com"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=get_cors_origins(),
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

