from fastapi import APIRouter, HTTPException, Response, Depends
from src.service.comments_service import CommentsService
from src.service.posts_service import PostService
from src.model.model import Comentarios
from src.schemas.comments_schemas import CommentSchema, EditSchema, ResponseCommentsSchema
from sqlalchemy.ext.asyncio import AsyncSession
from src.dependecies.session import pegar_sessao
from src.dependecies.jwt_dependecies import current_user

comments_router = APIRouter(prefix="/comments", tags=["comments"])

@comments_router.post('/posts/{post_id}/comments')
async def criar_comentario(post_id:int,dados: CommentSchema, user: str = Depends(current_user), session: AsyncSession = Depends(pegar_sessao)):
    try:
        autor_do_comentario_id = int(user["sub"])
        # O 'autor_id' do comentário recebe o ID de quem está logado (o comentador)
        objeto_model = Comentarios(texto=dados.texto, autor_id=autor_do_comentario_id, post_id=post_id)
        objeto_service = CommentsService(session)

        objeto_comentario = await objeto_service.criar_comentario(objeto_model)

        return {'mensagem': 'Comentario criado com sucesso', 'status_code': 200, 'content': objeto_comentario}

    except Exception:
        raise HTTPException(status_code=500, detail='Erro interno no servidor')

@comments_router.delete('/comments/{comment_id}')
async def delete_comentario(comment_id: int,post_id: int, user_id: str = Depends(current_user), session: AsyncSession = Depends(pegar_sessao)):
    try:
        # converte a string id, enviada pelo front-end, em int.
        comment_id_convertido = int(comment_id)
       # post_id_convertido = int(post_id)
        usuario_id = int(user_id["sub"])

        objeto_service = CommentsService(session)

        resposta = await objeto_service.deletar_comentario(comment_id_convertido, usuario_id, post_id)

        if not resposta:
            raise HTTPException(status_code=404, detail='Erro ao deletar comentário')

        return Response(status_code=200, content='Comentario deletado com sucesso')
    except Exception:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Edita o comentario, o id do comentario é passado pela URL
@comments_router.put('/{comment_id}')
async def editar_comentario(comment_id:int, dados: EditSchema,session: AsyncSession = Depends(pegar_sessao), user_id : str = Depends(current_user) ):
    try:
        comment_id_convertido = int(comment_id) #converte a string id, enviada pelo front-end, em int.
        autor_do_comentario_id = int(user_id["sub"])

        objeto_service = CommentsService(session)
        consulta = await objeto_service.editar_comentario(comment_id_convertido, autor_do_comentario_id, dados.texto)
        return {
            'status_code':200,
            'content': consulta,
                }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Pega todos os comentarios que tem dentro de um post
@comments_router.get('/posts/{post_id}/comments',response_model=ResponseCommentsSchema)
async def buscar_comentarios(post_id: int, session: AsyncSession = Depends(pegar_sessao)):
    try:
        post_id_convertido = int(post_id)
        objeto_service = CommentsService(session)
        objeto_post = PostService(session)

        consulta = await objeto_post.get_post(post_id_convertido)

        if not consulta:
            raise HTTPException(status_code=404, detail='Post não encontrado')

        lista_comentarios = await objeto_service.buscar_comentarios_detalhados(post_id_convertido)

        return ResponseCommentsSchema(content=lista_comentarios)
    except Exception:
        raise
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail='Erro interno no servidor')

