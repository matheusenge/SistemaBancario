from datetime import datetime
import re
from typing import Union, Match, Pattern

def valida_nome(nome: str) -> bool:
    pattern: Pattern[str] = re.compile(r'^[a-zA-Z0-9 ]+$')
    if any(char.isdigit() for char in nome) or len(nome.strip()) < 2 or pattern.search(nome) is None:
        return False
    return True


def valida_email(email: str) -> bool:
    pattern: Pattern[str] = re.compile(r"^(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|\"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*\")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])$")
    match: Match[str] = pattern.match(email)
    if match is None:
        return False
    return True


def valida_cpf(cpf: str) -> bool:
    if not cpf.isdigit() or len(cpf) != 11 or all(digito == cpf[0] for digito in cpf):
        return False

    digitos = list(map(int, cpf))
    check_digito_1 = (sum(digitos[i] * (10 - i) for i in range(9)) * 10 % 11) % 10
    check_digito_2 = (sum(digitos[i] * (11 - i) for i in range(10)) * 10 % 11) % 10

    return check_digito_1 == digitos[9] and check_digito_2 == digitos[10]


def valida_data(data: str) -> Union[datetime, str]:
    data_dt = datetime.strptime(data, "%d/%m/%Y")
    if data_dt > datetime.now():
        return False
    return data_dt 

