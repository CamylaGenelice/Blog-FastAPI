from fastapi import HTTPException


class ServiceError(Exception):


    def exception_usuario_nao_encontrado(self):
        return HTTPException(status_code=404, detail='Usuario não encontrado')