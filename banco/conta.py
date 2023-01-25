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
        return f'Número da agência: {self.__agencia} \nCliente: {self.cliente.__nome} \nSaldo: {formata_str_float(self.__saldo)}'
    

    def depositar(self: object, valor_deposito: float) -> None:
        self.saldo += valor_deposito
        
        print(f'''[{horas()}] Depósito realizado no valor de R${valor_deposito:,.2f}\nAG: {self.agencia} | Nome: {self.cliente.nome} | CPF: {self.cliente.cpf}''')


    def sacar(self: object, valor_saque: float) -> None:
        credito_disponivel: float = self.limite - self.credito
        options = {1: 'Sacar no crédito', 2: 'Sacar no crédito e débito'}

        if valor_saque > self.saldo + credito_disponivel:
            raise ValueError('Valor de saque superior ao limite disponível')

        if self.saldo - valor_saque >= 0:
            self.saldo -= valor_saque
            print(f'[{horas()}] Foi debitado {formata_str_float(valor_saque)} da sua conta.')
        else:
            while True:
                try:
                    escolha = int(input(f'Escolha uma opção: {options} \nOpção: '))
                    if escolha not in options:
                        raise ValueError('Opção inválida')
                    break
                except ValueError as e:
                    print(e)

            if escolha == 1:
                if credito_disponivel < valor_saque:
                    raise ValueError('Limite insuficiente')
                self.credito += valor_saque
                self.limite -= valor_saque
                print(f'Crédito usado: {formata_str_float(self.credito)}')
                print(f'Limite disponível: {formata_str_float(self.limite)}')
            elif escolha == 2:
                while True:
                    try:
                        valor = float(input('Informe a quantia de saldo que deseja usar: '))
                        assert valor <= self.saldo, "Saldo insuficiente."
                        assert valor + credito_disponivel >= valor_saque, "Limite insuficiente."
                        break
                    except ValueError:
                        print("Informe um valor válido.")
                    except AssertionError as e:
                        print(e)
                        continue

                self.credito += valor_saque - valor
                self.limite -= valor_saque - valor
                self.saldo -= valor
                print(f'Limite atual: {formata_str_float(self.limite)}')
                print(f'Saldo atual: {formata_str_float(self.saldo)}')
