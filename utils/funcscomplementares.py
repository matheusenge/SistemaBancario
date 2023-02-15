
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

    try:
        agencia = int(input('Informe sua agência: '))
    except ValueError:
        print("Por favor, informe um valor numérico para agência.")
        return

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
        print(f'{i + 1}. {conta.cliente.nome} - Conta: {conta.agencia}')
    
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
                print(f'Conta de {conta.cliente.nome}\nAgência: {conta.agencia}\nExcluída com sucesso.')
                return


def metodo_deposito_saque(contas: List[Conta]) -> None:
    if not contas:
        senao()
        return

    escolha_metodo = int(input('Deseja realizar depósito(1) ou saque(2)?'))

    if escolha_metodo in [1, 2]:
        agencia = int(input('Informe o número da sua agência: '))
        conta = next((conta for conta in contas if conta.agencia == agencia), None)
        if conta:
            valor = float(input('Informe o valor: '))
            if escolha_metodo == 1:
                try:
                    conta.depositar(valor)
                    salvar_contas(contas)
                except ValueError as e:
                    print(f'Deposito falhou, {e}')
            else:
                try:
                    conta.sacar(valor)
                except ValueError as e:
                    print(f'Saque falhou, {e}')
        else:
            print(f'Não foi encontrada a agência "{agencia}"')
    else:
        print("Opção inválida")
        

def transferencia(contas: List[Conta]) -> None:
    if not contas:
        senao()
        return

    try:
        agencia_saque = int(input('Informe a agência de saque: '))
        agencia_deposito = int(input('Informe a agência de depósito: '))
        valor = float(input('Valor que deseja transferir: '))
    except ValueError:
        print("Por favor, informe um valor numérico para agência e valor.")
        return

    conta_saque = next((conta for conta in contas if conta.agencia == agencia_saque), None)
    conta_deposito = next((conta for conta in contas if conta.agencia == agencia_deposito), None)
    
    if not conta_saque:
        print(f'Agência de saque "{agencia_saque}" não encontrada.')
    elif not conta_deposito:
        print(f'Agência de depósito "{agencia_deposito}" não encontrada.')
    elif conta_saque.saldo < valor:
        print('Você não tem saldo suficiente.')
    else:
        conta_saque.sacar(valor)
        conta_deposito.depositar(valor)
        print('Transferência realizada com sucesso!')
        salvar_contas(contas)


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
