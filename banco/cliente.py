from utils.formatacao import str_para_date, date_para_str

class Cliente:
    def __init__(self, nome: str, email: str, cpf: str, data_nascimento: str) -> None:
        self.__id = id(self)
        self.__nome = nome
        self.__email = email
        self.__cpf = cpf
        self.__data_nascimento = str_para_date(data_nascimento)


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
    def email(self: object, email: str) -> None:
        self.__email = email

    @property
    def cpf(self: object) -> str:
        return self.__cpf   

    @property
    def data_nascimento(self: object) -> str:
        return date_para_str(self.__data_nascimento)

    
    def __str__(self: object) -> str:
        return f'ID: {self.__id} \nNome: {self.__nome} \nE-mail: {self.__email} \nCPF: {self.__cpf} \nData de Nasc.: {self.__data_nascimento}'