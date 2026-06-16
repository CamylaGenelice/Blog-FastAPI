from fastapi import HTTPException
from src.repository.post_repository import PostRepository
from sqlalchemy.ext.asyncio import AsyncSession
from src.model.model import Posts
from src.schemas.post_schema import GetPostSchema
from typing import Optional

class PostService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.repository = PostRepository(session)


    async def criar_post(self, titulo: str, conteudo: str, autor: int, caminho_imagem: Optional[str] = None):
        try:
            if(not titulo or not conteudo or not autor):
                raise HTTPException(status_code=404, detail='Campos invalidos')

            objeto_model = Posts(titulo=titulo, conteudo=conteudo, autor_id=autor,caminho=caminho_imagem)
            if(autor != 2):
                raise HTTPException(status_code=403,detail='Usuario não tem autorização')

            objeto_post = await self.repository.criar_post(objeto_model)
            return objeto_post
        except Exception as e:
            print(e)
            raise e

    async def editar_post(self,id: int, titulo: str, texto: str):
        try:
            objeto_pesquisa = await self.repository.buscar_post(id)
            if not objeto_pesquisa:
                raise HTTPException(status_code=404, detail='Post não encontrado')

            objeto_post = await self.repository.alterar_post(id, titulo, texto)
            return objeto_post

        except Exception as e:
            print('ERRO no service',e)
            raise e

    async def buscar_post_nome(self, nome: str):
        try:
            consulta = await self.repository.buscar_nome_post(nome)
            if not consulta:
                raise HTTPException(status_code=404, detail='Nenhum post encontrado')
            return consulta

        except Exception as e:
            raise e

    async def get_post(self, id: int):
        try:
            consulta = await self.repository.buscar_post(id)
            if not consulta:
                return None
            return consulta

        except Exception as e:
            print(e)
            raise e

    async def get_posts(self) :
        try:
            objeto = await self.repository.buscar_posts()
            if not objeto:
                raise Exception('Não existe posts cadastrados')
            # Converte cada objeto SQLAlchemy para Pydantic schema
            return [GetPostSchema.model_validate(objeto) for objeto in objeto]
        except Exception as e:
            print(e)
            raise e

    async def deletar_post(self,id: int):
        try:
            objeto = await self.repository.buscar_post(id)
            if not objeto:
                raise HTTPException(status_code=404, detail='Post não encontrado')

            objeto_delete = await self.repository.deletar_post(id)
            return objeto_delete

        except Exception as e:
            print('Erro: ', e)
            raise e