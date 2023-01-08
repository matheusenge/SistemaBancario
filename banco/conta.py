from banco.cliente import *
from utils.formatacao import *

class Conta:
    codigo: int = 1

    def __init__(self: object, cliente: Cliente) -> None:
        self.__agencia: int = Conta.codigo
        self.__cliente: Cliente = cliente
        self.__saldo: float = 0.0
        self.__limite: float = 500.00
        self.__credito: float = 0.0
        Conta.codigo += 1


    @property
    def agencia(self: object) -> int:
        return self.__agencia   

    @property
    def cliente(self: object) -> str:
        return self.__cliente

    @property
    def saldo(self: object) -> float:
        return self.__saldo  
    
    @saldo.setter
    def saldo(self: object, valor: float) -> None:
        self.__saldo = valor

    @property
    def limite(self: object) -> float:
        return self.__limite

    @limite.setter
    def limite(self: object, valor: float) -> None:
        self.__limite = valor

    @property
    def credito(self: object) -> float:
        return self.__credito

    @credito.setter
    def credito(self: object, valor: float) -> None:
        self.__credito = valor

    def __str__(self: object) -> str:
        return f'Número da agência: {self.agencia} \nCliente: {self.cliente.nome} \nSaldo: {formata_str_float(self.saldo)}'

    
    def depositar(self: object, valor_deposito: float) -> None:
        self.saldo += valor_deposito
        
        print(f'''[{horas()}] Depósito realizado no valor de R${valor_deposito:,.2f}\nAG: {self.agencia} | Nome: {self.cliente.nome} | CPF: {self.cliente.cpf}''')


    def sacar(self: object, valor_saque: float) -> None:
        credito_disponivel: float = self.limite - self.credito

        if self.saldo - valor_saque >= 0:
            self.saldo -= valor_saque
            print(f'[{horas()}] Foi debitado {formata_str_float(valor_saque)} da sua conta.')
            return
        else:
            print('Você não tem saldo suficiente para saque')

            while True:
                escolha: int = int(input('''Escolha uma opção
                \r1 - Sacar no crédito
                \r2 - Sacar no crédito e debito\n
                \rOpção: '''))

                match escolha:
                    case 1:
                        if self.limite < 0 or credito_disponivel < valor_saque:
                            print('Limite insuficiente.')
                            return
                        self.credito += valor_saque
                        self.limite -= valor_saque
                    
                        print(f'Crédito usado: {formata_str_float(self.credito)}')
                        print(f'Limite Disponível: {formata_str_float(self.limite)}')
                        return

                    case 2:
                        if self.saldo + credito_disponivel <= 0:
                            print('Limite insuficiente.')
                            break
                        
                        valor: float = float(input('Informe a quantia de saldo que deseja usar: '))
                        
                        if self.saldo - valor < 0:
                            print('Saldo insuficiente.')
                            return
                        if valor + credito_disponivel < valor_saque:
                            print('Limite insuficiente.')
                            return

                        self.credito += valor_saque - valor
                        self.limite -= valor_saque - valor
                        self.saldo -= valor
                        print(f'Você tem {formata_str_float(self.limite)} de limite.')
                        print(f'Saldo atual: {formata_str_float(self.saldo)}')
                        return

                    case _:
                        print('Informe uma opção válida.')
                        continue


