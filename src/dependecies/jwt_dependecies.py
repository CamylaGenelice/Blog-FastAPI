
from fastapi import HTTPException, Depends
from jose import JWTError
import os
from dotenv import load_dotenv
from src.dependecies.session import pegar_sessao
from src.security.jwt_security import JwtSecurity
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = os.getenv('ALGORITHM')


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

async def current_user(token: str = Depends(oauth2_scheme), session: AsyncSession = Depends(pegar_sessao)):
    try:

            security = JwtSecurity(session)

            payload = await security.verify_access_token(token)

            if payload is None:
                raise HTTPException(status_code=401, detail="Token Invalido")
            return payload


    except JWTError as e:
            print('Erro: ', e)
            raise e


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
