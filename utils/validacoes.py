from datetime import datetime
import re

def valida_email(email) -> str:
    try:
        if not re.match(r"^(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|\"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*\")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])$", email):
            return False

        return True
    except ValueError: return False


def valida_cpf(cpf) -> str:
    try:
        nove_digitos = cpf[:9]
        contador_regressivo_1 = 10

        resultado_digito_1 = 0
        for digito in nove_digitos:
            if digito.isdigit():
                resultado_digito_1 += int(digito) * contador_regressivo_1
                contador_regressivo_1 -= 1
        digito_1 = (resultado_digito_1 * 10) % 11
        digito_1 = digito_1 if digito_1 <= 9 else 0

        dez_digitos = nove_digitos + str(digito_1)
        contador_regressivo_2 = 11

        resultado_digito_2 = 0
        for digito in dez_digitos:
            if digito.isdigit():
                resultado_digito_2 += int(digito) * contador_regressivo_2
                contador_regressivo_2 -= 1
        digito_2 = (resultado_digito_2 * 10) % 11
        digito_2 = digito_2 if digito_2 <= 9 else 0

        cpf_gerado_pelo_calculo = f'{nove_digitos}{digito_1}{digito_2}'

        if cpf == cpf_gerado_pelo_calculo:
            return True
        else: return False
    except ValueError: return False


def valida_data(date) -> str:
    try:
        date_dt = datetime.strptime(date, "%d/%m/%Y")
        
        if date_dt > datetime.now():
            return False

        return date_dt 
    except ValueError: return False
