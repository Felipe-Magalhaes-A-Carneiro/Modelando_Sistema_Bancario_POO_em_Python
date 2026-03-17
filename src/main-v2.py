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

    def criar_cliente(clientes):
        cpf = input("Informe o seu CPF (somente números):")

        if cpf in clientes:
            print("\n Atenção: Já existe cliente com esse CPF!")
            return
        
        nome = input("\nInforme o seu nome completo:")
        data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa)")
        endereco = input("Informe o endereço: ")

        # Criamos o objeto usando as variáveis que acabamos de preencher
        novo_cliente = PessoaFisica(nome=nome, data_nascimento=data_nascimento, cpf=cpf, endereco=endereco)
        
        # Guardamos na lista
        clientes.append(novo_cliente)
        print("\n=== Cliente criado com sucesso! ===")

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
