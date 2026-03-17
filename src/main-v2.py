from abc import ABC, abstractmethod
from datetime import datetime

# VERSÃO 2 = Utilizando INPUTS

class Cliente:
    # caracteristicas
    #contrutor inicializador:
    def __init__(self, endereco):
        self.__endereco = endereco
        self.__contas = []

    # atributos
    def adicionar_conta(self, conta):
        self.__contas.append(conta)

    def listar_contas(self):
        return self.__contas
    
    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

# -----------------------------------

class PessoaFisica(Cliente):
    def __init__(self, nome, data_nascimento, cpf, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf

# -----------------------------------

class Conta:
    def __init__(self, numero, cliente):
        self.__saldo = 0.0
        self.__numero = numero
        self.__agencia = "0001"
        self.__cliente = cliente
        self.__historico = Historico()

    
    @property
    def saldo(self):
        return self.__saldo
    
    @property
    def historico(self):
        return self.__historico

    def sacar(self, valor):
        if valor > self.__saldo:
            print("\nSaldo insuficiente ou valor inválido.")
            return False
        if valor > 0:
            self.__saldo -= valor
            print(f"\nSaque de R${valor} realizado.")
            return True
        return False
    
    def depositar(self, valor):
        if valor > 0:
            self.__saldo += valor
            print(f"\nDepósito de R${valor} realizado.")
            return True
        return False
    
# -----------------------------------
    

class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite = 500, limite_saques = 3):
        super().__init__(numero, cliente)
        self.limite = limite
        self.limite_saques = limite_saques

# -----------------------------------

class Historico:

    def __init__(self, arquivo = "historico.txt"):
        self.arquivo = arquivo
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes

    def adicionar_transacao(self, transacao):

        registro = f"{datetime.now().strftime("%d-%m-%Y %H:%M:%S")} - {transacao.__class__.__name__}: R${transacao.valor:.2f}"

        self._transacoes.append(registro)

        with open(self.arquivo, "a") as f:
            f.write(registro + "\n")

# -----------------------------------

class Transacao(ABC):

    @property
    @abstractmethod
    def valor(self):
        pass

    @abstractmethod
    def registrar(self, conta):
        pass

# -----------------------------------

class Saque(Transacao):
    
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):

        if conta.sacar(self.valor):
            conta.historico.adicionar_transacao(self)

# -----------------------------------

class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor
    
    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        sucesso = conta.depositar(self.valor)

        if sucesso:
            conta.historico.adicionar_transacao(self)


# ---------------- FUNÇÕES DO SISMTE MENU -------------------

def filtrar_cliente(cpf, clientes):
    
    clientes_filtrados = [cliente for cliente in clientes if cliente.cpf == cpf]
    return clientes_filtrados[0] if clientes_filtrados else None

def criar_cliente(clientes):
    cpf = input("Informe o seu CPF (somente números):")

    if filtrar_cliente(cpf, clientes):
        print("\n Atenção: Já existe cliente com esse CPF!")
        return
    
    nome = input("\nInforme o seu nome completo:")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa)")
    endereco = input("Informe o endereço: ")

    # Criamos o objeto usando as variáveis que acabamos de preencher
    cliente = PessoaFisica(nome=nome, data_nascimento=data_nascimento, cpf=cpf, endereco=endereco)
    
    # Guardamos na lista
    clientes.append(cliente)
    print("\n=== Cliente criado com sucesso! ===")

def criar_conta(numero_conta, clientes, contas):

    cpf = input("Digite o seu CPF: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print(">>> Cliente não encontrado!")
        return
    
    conta = ContaCorrente(numero= numero_conta, cliente= cliente)
    contas.append(conta)
    cliente.adicionar_conta(conta)
    print(">>> Conta criada com sucesso!")

def realizar_operacao(clientes, tipo_transacao):
    cpf = input("Digite o seu CPF: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print(">>> Cliente não encontrado!")
        return
    
    valor = float(input("Informe o valor do {tipo_transacao}"))
    transacao = Deposito(valor) if tipo_transacao == "Depósito" else Saque(valor)

    if not cliente.contas:
        print(">>> Cliente não possui conta!")
        return
    
    cliente.realizar_transacao(cliente.contas[0], transacao)


# --------------------------- MENU PRINCIPAL ---------------------------

def menu():
    return """
================ MENU ================
[1] Depositar
[2] Sacar
[3] Extrato
[4] Novo Usuário
[5] Nova Conta
[0] Sair
=> """


def main():
    cliente = []
    contas = []

    while True:
        opcao = input(menu())

        if opcao == "1":
            realizar_operacao(clientes, "Deposito")
        
        elif opcao == "2":
            realizar_operacao(clientes, "Saque")

        elif opcao == "3":
            cpf = input("Informe o seu CPF: ")

            if cliente and cliente.conta:
                print("\n================= EXTRATO =================")

                for t in cliente.contas[0].historico._transacoes:
                    print(t)
                
                print(f"\n>>> Saldo: R$ {cliente.contas[0].saldo:.2f}")

            else:
                print("\n>>> Conta não encontrada! ")
        
        elif opcao == "4":
            criar_cliente(clientes)

        elif opcao == "5":
            numero_conta = len(contas) + 1
            criar_conta(numero_conta, clientes, contas)
        
        elif opcao == "0":
            break
        
        else:
            print(">>> Operação inválida! <<<")