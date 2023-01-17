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
        opcao: str = (input('> '))
        if opcao.isdigit():
            opcao = int(opcao)
            match opcao:
                case 1:
                    dados: function = criar_conta(Cliente)
                    cliente: Cliente = Cliente(dados.nome, dados.email, dados.cpf, dados.data_nascimento)
                    conta: Conta = Conta(cliente)
                    contas.append(conta)
                    sleep(1)

                case 2: listar_contas(contas)

                case 3: atualizar_dados(contas)

                case 4: excluir_conta(contas)

                case 5: metodo_deposito_saque(contas)

                case 6: transferencia(contas)
                
                case 0:
                    print('Obrigado! Até logo...')
                    sleep(1)
                    break
                
                case _:
                    print('Opção inválida, tente novamente:')
        else:
            print('Insira um número entre 1/6 - Sair do sistema [0].')
            sleep(1)


if __name__ == '__main__': main()