from datetime import date, datetime

def date_para_str(data: date) -> str:
    return data.strftime('%d/%m/%Y')


def str_para_date(data: str, formato: str = '%d/%m/%Y') -> date:
    return datetime.strptime(data, formato).date()


def formata_str_float(valor: float) -> str:
    return f'R${valor:,.2f}'.replace(',', '.')


def horas() -> str:
    return datetime.now().strftime("%H:%M")
