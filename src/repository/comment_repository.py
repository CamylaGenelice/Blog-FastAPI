from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import select, delete, update
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

    async def buscar_comentario(self, id: int):
        try:
            consulta = select(Comentarios).filter(Comentarios.id == id)
            resultado = await self.session.execute(consulta)
            return resultado.scalars().first()
        except SQLAlchemyError as e:
            await self.session.rollback()
            print('Erro: ', e)
            raise e


    async def editar_comentario(self, id: int, texto:str):
        try:
            objeto_update = update(Comentarios).where(Comentarios.id == id).values(texto=texto)
            await self.session.execute(objeto_update)
            await self.session.commit()


        except SQLAlchemyError as e:
            await self.session.rollback()
            print('Erro: ', e)
            raise e

    async def deletar_comentario(self, id: int):
        try:
            consulta = delete(Comentarios).where(Comentarios.id == id)
            await self.session.execute(consulta)
            await self.session.commit()


        except SQLAlchemyError as e:
            await self.session.rollback()
            print('Erro: ', e)
            raise e