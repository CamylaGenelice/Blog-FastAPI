
from fastapi import APIRouter, HTTPException, Response, File, UploadFile, Form
from fastapi.params import Depends, Query
import os
from typing import Optional
from src.dependecies.session import pegar_sessao
from src.dependecies.jwt_dependecies import check_admin_roler
from src.service.posts_service import PostService
from src.schemas.post_schema import PostSchema, EditarPostSchema, ResponseCreatePostSchema, ResponseUpdatePostSchema
from sqlalchemy.ext.asyncio import AsyncSession
from src.routes.upload_images import upload_para_supabase

post_router = APIRouter(prefix="/post", tags=["post"])


@post_router.post('/criar_post', response_model=ResponseCreatePostSchema)
async def criar_post(titulo: str = Form(...), conteudo: str = Form(), imagem: Optional[UploadFile] = File(None), session: AsyncSession = Depends(pegar_sessao), role: dict = Depends(check_admin_roler)):
    try:
        url_imagem = None

        if imagem and imagem.filename:
            extensao = os.path.splitext(imagem.filename)[1].lower()

            if extensao not in ['.jpg', '.jpeg', '.png', '.webp']:
                raise HTTPException(status_code=400, detail='Formato de imagem inválido')

            url_imagem = await upload_para_supabase(imagem, pasta_destino='capas')


        role_admin = int(role.get('role_id'))
        objeto_service = PostService(session)
        await objeto_service.criar_post(titulo=titulo, conteudo=conteudo, autor=role_admin, caminho_imagem=url_imagem)


        return ResponseCreatePostSchema(
            mensagem='Post criado com sucesso!',
            objeto_titulo=titulo,
            objeto_texto=conteudo,
            objeto_imagem=url_imagem,
            code=201
        )

    except HTTPException as http_err:
        raise http_err
    except Exception as e:
        print('ERRO: ',e)
        raise HTTPException(status_code=500, detail='Erro interno no servidor')

@post_router.put('/{post_id}/editar_post')
async def atualizar_post(post_id:int, dados: EditarPostSchema, session: AsyncSession = Depends(pegar_sessao), _: str = Depends(check_admin_roler)):
    try:

        objeto_service = PostService(session)
        await objeto_service.editar_post(post_id,dados.titulo,dados.texto)

        return {
            'mensagem': 'Post atualizado com sucesso!',
            'code': 201
        }

    except HTTPException as http_err:
        raise http_err
    except Exception as e:
        print('ERRO na rota: ', e)
        raise HTTPException(status_code=500, detail='Erro interno no servidor')

# buscar todos os posts
@post_router.get('/posts')
async def buscar_posts(session: AsyncSession = Depends(pegar_sessao)):
    try:
        objeto_service = PostService(session)
        consulta = await objeto_service.buscar_posts()
        if not consulta:
            return HTTPException(status_code=404, detail='Não foi possivel encontrar os posts')
        return consulta

    except Exception as e:
        print('ERRO: ', e)
        raise HTTPException(status_code=500, detail='Erro interno no servidor')

# pesquisar post pelo titulo
@post_router.get('/pesquisar_post')
async def pesquisar_post(titulo_post: str = Query(None, min_length=3, max_length=700) ,session: AsyncSession = Depends(pegar_sessao)):
    try:
        objeto_service = PostService(session)
        consulta = await objeto_service.buscar_post_nome(titulo_post)

        return consulta
    except Exception:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail='Erro interno no servidor')

# para selecionar um post e colocar ele como principal
# tenho varios posts amostra e quero escolher entre eles
# é para isso que essa rota esta aqui
@post_router.post('/{post_id}')
async def buscar_post_id(post_id: int, session: AsyncSession = Depends(pegar_sessao)):
    try:
        objeto_service = PostService(session)
        post_id_convertido = int(post_id)
        consulta = await objeto_service.buscar_post_id(post_id_convertido)

        if not consulta:
            return HTTPException(status_code=404, detail='Não foi possivel encontrar o post')
        return consulta

    except HTTPException as e:
        raise e
    except Exception as e:
        print('ERRO: ', e)
        raise HTTPException(status_code=500, detail='Erro interno no servidor')


@post_router.delete('/{post_id}/deletar_post')
async def deletar_post(post_id:int, session: AsyncSession = Depends(pegar_sessao), _:str = Depends(check_admin_roler)):
    try:
        objeto_service = PostService(session)
        await objeto_service.deletar_post(post_id)
        return {
            'mensagem': 'Post deletado com sucesso!'
        }

    except HTTPException as e:
        print('ERRO: ',e)
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        print('ERRO: ', e)
        raise HTTPException(status_code=500, detail='Erro interno no servidor')

