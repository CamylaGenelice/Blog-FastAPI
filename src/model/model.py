from datetime import datetime

import pytz
from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship

from .data import Base

class Usuario(Base):
    __tablename__ = "usuario"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    senha = Column(String, nullable=False)
    role_id = Column(Integer, ForeignKey("role.id"))
    role = relationship('Role', foreign_keys=[role_id])
    codigo_recuperacao = Column(String, nullable=True)
    codigo_expiracao = Column(DateTime, nullable=True)
    tentativas_codigo = Column(Integer, default=0)
    token_refresh = Column(Text, nullable=True, unique=True)
    ativo = Column(Boolean, nullable=True, default=True)
    data_exclusao = Column(DateTime, nullable=True)
    comentarios = relationship('Comentarios', back_populates="autor")

    def __init__(self, nome,email, senha, role_id=1):
        self.nome = nome
        self.email = email
        self.senha = senha
        self.role_id = role_id

class Role(Base):
    __tablename__ = "role"
    id = Column(Integer, primary_key=True)
    nome = Column(String, nullable=False)

    def __init__(self, nome):
        self.nome = nome

class Posts(Base):
    __tablename__ = "post"
    id = Column(Integer, primary_key=True, autoincrement=True)
    titulo = Column(String, nullable=False)
    conteudo = Column(String, nullable=False)
    imagem_nome_arquivo = Column(String, nullable=True)
    data_criacao = Column(DateTime, nullable=True, default=lambda: datetime.now(pytz.timezone('America/Sao_Paulo')))
    autor_id = Column(Integer, ForeignKey("usuario.id"))
    aut = relationship("Usuario", foreign_keys=[autor_id])

    def __init__(self, titulo, conteudo, autor_id, caminho=None):
        self.titulo = titulo
        self.conteudo = conteudo
        self.autor_id = autor_id
        self.imagem_nome_arquivo = caminho

class Comentarios(Base):
    __tablename__ = "comentario"
    id = Column(Integer, primary_key=True, autoincrement=True)
    texto = Column(String, nullable=False)
    autor_id = Column(Integer, ForeignKey("usuario.id"))
    post_id = Column(Integer, ForeignKey("post.id",ondelete="CASCADE"))

    autor = relationship("Usuario", foreign_keys=[autor_id], back_populates="comentarios")
    post = relationship("Posts", foreign_keys=[post_id])

    def __init__(self, texto, autor_id, post_id):
        self.texto = texto
        self.autor_id = autor_id
        self.post_id = post_id