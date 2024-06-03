import textwrap
from abc import ABC, abstractmethod
from datetime import datetime

class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes

    def adicionar_transacao(self, transacao):
        self._transacoes.append(transacao)

class Transacao(ABC):
    @property
    @abstractmethod
    def valor(self):
        pass

    @abstractmethod
    def registrar(self, conta):
        pass

class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.depositar(self.valor)
        if sucesso_transacao:
            conta.historico.adicionar_transacao(f"Depósito: R$ {self.valor:.2f}")

class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self.valor)
        if sucesso_transacao:
            conta.historico.adicionar_transacao(f"Saque: R$ {self.valor:.2f}")

class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()

    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)

    @property
    def saldo(self):
        return self._saldo

    @property
    def numero(self):
        return self._numero

    @property
    def agencia(self):
        return self._agencia

    @property
    def cliente(self):
        return self._cliente

    @property
    def historico(self):
        return self._historico

    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print("Depósito realizado com sucesso!")
            return True
        else:
            print("Operação falhou! O valor informado é inválido.")
            return False

    def sacar(self, valor):
        if valor > self._saldo:
            print("Operação falhou! Você não tem saldo suficiente.")
            return False
        elif valor > 0:
            self._saldo -= valor
            print("Saque realizado com sucesso!")
            return True
        else:
            print("Operação falhou! O valor informado é inválido.")
            return False

    def exibir_extrato(self):
        print("\n============= EXTRATO =============")
        if not self._historico.transacoes:
            print("Não foram realizadas movimentações.")
        else:
            for transacao in self._historico.transacoes:
                print(transacao)
        print(f"\nSaldo: R$ {self._saldo:.2f}")
        print("=====================================")

class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super().__init__(numero, cliente)
        self._limite = limite
        self._limite_saques = limite_saques
        self._saques_realizados = 0

    def __str__(self):
        return f"""\
======================================
Agência:\t{self.agencia}
C/C:\t\t{self.numero}
Titular:\t{self.cliente.nome}"""

    def sacar(self, valor):
        if self._saques_realizados >= self._limite_saques:
            print("Operação falhou! Número de saques excedidos.")
            return False
        if valor > self._limite:
            print("Operação falhou! O valor do saque excede o limite.")
            return False
        if super().sacar(valor):
            self._saques_realizados += 1
            return True
        return False

class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)

class PessoaFisica(Cliente):
    def __init__(self, nome, data_nascimento, cpf, endereco):
        super().__init__(endereco)
        if not nome.replace(' ', '').isalpha():
            raise ValueError("O nome deve conter apenas letras.")
        if not (cpf.isdigit() and len(cpf) == 11):
            raise ValueError("O CPF deve conter apenas 11 números.")
        try:
            datetime.strptime(data_nascimento, "%d-%m-%Y")
        except ValueError:
            raise ValueError("Data de nascimento inválida. Use o formato dd-mm-aaaa.")
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf

def menu():
    menu = """\n
    ================ MENU ================
    [d]\tDepositar
    [s]\tSacar
    [e]\tExtrato
    [nc]\tNova conta
    [lc]\tListar contas
    [nu]\tNovo usuário
    [q]\tSair
    => """
    return input(textwrap.dedent(menu))

def filtrar_cliente(cpf, clientes):
    clientes_filtrados = [cliente for cliente in clientes if cliente.cpf == cpf]
    return clientes_filtrados[0] if clientes_filtrados else None

def criar_cliente(clientes):
    nome = input("Informe o nome do cliente: ")
    while not nome.replace(' ', '').isalpha():
        print("Nome inválido! O nome deve conter apenas letras.")
        nome = input("Informe o nome do cliente: ")

    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    while True:
        try:
            datetime.strptime(data_nascimento, "%d-%m-%Y")
            break
        except ValueError:
            print("Data de nascimento inválida! Use o formato dd-mm-aaaa.")
            data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")

    cpf = input("Informe o CPF (somente números): ")
    while not (cpf.isdigit() and len(cpf) == 11):
        print("CPF inválido! O CPF deve conter exatamente 11 números.")
        cpf = input("Informe o CPF (somente números): ")

    if filtrar_cliente(cpf, clientes):
        print("CPF já cadastrado!")
        return

    endereco = input("Informe o endereço: ")
    cliente = PessoaFisica(nome, data_nascimento, cpf, endereco)
    clientes.append(cliente)
    print("Cliente criado com sucesso!")

def criar_conta(numero_conta, clientes, contas):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)
    if not cliente:
        print("Cliente não encontrado!")
        return
    conta = ContaCorrente(numero_conta, cliente)
    cliente.adicionar_conta(conta)
    contas.append(conta)
    print("Conta criada com sucesso!")

def listar_contas(contas):
    for conta in contas:
        print(conta)

def recuperar_conta_cliente(cliente):
    if cliente.contas:
        return cliente.contas[0]  # Supondo que cada cliente tenha uma conta
    else:
        print("Cliente não possui conta!")
        return None

def depositar(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)
    if not cliente:
        print("Cliente não encontrado!")
        return

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    valor = float(input("Informe o valor do depósito: "))
    transacao = Deposito(valor)
    cliente.realizar_transacao(conta, transacao)

def sacar(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)
    if not cliente:
        print("Cliente não encontrado!")
        return

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    valor = float(input("Informe o valor do saque: "))
    transacao = Saque(valor)
    cliente.realizar_transacao(conta, transacao)

def exibir_extrato(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)
    if not cliente:
        print("Cliente não encontrado!")
        return

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    conta.exibir_extrato()

def main():
    clientes = []
    contas = []

    while True:
        opcao = menu().strip().lower()

        if opcao == "d":
            depositar(clientes)

        elif opcao == "s":
            sacar(clientes)

        elif opcao == "e":
            exibir_extrato(clientes)

        elif opcao == "nu":
            criar_cliente(clientes)

        elif opcao == "nc":
            numero_conta = len(contas) + 1
            criar_conta(numero_conta, clientes, contas)

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
