from fastapi import APIRouter, HTTPException, Response, Depends
from src.service.comments_service import CommentsService
from src.model.model import Comentarios
from src.schemas.comments_schemas import CommentSchema, DeleteSchema, EditSchema
from sqlalchemy.ext.asyncio import AsyncSession
from src.dependecies.session import pegar_sessao
from src.dependecies.jwt_dependecies import current_user, check_admin_roler

comments_router = APIRouter(prefix="/comments", tags=["comments"])

@comments_router.post('/')
async def criar_comentario(dados: CommentSchema, user: str = Depends(current_user), session: AsyncSession = Depends(pegar_sessao)):
    try:
        autor_do_comentario_id = int(user["sub"])
        # O 'autor_id' do comentário recebe o ID de quem está logado (o comentador)
        objeto_model = Comentarios(texto=dados.texto, autor_id=autor_do_comentario_id, post_id=dados.post_id)
        objeto_service = CommentsService(session)
        objeto_comentario = await objeto_service.criar_comentario(objeto_model)

        return {'mensagem': 'Comentario criado com sucesso', 'status_code': 200, 'content': objeto_comentario}


    except Exception as e:
        print(e)
        return HTTPException(status_code=400, detail=str(e))

@comments_router.delete('/delete')
async def delete_comentario(dados: DeleteSchema, _: str = Depends(check_admin_roler), session: AsyncSession = Depends(pegar_sessao)):
    try:
        objeto_service = CommentsService(session)
        await objeto_service.deletar_comentario(dados.id)
        return Response(status_code=200, content='Comentario deletado com sucesso')
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@comments_router.post('/edit')
async def editar_comentario( dados: EditSchema,session: AsyncSession = Depends(pegar_sessao), _ : str = Depends(current_user) ):
    try:
        objeto_service = CommentsService(session)
        consulta = await objeto_service.editar_comentario(dados.id, dados.texto)
        return {
            'status_code':200,
            'content': consulta,
                }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@comments_router.post('/buscar_comentario')
async def buscar_comentario(dados: DeleteSchema, session: AsyncSession = Depends(pegar_sessao)):
    try:
        objeto_service = CommentsService(session)
        consulta = await objeto_service.buscar_comentario(dados.id)
        return {
            'mensagem': 'Busca concluída com sucesso',
            'status_code': 200,
            'content': consulta,
        }

    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))

