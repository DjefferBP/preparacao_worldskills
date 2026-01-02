import datetime

class Conta:
    
    def __init__(self, saldo_inicial: float):
        if not saldo_inicial:
            raise ValueError("Saldo inicial inválido!")
        if saldo_inicial < 0:
            raise ValueError("Saldo inicial deve ser maior que 0!")
        self._saldo = saldo_inicial
        self._historico = []
        self._extrato_cache = None
    
    @property
    def saldo(self):
        return self._saldo
    
    @property
    def historico(self):
        if self._extrato_cache is None:
            self._extrato_cache = "\n".join(self._historico)
        return self._extrato_cache
            
            
    def registrar_operacao(self, descricao: str):
        timestamp = datetime.datetime.now().strftime("%d/%m/%Y %H:%M/%S")
        self._historico.append(f"[{timestamp}] {descricao}")
        self._extrato_cache = None
    
    def depositar(self, valor_depositado: float):
        if not valor_depositado:
            raise ValueError("Valor deposit ado deve ser válido!")
        if valor_depositado <= 0:
            raise ValueError("Valor depositado deve ser maior que zero!")
        self._saldo += valor_depositado
        self.registrar_operacao(f"Depósito: {valor_depositado}")
        
    def sacar(self, valor_sacado: float):
        if not valor_sacado:
            raise ValueError("Valor sacado deve ser válido!")
        if valor_sacado > self._saldo:
            raise ValueError("Valor sacado é maior que o valor que existe na conta!")
        self._saldo -= valor_sacado
        self.registrar_operacao(f"Saque: {valor_sacado}")
        
    def __str__(self):
        return f"Saldo: {self.saldo} | Operações: {len(self._historico)}"
    
    
try:
    c = Conta(33)
    c.depositar(100)
    c.sacar(50)
    print(c)
    print(c.historico)
except ValueError as e:
    print(e)
except AttributeError as e:
    print(f"Não é possível alterar o saldo diretamente!!")
    