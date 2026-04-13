from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import select, delete, update
from sqlalchemy.orm import joinedload

from src.model.model import Comentarios
from sqlalchemy.ext.asyncio import AsyncSession

class CommentRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def _salvar(self, objeto):
        try:
           self.session.add(objeto)
           await self.session.commit()
           await self.session.refresh(objeto)
           return objeto
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise e



    async def criar_comentario(self, comentario: Comentarios):
        return await self._salvar(comentario)

    async def buscar_comentarios(self, id: int):
        try:
            # Monta a consulta para buscar todos os comentários de um post específico,
            # carregando também o autor relacionado (joinedload) para evitar consultas extras.
            consulta = ((select(Comentarios)
                        .options(joinedload(Comentarios.autor_id)))
                        .filter(Comentarios.post_id == id))
            resultado = await self.session.execute(consulta)
            return resultado.scalars().all()

        except SQLAlchemyError as e:
            await self.session.rollback()
            raise e


    async def editar_comentario(self, id: int, usuario_id:int, texto:str):
        try:
            # Buscando o comentário filtrando pelo id e pelo dono.
            consulta = select(Comentarios).filter(Comentarios.id == id, Comentarios.autor_id == usuario_id)
            resultado = await self.session.execute(consulta)
            comentario = resultado.scalar_one_or_none() # Retorna o objeto ou None

            if not comentario:
                return None

            comentario.texto = texto
            await self.session.commit()
            await self.session.refresh(comentario)
            return comentario

        except SQLAlchemyError as e:
            await self.session.rollback()
            print('Erro: ', e)
            raise e

    async def deletar_comentario(self, id: int, usuario_id:int):
        try:
            consulta = select(Comentarios).filter(Comentarios.id == id, Comentarios.autor_id == usuario_id)
            resultado = await self.session.execute(consulta)
            comentario = resultado.scalar()

            if not comentario:
                return None

            delete(Comentarios).where(Comentarios.id == id)
            await self.session.commit()



        except SQLAlchemyError as e:
            await self.session.rollback()
            print('Erro: ', e)
            raise e