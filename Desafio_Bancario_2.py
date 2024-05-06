def depositar(saldo):
    while True:
        try:
            valor = float(input("Informe o valor do depósito: "))
            if valor > 0:
                saldo += valor
                print("Depósito realizado com sucesso.")
                return saldo, valor  # Retorna o saldo e o valor depositado
            else:
                print("Valor inválido. Por favor, insira um valor positivo.")
        except ValueError:
            print("Valor inválido. Por favor, insira um número válido.")

def sacar(saldo, limite, numero_saques):
    if numero_saques >= LIMITE_SAQUES:
        print("Operação falhou! Número máximo de saques excedido.")
        return saldo, numero_saques, False, 0

    valor = float(input("Informe o valor do saque: "))
    if valor <= 0:
        print("Valor inválido. Por favor, insira um valor positivo.")
        return saldo, numero_saques, False, 0

    if valor > saldo:
        print("Operação falhou! Você não tem saldo suficiente.")
        return saldo, numero_saques, False, 0
    elif valor > limite:
        print("Operação falhou! O valor do saque excede o limite.")
        return saldo, numero_saques, False, 0

    saldo -= valor
    numero_saques += 1
    print("Saque realizado com sucesso.")
    return saldo, numero_saques, True, valor

def exibir_extrato(saldo, extrato):
    print("\n================ EXTRATO ================")
    if not extrato:
        print("Não foram realizadas movimentações.")
    else:
        for movimentacao in extrato:
            print(movimentacao)
    print(f"\nSaldo: R$ {saldo:.2f}")
    print("==========================================")


saldo = 0
limite = 500
extrato = []
numero_saques = 0
LIMITE_SAQUES = 3

while True:
    menu = """\n
========== M E N U ==========
    [d] Depositar
    [s] Sacar
    [e] Extrato
    [q] Sair
    => """

    opcao = input(menu).strip().lower()

    if opcao == "d":
        saldo, valor_depositado = depositar(saldo)
        extrato.append(f"Depósito: R$ {valor_depositado:.2f}")

    elif opcao == "s":
        saldo, numero_saques, sucesso_saque, valor_saque = sacar(saldo, limite, numero_saques)
        if sucesso_saque:
            extrato.append(f"Saque: R$ {valor_saque:.2f}")

    elif opcao == "e":
        exibir_extrato(saldo, extrato)

    elif opcao == "q":
        print("Saindo...")
        break

    else:
        print("Operação inválida, por favor selecione novamente a operação desejada.")
