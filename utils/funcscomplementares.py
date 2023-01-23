
import os
from time import sleep

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


def criar_conta(dadosUsuario):
    while True:
        nome = input('Informe seu nome: ').title().strip()
        if valida_nome(nome): break
        else:
            print("Nome inválido.")
            continue
    
    while True:
        email = input('Insira seu E-mail: ')
        if valida_email(email): break
        else:
            print('Insira um E-mail válido.')
            continue 

    while True:
        cpf = input('Insira seu CPF: ')
        if valida_cpf(cpf): break
        else:
            print('CPF inválido.')
            continue
    
    while True:
        data_nascimento = input('Informe sua data de nascimento com [/]: ')
        if valida_data(data_nascimento): break
        else:
            print('Data de nascimento inválida.')
            continue

    pessoa = dadosUsuario(nome, email, cpf, data_nascimento)
    print('Conta criada com sucesso!')
    return pessoa


def listar_contas(contas):
    if not contas:
        senao()
        return

    for conta in contas:
        print(f'Agência: {conta.agencia}')
        print(f'Nome: {conta.cliente.nome}')
        print(f'E-mail: {conta.cliente.email}')
        print(f'CPF: {conta.cliente.cpf}')
        print(f'Data Nasc.: {conta.cliente.data_nascimento}')
        print(f'Saldo: {formata_str_float(conta.saldo)}')
        print(f'Limite: {formata_str_float(conta.limite)}')
        print('-=' * 20)


def atualizar_dados(contas):
    if not contas:
        senao()
        return

    agencia = int(input('Informe sua agência: '))
    conta_atualizar = next((conta for conta in contas if conta.agencia == agencia), None)
    if conta_atualizar:
        while True:
            novo_email = input('Digite seu novo E-mail: ')
            if valida_email(novo_email):
                conta_atualizar.cliente.email = novo_email
                print('E-mail atualizado com sucesso.')
                break
            else:
                print('Insira um E-mail válido.')
                continue 
    else:
        print(f'Agência "{agencia}" não encontrada.')


def excluir_conta(contas):
    if not contas:
        senao()
        return

    agencia = int(input('Informe a agência: '))
    contas_a_excluir = [conta for conta in contas if conta.agencia == agencia]
    if contas_a_excluir:
        for conta in contas_a_excluir:
            contas.remove(conta)
        print('Conta excluída com sucesso.')
    else:
        print(f'Não foi encontrada a agência "{agencia}"')


def metodo_deposito_saque(contas):
    if not contas:
        senao()
        return

    escolha_metodo = int(input('Deseja realizar depósito(1) ou saque(2)?'))

    if escolha_metodo == 1:
        agencia = int(input('Informe o número da sua agência para depositar: '))
        conta = next((conta for conta in contas if conta.agencia == agencia), None)
        if conta:
            valor_deposito = float(input('Informe o valor: '))
            conta.depositar(valor_deposito)

        else:
            print(f'Não foi encontrada a agência "{agencia}"')
    elif escolha_metodo == 2:
        agencia = int(input('Informe o número da sua agência para saque: '))
        conta = next((conta for conta in contas if conta.agencia == agencia), None)
        if conta:
            valor_saque = float(input('Informe o valor: '))
            conta.sacar(valor_saque)

        else:
            print(f'Não foi encontrada a agência "{agencia}"')
    else:
        print("Entrada inválida")
        

def transferencia(contas):
    if not contas:
        senao()
        return

    agencia_saque = int(input('Informe a agência: '))
    agencia_deposito = int(input('Informa a agência que deseja depositar: '))
    valor = float(input('Valor que deseja depositar: '))

    conta_saque = next((conta for conta in contas if conta.agencia == agencia_saque), None)
    conta_deposito = next((conta for conta in contas if conta.agencia == agencia_deposito), None)
    
    if conta_saque and conta_deposito:
        if conta_saque.saldo >= valor:
            conta_saque.sacar(valor)
            conta_deposito.depositar(valor)
            print('Transferência realizada com sucesso!')
        else:
            print('Você não tem saldo suficiente.')
    else:
        if not conta_saque:
            print(f'Agência de saque "{agencia_saque}" não encontrada')
        if not conta_deposito:
            print(f'Agência de deposito "{agencia_deposito}" não encontrada')
    

def senao():
    print('Nenhuma conta cadastrada.')
    sleep(1)
    os.system('cls')
