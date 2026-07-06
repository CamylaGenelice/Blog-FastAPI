from fastapi import APIRouter, HTTPException, File, UploadFile
from supabase import create_client, Client
import os
import uuid

app = APIRouter(prefix='/images', tags=['images'])

# Puxa as variáveis que a Vercel gerou automaticamente
SUPABASE_URL = os.getenv("ARMAZENAMENTO_IMAGENS_SUPABASE_URL")
SUPABASE_KEY = os.getenv("ARMAZENAMENTO_IMAGENS_SUPABASE_ANON_KEY")

# Inicializa o cliente do Supabase
if SUPABASE_URL and SUPABASE_KEY:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
else:
    # Caso você esteja testando local e esqueceu do arquivo .env
    supabase = None

# Nome do balde (bucket) público que você criou no Supabase
BUCKET_NAME = "imagens"


async def upload_para_supabase(file: UploadFile, pasta_destino: str = 'blog'):
    if not supabase:
        raise HTTPException(status_code=500, detail="Supabase não configurado.")
    try:
        file_bytes = await file.read()
        # Define o caminho e o nome que o arquivo terá dentro do Supabase. Cria uma pasta blog
        # e mantem o nome original do arquivo

        extensao = os.path.splitext(file.filename)[1].lower()
        nome_unico = f'{uuid.uuid4()}{extensao}'
        file_path = f'{pasta_destino}/{nome_unico}'
        supabase.storage.from_(BUCKET_NAME).upload(
            path=file_path,
            file=file_bytes,
            file_options={'content_type': file.content_type}
        )
        # Pega a URL pública permanente gerada pelo Supabase
        url_publica = supabase.storage.from_(BUCKET_NAME).get_public_url(file_path)

        # Retorna a URL para o TinyMCE colocar no meio texto
        return {'url': url_publica}
    except HTTPException as e:
        raise HTTPException(status_code=400, detail=f'Erro ao subir imagem: {str(e)}')


@app.post('/upload')
async def upload_image(file: UploadFile = File(...)):
    url = await upload_para_supabase(file, pasta_destino='blog')
    return {'url': url}