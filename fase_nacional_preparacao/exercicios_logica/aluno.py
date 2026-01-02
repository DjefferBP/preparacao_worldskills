

class Nota:
    
    def __init__(self, nota: float):
        self._nota = 0
        self.nota = nota
    
    @property
    def nota(self):
        return self._nota
    
    @nota.setter
    def nota(self, valor: float):
        if valor >= 0:
            self._nota = valor
        else:
            print("Nota Inválida!")
            
            
nota = Nota(55)
nota.nota = 3
nota.nota = -3