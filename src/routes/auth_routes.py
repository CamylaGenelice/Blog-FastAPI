from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from starlette.responses import JSONResponse

from src.dependecies.jwt_dependecies import current_user, check_admin_roler


from src.service.auth_service import User
from src.schemas.user_schemas import UserSchema, ResponseUser, UpdatePassword, ResponseUpdatePassword, DeleteUserSchema
from sqlalchemy.ext.asyncio import AsyncSession
from src.dependecies.session import (pegar_sessao)



auth_router = APIRouter(prefix="/auth", tags=["auth"])
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="auth/login",  # Este deve ser o endpoint de login
    auto_error=True
)

@auth_router.post('/cadastro', response_model=ResponseUser)
async def cadastro(objeto: UserSchema,session: AsyncSession =  Depends(pegar_sessao)):
   try:

       objeto_service = User(session)
       usuario = await objeto_service.criar_usuario(objeto)
       return ResponseUser (
           mensagem = 'Usuario cadastrado com sucesso',
           id=usuario.id,
           nome=usuario.nome,
           email=usuario.email,
           code=201
       )
   except Exception as e:
       print('ERRO: ',e)
       raise HTTPException(status_code=500, detail=str(e))

@auth_router.post('/login')
async def login( form_data: OAuth2PasswordRequestForm = Depends(), session: AsyncSession =  Depends(pegar_sessao)):
    try:

       objeto_service = User(session)
       objeto_user = await objeto_service.login_usuario(form_data.username, form_data.password)
       return objeto_user

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@auth_router.post('/atualizar', response_model=ResponseUpdatePassword)
async def atualizar_senha( dados:UpdatePassword,session: AsyncSession = Depends(pegar_sessao)):
    try:
        objeto_service = User(session)
        await objeto_service.atualizar_senha(dados.email, dados.senha)
        return ResponseUpdatePassword(
            message='Senha atualizada com sucesso',
            email=dados.email,
            code=200
        )
    except HTTPException as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        print('ERRO: ',e)
        raise HTTPException(status_code=500, detail='Erro interno no servidor')

#Get

@auth_router.get('/admin-only', )
async def rota_admin(obj: str = Depends(check_admin_roler)):
    return {'objeto': obj, "msg": 'esta vendo então pega'}

@auth_router.get('/usuarios',response_model=ResponseUser)
async def usuarios(session: AsyncSession = Depends(pegar_sessao), _:dict = Depends(check_admin_roler) ):
    try:
        objeto_service = User(session)
        usuarios = await objeto_service.buscar_todos_usuarios()
        return ResponseUser(
            mensagem = 'Lista de todos os usuarios cadastrados',
            id=usuarios.id,
            nome=usuarios.nome,
            email=usuarios.email,
            code=200
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@auth_router.delete('/user')
async def deletar_usuario(dados:DeleteUserSchema,_:dict = Depends(check_admin_roler), session: AsyncSession = Depends(pegar_sessao)):
    try:
        objeto_service = User(session)
        await objeto_service.deletar_usuario(dados.id)
        return JSONResponse(status_code=204, content={'mensagem': 'Usuario deletado com sucesso'})
    except Exception:
        raise HTTPException(status_code=500, detail='Erro interno no servidor')




