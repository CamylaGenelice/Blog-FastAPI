
from sqlalchemy.ext.asyncio import AsyncSession

from src.model.model import Usuario
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import select, delete, update


class UserQueries():
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


    async def criar_usuario(self, usuario: Usuario):
        obj =  await self._salvar(usuario)
        return obj

    async def atualizar_senha(self, email: str, senha: str):
        try:
            consulta = update(Usuario).where(Usuario.email == email).values(senha=senha)
            resultado = await self.sessao.execute(consulta)
            await self.sessao.commit()
            return resultado.scalars().first()
        except SQLAlchemyError as e:
            await self.sessao.rollback()
            print(f'Erro: ', {e})
            raise e
    async def deletar_usuario(self, id: int):
        try:
            consulta = delete(Usuario).where(Usuario.id == id)
            resultado = await self.sessao.execute(consulta)
            await self.sessao.commit()
            return resultado.scalars()
        except SQLAlchemyError as e:
            await self.sessao.rollback()
            print(f'Erro: ', {e})
            raise e

    async def buscar_usuario(self, email: str):
        try:
            user = select(Usuario).filter(Usuario.email == email)
            result = await self.sessao.execute(user)
            return result.scalars().first()
        except SQLAlchemyError as e:
            await self.sessao.rollback()
            print(f'Erro: ', {e})
            raise e

    async def pegar_hash(self, senha: Usuario):
        try:
            usuario = select(Usuario).filter_by(hash_salvo=senha)
            resultado = await self.sessao.execute(usuario)
            return resultado.scalars().first()
        except SQLAlchemyError as e:
            await self.sessao.rollback()
            print(f'Erro: ', {e})
            raise e

    async def buscar_todos_usuarios(self):
        try:
            user = select(Usuario)
            resultado = await self.sessao.execute(user)
            return resultado.scalars().all()
        except SQLAlchemyError as e:
            await self.sessao.rollback()
            print(f'Erro: ', {e})
            raise e