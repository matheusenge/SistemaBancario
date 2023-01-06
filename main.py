import os
from time import sleep
from typing import List

from banco.cliente import *
from banco.conta import *
from utils.funcscomplementares import *

os.system('cls')


contas: List[Conta] = []

def main() -> None:
    while True:
        menu()
        opcao: int = int(input('> '))

        match opcao:
            case 1:
                dados: function = criar_conta(Cliente)
                cliente: Cliente = Cliente(dados.nome, dados.email, dados.cpf, dados.data_nascimento)
                conta: Conta = Conta(cliente)
                contas.append(conta)
                print(cliente)
                sleep(1)

            case 2:
                listar_contas(contas)
                sleep(1)

            case 3:
                atualizar_dados(contas)
                sleep(1)

            case 4:
                excluir_conta(contas)
                sleep(1)

            case 5:
                metodo_deposito_ou_saque(contas)
                sleep(2)

            case 6:
                transferencia(contas)
                sleep(2)
            
            case 0:
                break
            
            case _:
                print('Opção inválida.')
                sleep(1.0)
                continue

if __name__ == '__main__':
    main()