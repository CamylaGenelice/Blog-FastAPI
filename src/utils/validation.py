import re


def validar_nome(nome: str) -> bool:
    padrao = re.match(r"^[A-Za-zÀ-ÖØ-öø-ÿ\s]+$", nome)
    if padrao:
        return True
    return False

def validar_email(email: str) -> bool:
    padrao = re.match(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$", email)
    if padrao:
        return True
    return False

def validar_senha(senha: str) -> bool:
    s  = len(senha)
    if s >= 7:
        return True
    return False