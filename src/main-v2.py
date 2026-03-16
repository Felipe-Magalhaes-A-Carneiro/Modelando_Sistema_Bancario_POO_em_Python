from abc import ABC, abstractmethod
from datetime import datetime

# VERSÃO 2 = Utilizando INPUTS

clientes = []
contas = []

class Cliente:
    # caracteristicas
    #contrutor inicializador:
    def __init__(self, endereco):
        self.__endereco = endereco
        self.__contas = []

    # atributos
    def adicionar_conta(self, conta):
        self.__contas.append(conta)
        print("\nConta adicionada ao cliente com sucesso!")

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
    
    @classmethod
    def nova_conta(cls, cliente, numero, agencia):
        return cls(cliente, numero, agencia)

    def sacar(self, valor):
        if valor > 0 and valor <= self.__saldo:
            self.__saldo -= valor
            print(f"\nSaque de R${valor} realizado.")
            return True
        print("\nSaldo insuficiente ou valor inválido.")
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

        # Sobrescreve o método sacar para incluir regras de limite de cheque especial:

        def sacar(self, valor):
            # Limite e número de saques
            return super().sacar(valor)
    pass
    
# -----------------------------------

class Historico:
    def __init__(self, arquivo = "historico.txt"):
        self.arquivo = arquivo
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes
    
    # Persistência de Dados em .txt
    def _carregar_do_disco(self):
        try:
            with open(self.arquivo, "alteracao") as f:
                return [linha.strip() for linha in f.readlines()]
        except FileNotFoundError:
            return []
    
    # def adicionar_transacao(self, transacao):
    #     self._transacoes.append({
    #         "tipo": transacao.__class__.__name__ ,
    #         "valor": transacao.valor,
    #         "data": datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    #     })

    def adicionar_transacao(self, transacao):
        data_hora = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        registro = f"{data_hora} - {transacao.__class__.__name__}: R${transacao.valor:.2f}"

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


# --- EXECUÇÃO ---

# 1. Criando o Cliente (Pessoa Física):
novo_cliente = PessoaFisica(nome = nome, data_nascimento= data_nascimento,  cpf = cpf, endereco = endereco)

# 2. Criando a Conta Corrente e vinculando ao cliente:
conta = ContaCorrente(numero = 1, cliente =  novo_cliente )
novo_cliente .adicionar_conta(conta)

# 3. Ralizando Depósito:
deposito = Deposito(1000.0)
novo_cliente .realizar_transacao(conta, deposito)

# 4. Realizando um Saque:
saque = Saque(55.0)
novo_cliente .realizar_transacao(conta, saque)

# 5. Exibindo o resultado final:
print(f"""
Cliente: {novo_cliente.nome}

Saldo Atual: R${conta.saldo:.2f}

---> Extrato em 'historico.txt' foi atualizado
""")
