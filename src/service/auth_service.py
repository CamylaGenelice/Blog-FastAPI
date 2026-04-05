
import bcrypt
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.schemas.user_schemas import UserSchema,DeleteUserSchema
from src.security.jwt_security import JwtSecurity

from src.utils.validation import (validar_nome, validar_senha, validar_email)
from src.model.model import Usuario
from src.repository.user_repository import UserQueries

class User():
    def __init__(self, session: AsyncSession):

        self.repository = UserQueries(session)
        self.session = session
        self.security = JwtSecurity(session)


    async def criar_usuario(self, dados: UserSchema):
        try:
            if not validar_nome(dados.nome):
                raise Exception('Nome inválido')
            if not validar_senha(dados.senha):
                raise Exception('Senha inválida')
            if not validar_email(dados.email):
                raise Exception('Email inválido')

            usuario_existe = await self.repository.buscar_usuario(dados.email)
            if  usuario_existe:
                raise Exception('Email já esta em uso')

            senha_bytes = dados.senha.encode()
            senha_hash = bcrypt.hashpw(senha_bytes, bcrypt.gensalt(10)).decode('utf-8')

            novo_usuario = Usuario(dados.nome, dados.email, senha_hash)
            obj = await self.repository.criar_usuario(novo_usuario)
            return obj

        except Exception as e:
            print('Erro Service: ',e)
            raise e

    async def deletar_usuario(self,usuario: DeleteUserSchema, id: int):


        try:
            if usuario.role_id != 2:
                return {"mensagem": "Usuário não tem permissão "}

            usuario = await self.repository.deletar_usuario(id)

            if usuario == 0:
                raise Exception("Usuário não encontrado")
            return {"mensagem": 'Usuário removido com sucesso'}
        except Exception as e:
            print('Erro: ',e)
            raise e

    async def login_usuario(self, email: str, senha: str):
        try:

            objeto = await self.repository.buscar_usuario(email)

            if objeto is None:
                raise HTTPException (status_code=400, detail='Usuario não encontrado')

            senha_correta = bcrypt.checkpw(senha.encode('utf-8'), objeto.senha.encode('utf-8'))

            if not senha_correta:
                raise HTTPException (status_code=400, detail='Dados incorretos')

            payload = {"sub": str(objeto.id), "role_id": objeto.role_id}
            access_token = self.security.create_access_token(payload)
            refresh_token = self.security.create_refresh_token(payload)
            await self.security.save_token(email, refresh_token)

            return {
                'access_token': access_token,
                'refresh_token': refresh_token,
                'token_type': 'bearer'
            }

        except Exception as e:
            print('Erro no login: ',e)
            raise e

    async def atualizar_senha(self, email: str, senha: str):
        try:
            objeto = await self.repository.buscar_usuario(email)
            if objeto is None:
                raise Exception ('Usuario não encontrado')

            senha_bytes = senha.encode()
            senha_hash = bcrypt.hashpw(senha_bytes, bcrypt.gensalt(10)).decode('utf-8')

            objeto_usuario = self.repository.atualizar_senha(email,senha_hash)
            return objeto_usuario

        except Exception as e:
            raise Exception('Erro ao atualizar senha: ',e)

    async def buscar_todos_usuarios(self):
        try:
            usuarios = await self.repository.buscar_todos_usuarios()
            return usuarios
        except Exception as e:
            print('Erro: ', e)
            raise e