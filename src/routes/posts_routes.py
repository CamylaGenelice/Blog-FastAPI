
from fastapi import APIRouter, HTTPException, Response
from fastapi.params import Depends


from src.dependecies.session import pegar_sessao
from src.dependecies.jwt_dependecies import check_admin_roler
from src.service.posts_service import PostService
from src.schemas.post_schema import PostSchema, EditarPostSchema, ResponseCreatePostSchema, GetPostSchema, ResponseUpdatePostSchema
from src.model.model import Posts
from sqlalchemy.ext.asyncio import AsyncSession


post_router = APIRouter(prefix="/post", tags=["post"])

@post_router.post('/criar_post', response_model=ResponseCreatePostSchema)
async def criar_post(dados: PostSchema, session: AsyncSession = Depends(pegar_sessao), _: dict = Depends(check_admin_roler)):
    try:
        objeto_model = Posts(titulo=dados.titulo, conteudo=dados.texto, autor_id=2)
        objeto_service = PostService(session)
        await objeto_service.criar_post(objeto_model)
        return ResponseCreatePostSchema(
            mensagem=f'Post criado com sucesso!',
            objeto_titulo=dados.titulo,
            objeto_texto=dados.texto,
            code=201
        )


    except Exception as e:
        print('ERRO: ',e)
        raise HTTPException(status_code=500, detail='Erro interno no servidor')

@post_router.post('/editar_post')
async def atualizar_post(dados:EditarPostSchema , session: AsyncSession = Depends(pegar_sessao), _: str = Depends(check_admin_roler)):
    try:

        objeto_service = PostService(session)
        await objeto_service.editar_post(dados.id, dados.titulo, dados.conteudo)

        return Response(status_code=201, content='Post atualizado com sucesso!')


    except Exception as e:
        print('ERRO na rota: ', e)
        raise HTTPException(status_code=500, detail='Erro interno no servidor')


@post_router.get('/posts')
async def buscar_posts(session: AsyncSession = Depends(pegar_sessao)):
    try:
        objeto_service = PostService(session)
        consulta = await objeto_service.get_posts()
        return consulta

    except Exception as e:
        print('ERRO: ', e)
        raise HTTPException(status_code=500, detail='Erro interno no servidor')

@post_router.delete('/deletar_post')
async def deletar_post(dados: GetPostSchema,session: AsyncSession = Depends(pegar_sessao), _:str = Depends(check_admin_roler)):
    try:
        objeto_service = PostService(session)
        await objeto_service.deletar_post(dados.id)
        return Response(status_code=200, content='Post deletado com sucesso!')

    except HTTPException as e:
        print('ERRO: ',e)
        raise HTTPException(status_code=404, detail='Não foi possivel encontrar o post')
    except Exception as e:
        print('ERRO: ', e)
        raise HTTPException(status_code=500, detail='Erro interno no servidor')

