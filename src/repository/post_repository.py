from sqlalchemy import delete, update

from src.model.model import Posts
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError
class PostRepository:

    def __init__(self, sessao: AsyncSession):
        self.sessao = sessao


    async def _salvar(self, objeto):
      try:
        self.sessao.add(objeto)
        await self.sessao.commit()
        await self.sessao.refresh(objeto)
        return objeto
      except SQLAlchemyError as e:
         await self.sessao.rollback()
         print(f'Erro: ', {e})
         raise e


    async def criar_post(self, post: Posts):
        return await self._salvar(post)

    async def alterar_post(self, id: int, titulo: str, texto: str):

        try:
            objeto_update = update(Posts).where(Posts.id == id).values(titulo=titulo, conteudo=texto)
            await self.sessao.execute(objeto_update)
            await self.sessao.commit()


        except SQLAlchemyError as e:
            await self.sessao.rollback()
            print(f'Erro: ', {e})
            raise e

    async def buscar_posts(self):
        try:
            obj = select(Posts)
            resultado = await self.sessao.execute(obj)
            return resultado.scalars().all()
        except SQLAlchemyError as e:
            await self.sessao.rollback()
            print(f'Erro: ', {e})
            raise e

    async def deletar_post(self, id: int):
        try:
            obj = delete(Posts).where(Posts.id == id)
            await self.sessao.execute(obj)
            await self.sessao.commit()
        except SQLAlchemyError as e:
            await self.sessao.rollback()
            print(f'Erro: ', {e})
            raise e

    async def buscar_post(self, id:int):
        try:
            objeto_select = select(Posts).where(Posts.id == id)
            objeto_execute = await self.sessao.execute(objeto_select)
            return objeto_execute.scalars().first()

        except SQLAlchemyError as e:
            await self.sessao.rollback()
            print(f'Erro: ', {e})
            raise e