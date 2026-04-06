from pydantic import BaseModel
from typing import Optional

class PostSchema(BaseModel):
    titulo: str
    texto: str

    class Config:
        from_attributes = True

class EditarPostSchema(BaseModel):
    id: int
    titulo: Optional[str] = None
    conteudo: Optional[str] = None

    class Config:
        from_attributes= True

class ResponseCreatePostSchema(BaseModel):
    mensagem: str
    objeto_titulo: str
    objeto_texto: str
    code: int

    class Config:
        from_attributes= True

class ResponseUpdatePostSchema(ResponseCreatePostSchema):

    class Config:
        from_attributes= True

class GetPostSchema(BaseModel):

    id: int
    titulo: str
    conteudo: str
    autor_id: int

    class Config:
        from_attributes= True
