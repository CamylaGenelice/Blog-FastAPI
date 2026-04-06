
# 📝 Blog API - Sistema de Postagens

Este projeto é uma API de blog desenvolvida com foco em boas práticas de desenvolvimento backend, oferecendo funcionalidades completas para gerenciamento de usuários, autenticação e criação de conteúdos.

---

## 🚀 Sobre o projeto

A **Blog API** é uma aplicação backend que permite:

* Criação e autenticação de usuários
* Criação, edição, listagem e exclusão de posts
* Sistema de comentários vinculado aos posts
* Controle de acesso baseado em permissões (roles)
* Validação de dados e tratamento de erros

O projeto foi estruturado seguindo princípios de organização em camadas, separando responsabilidades entre rotas, serviços e repositórios.

---

## 🧱 Arquitetura

O sistema segue uma arquitetura em camadas:

* **Routes (Rotas)** → Responsável por lidar com as requisições HTTP
* **Services (Serviços)** → Contém a lógica de negócio
* **Repositories (Repositórios)** → Responsável pela comunicação com o banco de dados
* **Schemas** → Validação e serialização de dados com Pydantic
* **Models** → Definição das entidades do banco com SQLAlchemy
* **Security** → Responsável por criar tokens JWT e validar 
* **Tests** → Responsavel por testar as funcionalidades dos modulos utilizando PyTest
---

## ⚙️ Tecnologias utilizadas

### 🔹 Backend

* **FastAPI** → Framework moderno e performático para construção de APIs
* **Python** → Linguagem principal do projeto

### 🔹 Banco de dados

* **PostgreSQL** → Banco de dados relacional
* **SQLAlchemy (Async)** → ORM para manipulação do banco de forma assíncrona
* **AsyncPG** → Driver assíncrono para PostgreSQL

### 🔹 Validação e tipagem

* **Pydantic** → Validação de dados e schemas de entrada/saída

### 🔹 Autenticação e segurança

* **JWT (JSON Web Token)** → Autenticação baseada em tokens
* **Dependências do FastAPI** → Controle de acesso e injeção de dependências

---

## 🔐 Funcionalidades principais

### 👤 Usuários

* Registro de novos usuários
* Login com geração de token JWT
* Controle de permissões (ex: admin)

### 📰 Posts

* Criar posts
* Listar posts
* Editar posts
* Deletar posts

### 💬 Comentários

* Criar comentários em posts
* Editar comentários
* Deletar comentários
* Buscar comentários

---

## 🧪 Boas práticas aplicadas

* Separação de responsabilidades (Clean Architecture)
* Uso de tipagem forte
* Validação de dados com Pydantic
* Tratamento de exceções
* Uso de async/await para alta performance
* Código limpo e organizado

---


## ▶️ Como executar o projeto

```bash
# Clone o repositório
git clone https://github.com/CamylaGenelice/Blog-FastAPI.git

# Acesse a pasta
cd seu-repositorio

# Crie um ambiente virtual
python -m venv venv

# Ative o ambiente
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Instale as dependências
pip install -r requirements.txt

# Execute o servidor
uvicorn main:app --reload
```

---

## 📄 Licença

Este projeto está sob a licença MIT.

---

## 💡 Autor
Desenvolvido por Camyla Genelice
Desenvolvido com foco em aprendizado e aplicação de boas práticas de engenharia de software backend.
