from pydantic import BaseModel

class CommentSchema(BaseModel):

    texto: str
   # autor_id: int
    post_id: int

    class Config:
        from_attributes = True




class DeleteSchema(BaseModel):
    id:int

    class Config:
        from_attributes = True

class EditSchema(BaseModel):
    id: int
    texto: str

    class Config:
        from_attributes = True