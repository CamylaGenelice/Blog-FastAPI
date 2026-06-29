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
            if not comentario_criado:
                raise Exception('Post não existe')
            return comentario_criado

        except Exception as e:
            print('Erro ao criar comentário: ',e)
            raise e

    async def deletar_comentario(self, comentario_id: int, usuario_id:int, post_id:int):
        try:
            consulta = await self.repository.buscar_comentario_por_id(comentario_id)
            if not consulta:
                raise HTTPException(status_code=404, detail='Comentário não encontrado')

            is_admin = (usuario_id == 10)

            if not (is_admin or usuario_id):
                raise HTTPException(status_code=403, detail='Sem permissão para deletar')

            await self.repository.deletar_comentario(comentario_id, post_id)

            return {'msg': 'Comentário deletado com sucesso'}

        except Exception as e:
            print("Erro: ",e)
            raise e

    async def buscar_comentarios_detalhados(self, post_id: int):
        try:
            comentarios = await self.repository.buscar_comentarios(post_id)
            if not comentarios:
                raise HTTPException(status_code=404, detail='Esse post ainda não tem comentários')
            return comentarios

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