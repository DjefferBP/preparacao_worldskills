import unittest
from bancos_com_heranca import ContaCorrente, ContaPoupanca

class TestConta(unittest.TestCase):
    def test_saque_valido(self):
        cc = ContaCorrente(100, limite=200)
        cc.sacar(250)  
        self.assertEqual(cc.saldo, -150)
        
    def test_saque_excede_limite(self):
        cc = ContaCorrente(100, limite=200)
        with self.assertRaises(ValueError):
            cc.sacar(400)
            
    

class TestContaPoupanca(unittest.TestCase):

    def test_saque_invalido(self):
        cp = ContaPoupanca(100)
        with self.assertRaises(ValueError):
            cp.sacar(150)

    def test_deposito_invalido(self):
        cp = ContaPoupanca(100)
        with self.assertRaises(ValueError):
            cp.depositar(-50)

