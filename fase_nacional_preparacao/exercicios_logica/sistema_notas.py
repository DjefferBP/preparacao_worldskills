class Aluno:
    def __init__(self, nome: str, idade: int, nota: float):
        self.nome = nome
        self.idade = idade
        self.nota = nota
    def __str__(self):
        return f"{self.nome} | Idade: {self.idade} | Nota: {self.nota}"
class Turmas:
    def __init__(self, serie: str, turma: str, periodo: str):
        self.serie = serie
        self.turma = turma
        self.periodo = periodo
        self.alunos = []
    def __str__(self):
        texto = f"Série: {self.serie} | Turma: {self.turma} | Período: {self.periodo}| Alunos da turma {self.serie}°{self.turma}:"
        for aluno in self.alunos:
            texto += f"\n{aluno}"
        return texto
    def adicionar_aluno(self, aluno: object) -> bool:
        if isinstance(aluno, Aluno):
            self.alunos.append(aluno)
            return True
        return False
    def calcular_media_geral_da_turma(self):
        notas = 0
        if not self.alunos:
            print("Não há alunos na turma!")
            return
        for aluno in self.alunos:
            notas += aluno.nota
        media = notas / len(self.alunos)
        print(f"A média geral da turma {self.serie}°{self.turma} é: {media:.2f}.")
        
    def melhor_aluno(self) -> object:
        melhor_aluno = self.alunos[0]
        for aluno in self.alunos:
            if aluno.nota > melhor_aluno.nota:
                melhor_aluno = aluno
        aluno_melhor = {
            "Turma": f"{self.serie}°{self.turma}",
            "Melhor aluno:" : melhor_aluno
        }
        return aluno_melhor
        
class SistemaNotas:
    def __init__(self):
        self.turmas = []
    def adicionar_turma(self, turma: object) -> bool:
        if isinstance(turma, Turmas):
            self.turmas.append(turma)
            return True
        return False
    
    def verificar_melhor_aluno_entre_turmas(self) -> list:
        if not self.turmas:
            print("Não há nenhuma turma para ser verificada!")
            return
        melhores_alunos = []
        
        for turma in self.turmas:
            melhor_aluno = turma.melhor_aluno()
            melhores_alunos.append(melhor_aluno)
        
        return melhores_alunos
    
    def mostrar_melhores_alunos(self):
        print("==== MELHORES ALUNOS DE CADA TURMA ====")
        melhores_alunos = self.verificar_melhor_aluno_entre_turmas()
        for aluno in melhores_alunos:
            for key, value in aluno.items():
                print(key, value)
            print("=====")
        
aluno1 = Aluno("João", 16, 8.5)
aluno2 = Aluno("Maria", 15, 9.2)
aluno3 = Aluno("Pedro", 16, 6.8)
aluno4 = Aluno("Ana", 17, 9.8)
aluno5 = Aluno("Lucas", 16, 7.4)
aluno6 = Aluno("Beatriz", 15, 8.9)
# ==== CRIANDO TURMAS ====
turma1 = Turmas("1", "A", "Manhã")
turma2 = Turmas("2", "B", "Tarde")
# ==== ADICIONANDO ALUNOS NAS TURMAS ====
turma1.adicionar_aluno(aluno1)
turma1.adicionar_aluno(aluno2)
turma1.adicionar_aluno(aluno3)
turma2.adicionar_aluno(aluno4)
turma2.adicionar_aluno(aluno5)
turma2.adicionar_aluno(aluno6)
# ==== CRIANDO SISTEMA ====
sistema = SistemaNotas()
# ==== ADICIONANDO TURMAS NO SISTEMA ====
sistema.adicionar_turma(turma1)
sistema.adicionar_turma(turma2)
print(turma1)
print(turma2)
turma1.calcular_media_geral_da_turma()
turma2.calcular_media_geral_da_turma()
print()
sistema.mostrar_melhores_alunos()