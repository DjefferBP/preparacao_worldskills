

class Idade:
    
    def __init__(self, idade: int):
        self._idade = 0
        self.idade = idade
    
    @property
    def idade(self):
        return self._idade
    
    @idade.setter
    def idade(self, nova_idade: int):
        if nova_idade >= 0 and nova_idade <= 130:
            self._idade = nova_idade

        print("Idade inválida!")

        
        
idade = Idade(5)
idade.idade = 88
idade.idade = -1




class Temperatura:
    
    def __init__(self, celsius: int):
        self._celsius = 0
        self.celsius = celsius
    
    @property
    def celsius(self):
        return self._celsius
    
    @celsius.setter
    def celsius(self, graus_celsius: int):
        if graus_celsius >= -50 and graus_celsius <= 100:
            self._celsius = graus_celsius
        print("Temperatura inválida!")
        
temp = Temperatura(50)
temp.celsius = 11
temp.celsius = 111


class Nome:
    
    def __init__(self, nome: str):
        self._nome = ""
        self.nome = nome
        
    @property
    def nome(self):
        return self._nome
    
    @nome.setter
    def nome(self, nome: str):
        self._nome = nome.strip().lower().capitalize()
    
nome = Nome("Djeffer")
nome.nome = "roDRigo"
print(nome.nome)
nome.nome = "MArciCÓ"
print(nome.nome)


class Retangulo:
    
    def __init__(self, largura: float, altura: float):
        self._altura = 0
        self._largura = 0
        self.largura = largura
        self.altura = altura
    @property
    def largura(self):
        return self._largura

    @largura.setter
    def largura(self, valor):
        if valor > 0:
            self._largura = valor
        else:
            raise ValueError("Largura inválida")

    @property
    def altura(self):
        return self._altura

    @altura.setter
    def altura(self, valor):
        if valor > 0:
            self._altura = valor
        else:
            raise ValueError("Altura inválida")
        
    @property
    def area(self):
        return self._altura * self._largura
    
retangulo = Retangulo(56, 12)
print(retangulo.area)


class ContaBancaria:
    
    def __init__(self, saldo_inicial: float):
        self._saldo = 0
        self.saldo = saldo_inicial
        
        
    @property
    def saldo(self):
        return self._saldo
    
    @saldo.setter
    def saldo(self, saldo_inicial: float):
        if saldo_inicial >= 0:
            self._saldo = saldo_inicial
        else:
            raise ValueError("Saldo inicial inválido!")
            
    def depositar(self, valor: float):
        if valor <= 0:
            print("Você deve depositar um valor maior que 0!")
            return
        self._saldo += valor
        
    def sacar(self, valor: float):
        if valor <= 0:
            print("O valor a ser sacado deve ser maior que 0!")
            return
        if valor > self._saldo:
            print("Este valor ultrapassa o valor disponível para saque!")
            return
        self._saldo -= valor
        
    def __str__(self):
        return f"Saldo disponível: {self._saldo}"
    
try:
    conta = ContaBancaria(-3)
    conta.depositar(60)
    conta.sacar(300)
    print(conta)
except ValueError as e:
    print(f"Erro: {e}")
