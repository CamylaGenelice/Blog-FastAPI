from pydantic import BaseModel

class UserSchema(BaseModel): #para a função criar user

    nome: str
    email: str
    senha: str

    class Config:
        from_attributes = True
class LogoutResponse(BaseModel):
    message: str
    code: int
    class Config:
        from_attributes = True

class GetUserResponse(BaseModel):
    objeto: dict
    code: int

    class Config:
        from_attributes = True

class UpdatePassword(BaseModel):
    email: str
    senha: str

    class Config:
        from_attributes = True


class ResponseUpdatePassword(BaseModel):
    message: str
    email: str
    code: int
    class Config:
        from_attributes = True
class ResponseUser(BaseModel):
    mensagem: str
    id: int
    nome: str
    email: str
    code: int

    class Config:
        from_attributes = True

class DeleteUserSchema(BaseModel):
    role_id: int
    id: int

    class Config:
        from_attributes = True