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
            print('Erro ao criar comentário: ',e)
            raise e

    async def deletar_comentario(self, id: int, usuario_id:int):
        try:
            comentario = await self.repository.deletar_comentario(id, usuario_id)
            if comentario is None:
                raise Exception('Erro ao deletar comentário: Comentário is None')
            return comentario
        except Exception as e:
            print("Erro: ",e)
            raise e

    async def buscar_comentarios_detalhados(self, post_id: int):
        try:
            comentarios = await self.repository.buscar_comentarios(post_id)
            if not comentarios:
                raise Exception('Este post ainda não tem comentários.')

        except Exception as e:
            print("Erro ao buscar comentários: ",e)
            raise e

    async def editar_comentario(self, id: int, usuario:int ,texto:str):
        try:
            objeto_comentario = await self.repository.editar_comentario(id,usuario, texto)
            return objeto_comentario
        except Exception as e:
            print("Erro ao editar comentario ",e)
            raise e