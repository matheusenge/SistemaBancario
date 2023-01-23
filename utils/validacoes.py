from datetime import datetime
import re
from typing import Union

def valida_nome(nome):
    try:
        valida = re.compile('^[a-zA-Z0-9 ]+$')
        if any(char.isdigit() for char in nome) or len(nome.strip()) < 2 or valida.search(nome) == None:
            return False

        return True
    except ValueError: return False


def valida_email(email) -> str:
    try:
        if not re.match(r"^(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|\"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*\")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])$", email):
            return False

        return True
    except ValueError: return False


def valida_cpf(cpf: str) -> Union[bool, str]:
    try:
        nove_digitos = cpf[:9]
        digito_1 = get_cpf_digit(nove_digitos, 10)
        digito_2 = get_cpf_digit(nove_digitos + str(digito_1), 11)
        cpf_gerado_pelo_calculo = f'{nove_digitos}{digito_1}{digito_2}'

        if cpf == cpf_gerado_pelo_calculo:
            return True
        else: return False
    except ValueError: return False
    
def get_cpf_digit(numero_cpf: str, contador: int) -> int:
    result = 0
    for digito in numero_cpf:
        if digito.isdigit():
            result += int(digito) * contador
            contador -= 1
    digito = (result * 10) % 11
    return digito if digito <= 9 else 0


def valida_data(data: str) -> Union[datetime, str]:
    try:
        data_dt = datetime.strptime(data, "%d/%m/%Y")
        
        if data_dt > datetime.now():
            return False

        return data_dt 
    except ValueError: return False