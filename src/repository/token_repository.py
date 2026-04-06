from sqlalchemy import select, update
from src.model.model import Usuario
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError


class TokenRepository:

    def __init__(self, session: AsyncSession):
        self.session = session


    async def get_token(self, token: str) -> Usuario:
        try:
            obj = select(Usuario).filter(Usuario.token_refresh == token)
            resultado = await self.session.execute(obj)
            return resultado.scalar()

        except SQLAlchemyError as e:
            print("Erro: ",e)
            raise e

    async def salvar_token_refresh(self, email: str, token: str):
        try:

            usuario = (update(Usuario).where(Usuario.email == email).values(token_refresh=token))
            await self.session.execute(usuario)
            await self.session.commit()

        except SQLAlchemyError as e:
            print("Erro ao salvar token: ",e)
            raise e