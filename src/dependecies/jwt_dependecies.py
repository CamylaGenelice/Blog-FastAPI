
from fastapi import HTTPException, Depends, Cookie
from jose import JWTError
import os
from dotenv import load_dotenv
from typing import Annotated

from src.dependecies.session import pegar_sessao
from src.security.jwt_security import JwtSecurity
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

load_dotenv()


SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = os.getenv('ALGORITHM')


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

async def current_user(access_token: Annotated[str | None, Cookie()] = None, session: AsyncSession = Depends(pegar_sessao)):
    try:

            if not access_token:
                raise HTTPException(status_code=401, detail="Token não encontrado nos cookies")

            token = access_token.replace('Bearer', '')

            security = JwtSecurity(session)

            payload = await security.verify_access_token(token)

            if payload is None:
                raise HTTPException(status_code=401, detail="Erro ao validar token")
            return payload


    except JWTError as e:
            print('Erro: ', e)
            raise HTTPException(status_code=401, detail=str(e))


async def check_admin_roler(user: dict = Depends(current_user)):
    try:
        if user.get('role_id') != 2:
            raise HTTPException(status_code=403, detail='Acesso Negado')
        if user.get('scope') != 'access':
            raise HTTPException(status_code=403, detail='Token invalido')
        return user
    except JWTError as e:
        print('Erro: ', e)
        raise e

async def get_me(user: dict = Depends(current_user)):
    try:
        """
            Retorna os dados do usuário autenticado baseando-se no Cookie/Token.
            Se o usuário não estiver logado, a dependência 'current_user' 
            já retornará 401 automaticamente.
        """
        # 'user' aqui é o payload decodificado da função current_user
        return {
            "id": user.get('sub'),
            'role_id': user.get('role_id'),
        }
    except Exception as e:
        raise HTTPException(status_code=403, detail=str(e))
