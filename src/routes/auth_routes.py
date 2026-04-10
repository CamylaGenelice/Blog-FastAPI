from fastapi import APIRouter, HTTPException, Depends, Response
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from starlette.responses import JSONResponse

from src.dependecies.jwt_dependecies import check_admin_roler, get_me


from src.service.auth_service import UserService
from src.schemas.user_schemas import UserSchema, ResponseUser, UpdatePassword, ResponseUpdatePassword, DeleteUserSchema, GetUserResponse, LogoutResponse
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

       objeto_service = UserService(session)
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

       objeto_service = UserService(session)
       tokens = await objeto_service.login_usuario(form_data.username, form_data.password)

       response = JSONResponse(status_code=200, content='Login realizado com sucesso')

       response.set_cookie(
           key='access_token',
           value=tokens['access_token'],
           httponly=True,
           max_age=1800,
           samesite='lax')

       return response

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@auth_router.post('logout',response_model=LogoutResponse)
async def logout(response: Response,_: AsyncSession = Depends(pegar_sessao)):
    response.delete_cookie(key='access_token')
    return LogoutResponse(
        message='Logout realizado com sucesso',
        code=200
    )


@auth_router.post('/atualizar', response_model=ResponseUpdatePassword)
async def atualizar_senha( dados:UpdatePassword,session: AsyncSession = Depends(pegar_sessao)):
    try:
        objeto_service = UserService(session)
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

@auth_router.get('/admin-only')
async def rota_admin(obj: dict = Depends(check_admin_roler)):
    return {'objeto': obj}

@auth_router.get('/me', response_model=GetUserResponse)
async def me(user: dict = Depends(get_me)):
    return GetUserResponse(
        objeto=user,
        code=200
    )

@auth_router.get('/usuarios',response_model=ResponseUser)
async def usuarios(session: AsyncSession = Depends(pegar_sessao), _:dict = Depends(check_admin_roler) ):
    try:
        objeto_service = UserService(session)
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
async def deletar_usuario(dados:DeleteUserSchema, _:dict = Depends(check_admin_roler), session: AsyncSession = Depends(pegar_sessao)):
    try:
        objeto_service = UserService(session)
        await objeto_service.deletar_usuario(dados.id)
        return JSONResponse(status_code=204, content={'mensagem': 'Usuario deletado com sucesso'})
    except Exception:
        raise HTTPException(status_code=500, detail='Erro interno no servidor')




