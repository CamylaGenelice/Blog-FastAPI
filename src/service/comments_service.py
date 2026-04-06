from fastapi import HTTPException

from src.model.model import Comentarios
from src.repository.comment_repository import CommentRepository
from sqlalchemy.ext.asyncio import AsyncSession
class CommentsService:

    def __init__(self, session:AsyncSession ):
        self.session = session
        self.repository = CommentRepository(session)



    async def criar_comentario(self,dados: Comentarios ):
        try:

            comentario_criado =  await self.repository.criar_comentario(dados)
            return comentario_criado

        except Exception as e:
            print(e)
            raise e

    async def deletar_comentario(self, id: int):
        try:
            objeto_busca = await self.buscar_comentario(id)
            if not objeto_busca:
                raise Exception('Comentario não encontrado')
            comentario = await self.repository.deletar_comentario(id)
            return comentario

        except Exception as e:
            print("Erro: ",e)
            raise e

    async def buscar_comentario(self, id: int):
        try:
            comentario = await self.repository.buscar_comentario(id)
            if not comentario:
                raise Exception('Comentario não encontrado')
            return comentario
        except Exception as e:
           # print("Erro ao buscar comentario ",e)
            raise e

    async def editar_comentario(self, id: int, texto:str):
        try:
            consulta = await self.repository.buscar_comentario(id)
            if not consulta:
                raise Exception('Comentario não encontrado')
            objeto_comentario = await self.repository.editar_comentario(id, texto)
            return objeto_comentario
        except Exception as e:
            print("Erro ao editar comentario ",e)
            raise e