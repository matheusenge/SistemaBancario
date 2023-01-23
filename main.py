import os
from time import sleep
from typing import List
from banco.cliente import *
from banco.conta import *
from utils.funcscomplementares import *

os.system('cls')

contas: List[Conta] = []

def main():
    while True:
        menu()
        opcao = input('> ')
        if not opcao.isdigit():
            print('Insira um número entre 1/6 - Sair do sistema [0].')
            sleep(1)
            continue
        opcao = int(opcao)
        if opcao == 1:
            dados = criar_conta(Cliente)
            cliente = Cliente(dados.nome, dados.email, dados.cpf, dados.data_nascimento)
            conta = Conta(cliente)
            contas.append(conta)
            sleep(1)

        elif opcao == 2:
            listar_contas(contas)

        elif opcao == 3:
            atualizar_dados(contas)

        elif opcao == 4:
            excluir_conta(contas)

        elif opcao == 5:
            metodo_deposito_saque(contas)

        elif opcao == 6:
            transferencia(contas)

        elif opcao == 0:
            print('Obrigado! Até logo...')
            sleep(1)
            break
        
        else:
            print('Opção inválida, tente novamente:')


if __name__ == '__main__': main()