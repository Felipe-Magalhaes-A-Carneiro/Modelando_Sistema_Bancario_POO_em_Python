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
    def __init__(self, nome, data_nascimento, cpf, endereco):
        super().__init__(endereco)
        self.__nome = nome
        self.__data_nascimento = data_nascimento
        self.__cpf = cpf


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
    def __init__(self, numero, cliente, limite = 500, limite_saques = 3):
        super().__init__(numero, cliente)
        self.limite = limite
        self.limite_saques = limite_saques

        # Sobrescreve o método sacar para incluir regras de limite de cheque especial:

        def sacar(self, valor):
            # Limite e número de saques
            return super().sacar(valor)
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
