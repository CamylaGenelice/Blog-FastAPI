from pydantic import BaseModel, Field, computed_field
from typing import List

class CommentSchema(BaseModel):

    texto: str

    class Config:
        from_attributes = True


class ComentarioFormatado(BaseModel):
    id_comentario: int = Field(alias="id")  # Mapeia 'id' do banco para 'id_comentario'
    texto: str
    post_id: int

    # Aqui está o segredo: pegamos o ID e o Nome de dentro do objeto autor
    # Mas entregamos como campos de primeiro nível
    @computed_field
    @property
    def id_usuario(self) -> int:
        return self.autor.id

    @computed_field
    @property
    def nome_usuario(self) -> str:
        return self.autor.nome

    # Precisamos declarar o autor aqui para o Pydantic ler do SQLAlchemy,
    # mas o 'exclude=True' faz ele NÃO aparecer no JSON final
    autor: object = Field(exclude=True)

    class Config:
        from_attributes = True
        populate_by_name = True

class ResponseCommentsSchema(BaseModel):
   content: List[ComentarioFormatado]

class DeleteSchema(BaseModel):
    id:int

    class Config:
        from_attributes = True

class EditSchema(BaseModel):
    id: int
    texto: str

    class Config:
        from_attributes = True