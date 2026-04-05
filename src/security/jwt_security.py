from fastapi.responses import JSONResponse
from jose import jwt, JWTError, ExpiredSignatureError
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import AsyncSession
from src.repository.token_repository import TokenRepository
import os
load_dotenv()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")
SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = os.getenv('ALGORITHM')
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv('EXPIRE_MINUTES'))



class JwtSecurity:
    def __init__(self, session: AsyncSession):
        self.repository = TokenRepository(session)

    def create_access_token(self, data: dict):
        to_encode = data.copy()

        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

        to_encode.update({"exp": expire,  "scope": "access" })

        encode_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encode_jwt

    def create_refresh_token(self,data: dict):
        expire = datetime.now(timezone.utc) + timedelta(days=2)
        to_encode = data.copy()
        to_encode.update({"exp": expire, "scope": "refresh"})
        token_refresh =  jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return token_refresh

    async def verify_refresh_token(self,token: str):

        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            token = await self.repository.get_token(token)

            if token is None:
                return {"mensagem": "Token não existe"}
            if payload.get("scope") != "refresh":
                return {"error": "Token inválido"}
            return token

        except ExpiredSignatureError:
            return {"error": "Refresh token expirado. Faça login novamente."}
        except JWTError as e:
            print('Erro: ',e)
            return {"error": "Token inválido."}

    async def verify_access_token(self, token: str):
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            # expire = payload.get("exp")
            #
            # if expire and datetime.fromtimestamp(expire) < datetime.now():
            #     raise Exception("Token expirado")

            return payload
        except ExpiredSignatureError:
            print("Token expirado")
            return None
        except JWTError as e:
            print('Erro: ',e)
            raise e

    async def save_token(self, email: str, token: str):
        try:
             objeto = await self.repository.salvar_token_refresh(email, token)
             return objeto
        except Exception as e:
            print('Erro: ',e)
            raise e


