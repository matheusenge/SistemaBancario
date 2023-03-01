
import logging
import os
import pickle
from time import sleep
from typing import List, Tuple

from banco.conta import *
from utils.validacoes import *


def menu():
    options = '''
    1 - Cadastrar cliente
    2 - Listar clientes
    3 - Atualizar dados
    4 - Excluir cadastro
    5 - Depósito/Saque
    6 - Transferência
    0 - Sair do sistema
    '''
    print(options)


def criar_conta(dadosUsuario: type) -> Tuple[str, str, str, datetime]:
    try:
        nome = input('Informe seu nome: ').strip().title()
        while not valida_nome(nome):
            print("Nome inválido.")
            nome = input('Informe seu nome: ').strip().title()

        email = input('Insira seu E-mail: ')
        while not valida_email(email):
            print('Insira um E-mail válido.')
            email = input('Insira seu E-mail: ')

        cpf = input('Insira seu CPF: ')
        while not valida_cpf(cpf):
            print('CPF inválido.')
            cpf = input('Insira seu CPF: ')
        cpf = formata_cpf(cpf)

        data_nascimento = input('Informe sua data de nascimento com [/]: ')
        while not valida_data(data_nascimento):
            print('Data de nascimento inválida.')
            data_nascimento = input('Informe sua data de nascimento com [/]: ')

        pessoa = dadosUsuario(nome, email, cpf, data_nascimento)
        print('Conta criada com sucesso!')
        return pessoa
        
    except Exception as e:
        print(f'A conta não pôde ser criada. {e}')


def listar_cadastros(contas: List[Conta]) -> None:
    if not contas:
        senao()
        return

    print('Lista de contas:')
    for i, conta in enumerate(contas):
        print(f'{i + 1}.')
        print(f'Agência: {conta.agencia}')
        print(f'Nome: {conta.cliente.nome}')
        print(f'E-mail: {conta.cliente.email}')
        print(f'CPF: {conta.cliente.cpf}')
        print(f'Data Nasc.: {conta.cliente.data_nascimento}')
        print(f'Saldo: {formata_str_float(conta.saldo)}')
        print(f'Limite: {formata_str_float(conta.limite)}')
        print('-' * 40)


def atualizar_dados(contas: List[Conta]) -> None:
    if not contas:
        senao()
        return

    while True:
        try:
            agencia = int(input('Informe sua agência: '))
        except ValueError:
            print("Por favor, informe um valor numérico para agência.")
            continue

        conta_atualizar = next((conta for conta in contas if conta.agencia == agencia), None)
        if conta_atualizar:
            while True:
                novo_email = input('Digite seu novo E-mail: ')
                if valida_email(novo_email):
                    conta_atualizar.cliente.email = novo_email
                    print('E-mail atualizado com sucesso.')
                    salvar_contas(contas)
                    break
                else:
                    print('Insira um E-mail válido.')
                    continue 
        else:
            print(f'Agência "{agencia}" não encontrada.')


def excluir_cadastro(contas: List[Conta]) -> None:
    if not contas:
        senao()
        return
    
    print('Selecione a conta que deseja excluir:')
    for i, conta in enumerate(contas):
        print(f'{i + 1}. {conta.cliente.nome} - CPF: {conta.cliente.cpf}')
    
    while True:
        escolha = input('Digite o número da conta ou [0] para cancelar: ')
        if escolha == '0':
            return
        elif not escolha.isdigit():
            print('Por favor, insira um número válido.')
        else:
            indice = int(escolha) - 1
            if indice < 0 or indice >= len(contas):
                print('Por favor, selecione uma opção válida.')
            else:
                conta = contas[indice]
                contas.remove(conta)
                salvar_contas(contas)
                print(f'Conta de:\nTitular: {conta.cliente.nome}\nCPF: {conta.cliente.cpf}\nExcluída com sucesso.')
                return


