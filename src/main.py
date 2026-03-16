from abc import ABC, abstractmethod
from datetime import datetime

class Cliente:
    # caracteristicas
    #contrutor inicializador:
    def __init__(self, endereco):
        self.__endereco = endereco
        self.__contas = []

    # atributos
    def adicionar_conta(self, conta):
        self.__contas.append(conta)
        print("Conta adicionada ao cliente com sucesso!")

    def listar_contas(self):
        return self.__contas
    
# -----------------------------------

class PessoaFisica(Cliente):
    def __init__(self, endereco, cpf, nome):
        super().__init__(endereco)
        self.__cpf = cpf
        self.__nome = nome
        self.__data_nascimento = datetime
    pass

# -----------------------------------

class Conta:
    def __init__(self, numero, agencia, cliente, historico):
        self.__saldo = 0.0
        self.__numero = numero
        self.__agencia = agencia
        self.__cliente = cliente
        self.__historico = []

    
    @property
    def saldo(self):
        return self.__saldo
    
    @classmethod
    def nova_conta(cls, cliente, numero, agencia):
        return cls(cliente, numero, agencia)

    def sacar(self, valor):
        if valor > 0 and valor <= self.__saldo:
            self.__saldo -= valor
            print(f"Saque de R${valor} realizado.")
            return True
        print("Saldo insuficiente ou valor inválido.")
        return False
    
    def depositar(self, valor):
        if valor > 0:
            self.__saldo += valor
            print(f"Depósito de R${valor} realizado.")
            return True
        return False
    
# -----------------------------------
    

class ContaCorrente(Conta):
    def __init__(self, saldo, numero, agencia, Cliente, Historico, limite, limite_saques):
        super().__init__(saldo, numero, agencia, Cliente, Historico)
        self.__limite = limite
        self.__limite_saques = limite_saques
    pass
    
# -----------------------------------

class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes
    
    def adicionar_transacao(self, transacao):
        self._transacoes.append({
            "tipo": transacao.__classe__.__name__ ,
            "valor": transacao.valor,
            "data": datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        })

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
        sucesso = conta.sacar(self.valor)

        if sucesso:
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
