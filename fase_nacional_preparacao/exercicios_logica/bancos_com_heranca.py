from abc import ABC, abstractmethod
from datetime import datetime

class Transacao:
    def __init__(self, tipo: str, valor: float):
        self.data = datetime.now()
        self.tipo = tipo
        self.valor = valor
    
class Historico:
    
    def __init__(self):
        self.transacoes: list[Transacao] = []
    
    def adicionar(self, transacao: Transacao):
        self.transacoes.append(transacao)
    
    def gerar_extrato(self) -> str:
        linhas = []
        for t in self.transacoes:
            data = t.data.strftime("%d/%m/%Y %H:%M:%S")
            linhas.append(f"[{data}] | {t.tipo} | R${t.valor:.2f}")
        transacoes = "\n".join(linhas)
        return transacoes
    
class Conta(ABC):
    
    def __init__(self, saldo: float):
        if saldo < 0:
            raise ValueError("Saldo inicial não deve ser negativo!")
        self._saldo = saldo
        self._historico = Historico()
        self._extrato_cache = None
        
    @property
    def saldo(self):
        return self._saldo
    
    @property
    def ver_extrato(self):
        if self._extrato_cache is None:
            self._extrato_cache = self._historico.gerar_extrato()
        return self._extrato_cache
    
    @abstractmethod
    def sacar(self, valor: float):
        pass
    
    def depositar(self, valor: float):
        if valor <= 0:
            raise ValueError("Não é possível depositar um valor negativo!")
        self._saldo += valor
        self.registrar_operacao("deposito", valor)
    
    def registrar_operacao(self, tipo: str, valor: float):
        self._historico.adicionar(Transacao(tipo, valor))
        self._extrato_cache = None
    
    def __str__(self):
        return f"Saldo: R${self._saldo} | Registros: {len(self._historico.transacoes)}"
    
class ContaCorrente(Conta):
    
    def __init__(self, saldo, limite: float):
        super().__init__(saldo)
        self._limite = limite
    
    @property
    def limite(self):
        return self._limite

    def sacar(self, valor: float):
        if valor <= 0:
            raise ValueError("Não é possível sacar um valor negativo!")

        if valor > self._saldo + self._limite:
            raise ValueError("Não é possível sacar mais dinheiro! Você atingiu o limite da sua conta!")
        self._saldo -= valor
        self.registrar_operacao("saque", valor)
    

    
    
class ContaPoupanca(Conta):
    
    def __init__(self, saldo):
        super().__init__(saldo)
        
    def sacar(self, valor: float):
        if valor <= 0:
            raise ValueError("Não é possível sacar um valor negativo!")
        if valor > self._saldo:
            raise ValueError("Você não tem saldo suficiente para sacar!")
        self._saldo -= valor
        self.registrar_operacao("saque", valor)

def executar_operacao(conta: Conta, operacao: str, valor: float):
    if operacao == "depositar":
        conta.depositar(valor)
        return
    elif operacao == "sacar":
        conta.sacar(valor)
        return
    else:
        raise ValueError("Esta operação não está disponível!")
    


try:
    cr = ContaCorrente(400, 300)
    cp = ContaPoupanca(700)
    cr.sacar(30)
    cr.depositar(700)
    cr.sacar(300)
    print(cr.ver_extrato)
    cp.depositar(400)
    cp.depositar(30)
    cp.sacar(600)
    print(cp, "\n=====================\n")
    executar_operacao(cp, "depositar", 40)
    print(cp.ver_extrato)
except ValueError as e:
    print(e)
    