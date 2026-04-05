import pytest
import psycopg2
import bcrypt
from unittest.mock import AsyncMock, MagicMock
from src.service.auth_service import User
from src.schemas.user_schemas import UserSchema

@pytest.mark.asyncio
class TestUser:

    async def test_criar_usuario(self, mocker):
        # 1. Preparação (Setup)
        # Simulamos a sessão e o repositório
        mock_session = MagicMock()
        mock_repo = AsyncMock()
        mocker.patch('src.repository.user_repository.UserQueries', return_value=mock_repo)

        mock_repo.buscar_usuario.return_value = None
        mock_repo.criar_usuario.return_value = {"id": 1, "nome":"teste"}

        service = User(mock_session)
        dados_usuario = UserSchema(nome="Usuario Teste", email="teste@email.com", senha="SenhaForte123!")

        resultado = await service.criar_usuario(dados_usuario)

        # 3. Verificação (Assertion)
        assert resultado is not None
        mock_repo.buscar_usuario.assert_called_once_with("teste@email.com")
        mock_repo.criar_usuario.assert_called_once()


    async def test_criar_usuario_email_duplicado(self, mocker):
        mock_repo = AsyncMock()
        mocker.patch('src.repository.user_repository.UserQueries', return_value=mock_repo)

        # Simulamos que o usuário JÁ existe
        mock_repo.buscar_usuario.return_value = {"id": 1, "email": "duplicado@email.com"}

        service = User(MagicMock())
        dados = UserSchema(nome="Teste", email="duplicado@email.com", senha="Senha123!")

        # Verificamos se a exceção correta é lançada
        with pytest.raises(Exception) as excinfo:
            await service.criar_usuario(dados)

        assert str(excinfo.value) == 'Email já esta em uso'

    async def test_login_usuario_sucesso(self,mocker):
        # --- SETUP ---
        mock_repo = AsyncMock()
        # Mockamos a classe UserQueries para retornar o nosso mock_repo
        mocker.patch('src.repository.user_repository.UserQueries', return_value=mock_repo)

        service = User(MagicMock())

        # Criamos um hash real para simular o que estaria no banco
        senha_plana = "senha123"
        hash_banco = bcrypt.hashpw(senha_plana.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        # Simulamos o retorno do banco de dados
        mock_usuario_db = MagicMock()
        mock_usuario_db.email = "user@teste.com"
        mock_usuario_db.senha = hash_banco  # O que vem do banco é o hash

        mock_repo.buscar_usuario.return_value = mock_usuario_db
        mock_repo.pegar_hash.return_value = hash_banco

        # Dados que o usuário envia no login
        dados_login = MagicMock()
        dados_login.email = "user@teste.com"
        dados_login.senha = "senha123"

        # --- EXECUÇÃO ---
        # Aqui chamamos sua função (assumindo que você completou o '...')
        resultado = await service.login_usuario(dados_login)

        # --- VERIFICAÇÃO ---
        # Se o bcrypt.checkpw retornar True, sua função deve prosseguir
        assert resultado is True  # Ou o que sua função retornar em caso de sucesso