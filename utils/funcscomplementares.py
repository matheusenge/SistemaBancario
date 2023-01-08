
from time import sleep
import os
from banco.conta import *
from utils.validacoes import *

def menu():
    print('''
- PRESSIONE 1 PARA CADASTRAR CLIENTE
                                   
- PRESSIONE 2 PARA LISTAR CLIENTES
                                                            
- PRESSIONE 3 PARA ATUALIZAR DADOS

- PRESSIONE 4 PARA EXCLUIR CADASTRO
                                            
- PRESSIONE 5 PARA DEPOSITO/SAQUE
                                              
- PRESSIONE 6 PARA TRANSFERENCIA
                                            
- PRESSIONE 0 PARA SAIR DO SISTEMA
    ''')


def criar_conta(dados_usuario):
    while True:
        nome: str = input('Informe seu nome: ').title().strip()
        if any(char.isdigit() for char in nome):
            print('Somente Letras!')
            continue
        break
    
    while True:
        email: str = input('Insira seu E-mail: ')
        checa_email = valida_email(email)

        if checa_email: break

        else: 
            print('Insira um E-mail válido.')
            continue 

    while True:
        cpf: str = input('Insira seu CPF: ')
        checa_cpf = valida_cpf(cpf)
        
        if checa_cpf: break
            
        else:
            print('CPF inválido.')
            continue
    
    while True:
        data_nascimento: str = input('Informe sua data de nascimento com [/]: ')
        data = valida_data(data_nascimento)
        
        if not data:
            print('Insira uma data válida.')
            continue

        else: break

    pessoa: object = dados_usuario(nome, email, cpf, data_nascimento)
    print('Conta criada com sucesso!')
    return pessoa


def listar_contas(contas):
    if contas:
        for conta in contas:
            print(f'Agência: {conta.agencia}')
            print(f'Nome: {conta.cliente.nome}')
            print(f'E-mail: {conta.cliente.email}')
            print(f'CPF: {conta.cliente.cpf}')
            print(f'Data Nasc.: {conta.cliente.data_nascimento}')
            print(f'Saldo: {formata_str_float(conta.saldo)}')
            print(f'Limite: {formata_str_float(conta.limite)}')
            print('-=' * 20)
    else:
        print('Nenhum cadastro encontrado.')
        sleep(1.5)
        os.system('cls')


def atualizar_dados(contas):
    if contas:
        agencia: int = int(input('Informe sua agencia: '))
        for conta in contas:
            if agencia == conta.agencia: 
                while True:
                    novo_email: str = input('Digite seu novo E-mail: ')
                    checa_email = valida_email(novo_email)

                    if checa_email: break

                    else:
                        print('Insira um E-mail válido.')
                        continue 
                conta.cliente.email: str = novo_email
                print('E-mail atualizado com sucesso.')
                sleep(0.5)
                return
        else:
            print(f'Não foi encontrada a agência "{agencia}"')
            return

    print('Nenhuma conta cadastrada.')
    sleep(1.5)
    os.system('cls')


def excluir_conta(contas):
    if contas:
        agencia: int = int(input('Informe sua agencia: '))
        for conta in contas:
            if agencia == conta.agencia:
                contas.pop()
                print('Conta excluída com sucesso.')
                return
        else:
            print(f'Não foi encontrada a agência "{agencia}"')
            return
             
    print('Nenhuma conta cadastrada.')
    sleep(1.5)
    os.system('cls')


def metodo_deposito_ou_saque(contas):
    if contas:
        escolha_metodo: int = int(input('Deseja realizar deposito(1) ou saque(2)?'))

        match escolha_metodo:
            case 1:   
                agencia: int = int(input('Informe o número da sua agencia para depositar: '))
                
                for conta in contas:
                    if agencia == conta.agencia:
                        valor_deposito: float = float(input('Informe o valor: '))
                        conta.depositar(valor_deposito)
                        sleep(1)
                        break
                else:
                    print(f'Não foi encontrada a agência "{agencia}"')
                    sleep(1.5)
                    os.system('cls')
            case 2:      
                agencia: int = int(input('Informe o número da sua agencia para saque: '))
         
                for conta in contas:
                    if agencia == conta.agencia:
                        valor_saque: float = float(input('Informe o valor: '))
                        conta.sacar(valor_saque)
                        sleep(1)
                        break
                else:
                    print(f'Não foi encontrada a agência "{agencia}"')
                    sleep(1.5)
                    os.system('cls')
    else:
        print('Nenhuma conta cadastrada no sistema.')
        sleep(1.5)
        os.system('cls')
        

def depositar(valor, agencia, contas):
    [conta.depositar(valor) for conta in contas if conta.agencia == agencia]


def sacar(valor, agencia, contas):
    [conta.sacar(valor) for conta in contas if conta.agencia == agencia]


def transferencia(contas):
    if contas:
        agencia_saque: int = int(input('Informe a sua agencia: '))
        agencia_deposito: int = int(input('Informa a agencia que deseja depositar: '))
        valor: float = float(input('Valor que deseja depositar: '))

    for conta in contas:
        if agencia_saque == conta.agencia:
            if conta.saldo >= valor:
                sacar(valor, agencia_saque, contas)
                depositar(valor, agencia_deposito, contas)
                print('Transferencia realizada com sucesso!')   
                break
            else:
                print('Você não tem saldo suficiente.')
                break
        else:
            print('Agencia não encontrada')
            continue
    else:
        print('Nenhuma agencia cadastrada.')
        sleep(1.5)
        os.system('cls')