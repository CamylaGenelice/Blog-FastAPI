from pydantic import BaseModel
from typing import Optional

class PostSchema(BaseModel):
    titulo: str
    texto: str

    class Config:
        from_attributes = True

class EditarPostSchema(BaseModel):
    titulo: Optional[str] = None
    texto: Optional[str] = None

    class Config:
        from_attributes= True

class ResponseCreatePostSchema(BaseModel):
    mensagem: str
    objeto_titulo: str
    objeto_texto: str
    objeto_imagem: Optional[str] = None
    code: int

    class Config:
        from_attributes= True

class ResponseUpdatePostSchema():
    mensagem: str
    class Config:
        from_attributes= True

class GetPostSchema(BaseModel):

    id: int
    titulo: str
    conteudo: str
    autor_id: int

    class Config:
        from_attributes= True
