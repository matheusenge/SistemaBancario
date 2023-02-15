import os
from typing import Callable, List

from banco.cliente import Cliente
from banco.conta import Conta
from utils.funcscomplementares import *


def main() -> None:
    contas: List[Conta] = carregar_contas()
    os.system('cls' if os.name == 'nt' else 'clear')
    
    opcoes = {
        1: criar_conta,
        2: listar_cadastros,
        3: atualizar_dados,
        4: excluir_cadastro,
        5: metodo_deposito_saque,
        6: transferencia,
        0: 'exit'
    }
    while True:
        menu()
        opcao = input('> ')
        if not opcao.isdigit():
            print('Insira um número entre 1/6 - Sair do sistema [0].')
            continue
        opcao = int(opcao)
        if opcao not in opcoes:
            print('Opção inválida, tente novamente:')
            continue
        if opcao == 0:
            print('Obrigado! Até logo...')
            break
        else:
            funcao: Callable = opcoes[opcao]
            if opcao == 1:
                cliente = funcao(Cliente)
                conta = Conta(cliente)
                contas.append(conta)
                salvar_contas(contas)
            else:
                funcao(contas)

main()