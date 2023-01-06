from datetime import date
from utils.formatacao import str_para_date, date_para_str
from random import randint

class Cliente:
    identificador: int = randint(1, 500)

    def __init__(self: object, nome: str, email: str, cpf: str, data_nascimento: str) -> None:
        self.__id: int = Cliente.identificador
        self.__nome: str = nome
        self.__email: str = email
        self.__cpf: str = cpf
        self.__data_nascimento: date = str_para_date(data_nascimento)
        Cliente.identificador += randint(1, 10)


    @property
    def id(self: object) -> int:
        return self.__id  

    @property
    def nome(self: object) -> str:
        return self.__nome    

    @property
    def email(self: object) -> str:
        return self.__email

    @email.setter
    def email(self: object, email: float) -> None:
        self.__email = email

    @property
    def cpf(self: object) -> str:
        return self.__cpf   

    @property
    def data_nascimento(self: object) -> str:
        return date_para_str(self.__data_nascimento)

    
    def __str__(self: object) -> str:
        return f'ID: {self.identificador} \nNome: {self.nome} \nE-mail: {self.email} \nCPF: {self.cpf} \nData de Nasc.: {self.data_nascimento}'