def metodo_deposito_saque(contas: List[Conta]) -> None:
    if not contas:
        senao()
        return

    while True:
        try:
            escolha_metodo = int(input('Deseja realizar depósito(1) ou saque(2)?'))

            if escolha_metodo in [1, 2]:
                agencia = int(input('Informe o número da sua agência: '))
                conta = next((conta for conta in contas if conta.agencia == agencia), None)
                if conta:
                    valor = float(input('Informe o valor: '))
                    if escolha_metodo == 1:
                        try:
                            conta.depositar(valor)
                            logging.info(f'{conta.cliente.nome} realizou um depósito de R${valor:.2f}.')
                            salvar_contas(contas)
                            break
                        except ValueError as e:
                            print(f'Deposito falhou, {e}')
                    else:
                        try:
                            conta.sacar(valor)
                            logging.info(f'{conta.cliente.nome} realizou um saque de R${valor:.2f}.')
                            break
                        except ValueError as e:
                            print(f'Saque falhou, {e}')
                else:
                    print(f'Não foi encontrada a agência "{agencia}"')
            else:
                print("Opção inválida.")
                continue
        except ValueError as error:
            print(f'Erro ao digitar valor: {error}')
            continue
        

def transferencia(contas: List[Conta]) -> None:
        if len(contas) < 2:
            print('Operação não pode ser realizada. É necessário ao menos 2 contas cadastradas.')
            return
        print('Transferência entre contas\n')

        while True:
            numero_conta_origem = input('Digite o número da conta de origem: ')
            if not numero_conta_origem.isdigit():
                print('Número de conta inválido. Tente novamente.\n')
                continue
            numero_conta_origem = int(numero_conta_origem)
            conta_saque = next((conta for conta in contas if conta.agencia == numero_conta_origem), None)
            
            if conta_saque is None:
                print('Conta de origem não encontrada. Tente novamente.\n')
                continue
            for conta in contas:
                if conta == conta_saque:
                    print(f'\nConta de origem encontrada: {conta.cliente.nome} ({conta.agencia})')
            break

        while True:
            numero_conta_destino = input('Digite o número da conta de destino: ')
            if not numero_conta_destino.isdigit():
                print('Número de conta inválido. Tente novamente.\n')
                continue
            numero_conta_destino = int(numero_conta_destino)
            conta_deposito = next((conta for conta in contas if conta.agencia == numero_conta_destino), None)


            if conta_deposito is None:
                print('Conta de destino não encontrada. Tente novamente.\n')
                continue
            for conta in contas:
                if conta == conta_deposito:
                    print(f'\nConta de destino encontrada: {conta.cliente.nome} ({conta.agencia})')
            break

        while True:
            try:
                valor = float(input('Digite o valor a ser transferido: R$ '))
                if valor <= 0:
                    print('Valor deve ser maior que zero. Tente novamente.\n')
                    continue
                if conta_saque.saldo < valor:
                    print('Saldo insuficiente para realizar a transferência. Tente novamente.\n')
                    continue
            except ValueError as error:
                print(f'Erro ao digitar valor: {error}')
                continue

            confirma = confirmar_transferencia(conta_deposito)
            if confirma:
                conta_saque.sacar(valor)
                conta_deposito.depositar(valor)
                logging.info(f'{conta_saque.cliente.nome} realizou uma transferência de R${valor:.2f} para {conta_deposito.cliente.nome}')
                print(f'[{horas()}] Transferência realizada com sucesso!')
                salvar_contas(contas)
                break
            else:
                break


def confirmar_transferencia(conta_deposito):
    print(f'''Confirme os dados:\nAgência: {conta_deposito.agencia}\nNome destinatário: {conta_deposito.cliente.nome}\nCPF: {conta_deposito.cliente.cpf}\n''')
    while True:
        try:
            confirmacao = int(input('Realizar transferência? [1]=sim /[2]=não '))
            if confirmacao == 1:
                return True
            elif confirmacao == 2:
                print('Transferência cancelada.')
                return False
            else:
                raise ValueError('Opção inválida.')
        except ValueError as error:
            print(f'Erro ao confirmar transferência: {error}')


def carregar_contas() -> List[Conta]:
    try:
        if os.path.exists('contas.dat'):
            with open('contas.dat', 'rb') as file:
                return pickle.load(file)
        else:
            with open('contas.dat', 'wb') as file:
                pickle.dump([], file)
            return []
    except (FileNotFoundError, EOFError, pickle.UnpicklingError) as error:
        print(f"Erro ao carregar contas: {error}")
        return []


def salvar_contas(contas: List[Conta]) -> None:
    try:
        with open('contas.dat', 'wb') as file:
            pickle.dump(contas, file)
    except (FileNotFoundError, EOFError, pickle.PicklingError) as error:
        print(f"Erro ao salvar contas: {error}")


def senao():
    print('Não há contas cadastradas.')
    sleep(1)
    os.system('cls')
