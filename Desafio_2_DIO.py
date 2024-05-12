from datetime import datetime

def depositar(saldo, valor, extrato, /):
    try:
        if valor > 0:
            saldo += valor
            extrato += (f"Depósito: R$ {valor:.2f}\n")
            print("Depósito realizado com sucesso.")
        else:
            print("Valor inválido. Por favor, insira um valor positivo.")

        return saldo, extrato
    except ValueError:
        print("Valor inválido. Por favor, insira um número válido.")
        return saldo, extrato


def sacar(*, saldo, valor, extrato, limite, numero_saques, limite_saques):
    excedeu_saldo = valor > saldo
    excedeu_limite = valor > limite
    excedeu_saques = numero_saques  > limite_saques

    if excedeu_saldo:
        print("Operação falhou! Você não tem saldo suficiente.")


    elif excedeu_limite:
        print("Valor inválido. O valor do saque excede o limite.")


    elif excedeu_saques:
        print("Operação falhou! Número de saques excedidos .")

    elif valor > 0:
        saldo -= valor
        numero_saques += 1
        extrato += f"Saque: R$ {valor:.2f}\n"
        print("Saque realizado com sucesso.")

    else:
      print("Operação falhou ! O valor informado é inválido. ")

    return saldo, extrato


def exibir_extrato(saldo, /, *, extrato):
    print("\n================ EXTRATO ================")
    if not extrato:
        print("Não foram realizadas movimentações.")
    else:
        for movimentacao in extrato.split('\n'):
            print(movimentacao)
    print(f"\nSaldo: R$ {saldo:.2f}")
    print("===========================================")

def criar_usuario(usuarios):
    cpf = input("Informe o CPF (somente números): ")
    
    if len(cpf) != 11 or not cpf.isdigit():
        print("CPF inválido! O CPF deve conter exatamente 11 números.")
        return
    
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print("Usuário com CPF já cadastrado!")
        return
      

    nome = input("Digite o nome completo: ")

    while True:
        try:
            data_nascimento = datetime.strptime(input("Digite a data de nascimento (dd-mm-aaaa): "), "%d-%m-%Y")
            break  # Se a conversão for bem-sucedida, saímos do loop
        except ValueError:
            print("Formato de data inválido! Por favor, insira a data no formato dd-mm-aaaa.")
    
    endereco = input("Digite o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

    usuarios.append({"nome": nome, "data_nascimento": data_nascimento, "cpf": cpf, "endereco": endereco})
    print("Usuário cadastrado com sucesso!")

def filtrar_usuario(cpf, usuarios):
    usuarios_filtrados = [usuario for usuario in usuarios if usuario["cpf"]==cpf]
    return usuarios_filtrados[0] if usuarios_filtrados else None

def criar_conta(agencia, numero_conta, usuarios):
    cpf = input("Informe o CPF do usuário: ")
    usuario = filtrar_usuario(cpf, usuarios)


    if usuario:
      print("Conta criada com sucesso!")
      return {"agencia": agencia, "numero_conta": numero_conta, "usuario": usuario}

    else:
      print("Usuário não encontrado. Criação de conta encerrada.")



def listar_contas(contas):
    print("======== LISTA DE CONTAS ========")
    if not contas:
      print("Nenhuma conta cadastrada.")

    else:
      for conta in contas:
        print(f"Agência: {conta['agencia']}")
        print(f"Número da Conta: {conta['numero_conta']}")
        print(f"Titular: {conta['usuario']['nome']}")
        print("=" * 25)

def menu():
    print("=" * 10  + "M E N U"  + "=" * 10)
    while True:
        opcao = input('[d] Depositar\n'+
                      '[s] Sacar\n'+
                      '[e] Extrato\n'+
                      '[nc] Nova Conta\n'+
                      '[nu] Novo Usuário\n'+
                      '[lc] Listar Contas\n'+
                      '[q] Sair\n'+
                      '>>').strip().lower()

        return opcao

def main():
    saldo = 0
    limite = 500
    extrato = ""
    numero_saques = 0
    LIMITE_SAQUES = 3
    AGENCIA = "0001"
    usuarios = []
    contas = []
 
    while True:
        opcao = menu()

        if opcao == "d":
            valor = float(input("Informe o valor do depósito: "))
            saldo, extrato = depositar(saldo, valor, extrato)

        elif opcao == "s":
            valor= float(input("informe o valor do saque: "))

            saldo, extrato = sacar(
                saldo=saldo,
                valor=valor,
                extrato=extrato,
                limite=limite,
                numero_saques=numero_saques,
                limite_saques=LIMITE_SAQUES,
            )

        elif opcao == "e":
            exibir_extrato(saldo, extrato=extrato)

        elif opcao == "nc":
            numero_conta = len(contas) + 1
            conta = criar_conta(AGENCIA, numero_conta, usuarios)

            if conta:
                contas.append(conta)

        elif opcao == "nu":
            criar_usuario(usuarios)

        elif opcao == "lc":
            listar_contas(contas)

        elif opcao == "q":
            print("Saindo...")
            break   # encerra o laço principal

        else:
            print("Operação inválida, por favor selecione novamente a operação desejada.")
            continue  # volta para o início do laço

if __name__ == "__main__":
    main()

