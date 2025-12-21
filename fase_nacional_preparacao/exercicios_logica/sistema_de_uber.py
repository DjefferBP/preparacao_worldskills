from datetime import datetime
import math
import random
from enum import Enum
import uuid
from collections import deque

## FOI UTILIZADO IA PARA RETIRAR DÚVIDAS, PARA A FUNÇÃO DE ENCONTRAR MOTORISTA MAIS PRÓXIMO, E PARA FAZER TESTES.


def calcular_distancia(ponto1, ponto2):
    return math.sqrt((ponto2[0] - ponto1[0])**2 + (ponto2[1] - ponto1[1])**2)

class Constantes(Enum):
    BANDEIRADA = 5.00
    KM = 2.50
    POR_MINUTO = 0.50

class StatusMotorista(Enum):
    DISPONIVEL = True
    INDISPONIVEL = False

class Passageiro:
    def __init__(self, nome: str, saldo: float):
        self.nome = nome
        self.posicao = (0, 0)
        self.saldo = saldo
        
    def adicionar_saldo(self, valor: float):
        print(f"R${valor:.2f} adicionado à {self.nome}")
        return self.saldo + valor
    
    def decrementar_saldo(self, valor: float):
        print(f"Você gastou R${valor:.2f} nessa corrida.")
        return self.saldo - valor

class Motorista:
    def __init__(self, nome: str, posicao_motorista: tuple):
        self.nome = nome
        self.posicao = posicao_motorista
        self.disponivel = StatusMotorista.DISPONIVEL.value
        self.corridas_realizadas = 0

class Uber():
    def __init__(self):
        self.corridas_em_andamento = deque()
        self.todos_passageiros = []
        self.todos_motoristas = []
        
    def adicionar_motorista(self, motorista: object):
        if not isinstance(motorista, Motorista):
            print("Este usuário não pertence a classe de motorista!")
            return
        
        if motorista in self.todos_motoristas:
            print("Este motorista já está cadastrado!")
            return
        
        self.todos_motoristas.append(motorista)
        print("Motorista", motorista.nome, "adicionado com sucesso!")
    
    def adicionar_passageiro(self, passageiro: object):
        if not isinstance(passageiro, Passageiro):
            print("Este usuário não pertence a classe de passageiro!")
            return
        
        if passageiro in self.todos_passageiros:
            print("Este passageiro já está cadastrado!")
            return
        
        self.todos_passageiros.append(passageiro)
        print("passageiro", passageiro.nome, "adicionado com sucesso!")
        
    def solicitar_corrida(self, passageiro: object, destino: tuple):
        if not isinstance(passageiro, Passageiro):
            print("Este usuário não pertence a classe de passageiro!")
            return
        
        if passageiro not in self.todos_passageiros:
            print("Este passageiro não está cadastrado!")
            return

        posicao_pas = passageiro.posicao
        motoristas_disponiveis = []
        for motorista in self.todos_motoristas:
            if motorista.disponivel != StatusMotorista.DISPONIVEL.value:
                continue
            motoristas_disponiveis.append(motorista)
            
        motorista_mais_proximo, distancia_ate_passageiro = self.encontrar_motorista_mais_proximo(posicao_pas, motoristas_disponiveis)
        if not motorista_mais_proximo:
            print("Não foi encontrado nenhum motorista próximo a você para a corrida!")
            return
        destino_km = calcular_distancia(passageiro.posicao, destino)
        
        if distancia_ate_passageiro < 0:
            print(f"Erro ao calcular a distância até o passageiro. Valor atual: {distancia_ate_passageiro}")
            return
        
        self.marcar_indisponibilidade_motorista(motorista_mais_proximo)
        
        total_tempo = 0
        total_valor = 0
        tempo_ate_passageiro = (distancia_ate_passageiro / 60) * 60
        tempo_ate_destino = (destino_km / 60) * 60

        distancia_total = destino_km + distancia_ate_passageiro
        total_tempo = tempo_ate_passageiro = tempo_ate_destino
        valor_corrida = (Constantes.KM.value * distancia_total) + (Constantes.POR_MINUTO.value * total_tempo) + Constantes.BANDEIRADA.value
        
        if passageiro.saldo < valor_corrida:
            print("Você não tem saldo o suficiente para conseguir pagar esta corrida!")
            return
        
        motorista_mais_proximo.posicao = destino
        corrida = Corrida(passageiro, motorista_mais_proximo, destino, distancia_total, distancia_ate_passageiro, total_tempo, valor_corrida)
        passageiro.decrementar_saldo(valor_corrida)
        passageiro.posicao = destino
        self.corridas_em_andamento.append(corrida)

        print("CORRIDA SOLICITADA COM SUCESSO!")
        print(f"Passageiro: {passageiro.nome} | Motorista: {motorista_mais_proximo.nome} | Valor: R${valor_corrida:.2f} | Distância total: {distancia_total:.2f}km | Tempo estimado: {total_tempo:.2f}min")

        
    def marcar_indisponibilidade_motorista(self, motorista: object) -> bool:
        motorista.disponibilidade = StatusMotorista.INDISPONIVEL.value
    
    def marcar_disponibilidade_motorista(self, motorista: object) -> bool:
        motorista.disponibilidade = StatusMotorista.DISPONIVEL.value
    
    def encontrar_motorista_mais_proximo(self, passageiro_pos: tuple, motoristas_disponiveis: list, raio_max=10.0):
        mais_proximo = None
        menor_distancia = float('inf')
        
        for motorista in motoristas_disponiveis:
            distancia = calcular_distancia(passageiro_pos, motorista.posicao)
            
            if distancia <= raio_max and distancia < menor_distancia:
                menor_distancia = distancia
                mais_proximo = motorista
        
        return mais_proximo, menor_distancia if mais_proximo else None
    
    
    def ver_corridas_em_andamento(self):
        if not self.corridas_em_andamento:
            print("Não há corridas em andamento")
            return
        
        for corrida in self.corridas_em_andamento:
            data_corrida = datetime.strftime(corrida.data_solicitacao, "DIA: %d MÊS %m ANO: %Y ás %H:%M:%S")
            print(f"Motorista: {corrida.motorista.nome}\nPassageiro: {corrida.passageiro.nome}\n === INFORMAÇÕES DA CORRIDA ==="\
                f"\nPosição do passageiro: {corrida.origem}\nDestino: {corrida.destino}\nDistância total da corrida: {corrida.distancia:.2f}km\n"\
                    f"Distância até o passageiro: {corrida.distancia_ate_passsageiro:.2f}km\nTempo total da corrida estimado: {corrida.tempo:.2f}min\n"\
                        "Valor da corrida: R${0:.2f}\nDATA SOLICITADA: {1}".format(corrida.valor, data_corrida))
    
    
class Corrida():
    def __init__(self, passageiro, motorista, destino, distancia, distancia_ate_passageiro, tempo, valor):
        self.id = str(uuid.uuid4())[:8]
        self.passageiro = passageiro
        self.motorista = motorista
        self.origem = passageiro.posicao
        self.destino = destino
        self.distancia = distancia
        self.distancia_ate_passsageiro = distancia_ate_passageiro
        self.tempo = tempo
        self.valor = valor
        self.data_solicitacao = datetime.now()
        

pas1 = Passageiro("Misael", 60)
pas2 = Passageiro("Gabriel Henrique Machado", 30)

motorista1 = Motorista("Daniel Fugibosta", (1, 3))
motorista2 = Motorista("Saulo Correa", (1, 2))

uber = Uber()
uber.adicionar_motorista(motorista1)
uber.adicionar_motorista(motorista2)

uber.adicionar_passageiro(pas1)
uber.adicionar_passageiro(pas2)

print("\n" + "="*60)

motoristas_extras = [
    Motorista("Carlos Silva", (2, 3)),
    Motorista("Ana Santos", (5, 1)),
    Motorista("Paulo Costa", (7, 2)),
    Motorista("Fernanda Lima", (4, 6)),
    Motorista("Roberto Alves", (1, 4))
]

passageiros_extras = [
    Passageiro("Mariana", 100.0),
    Passageiro("Ricardo", 50.0),
    Passageiro("Juliana", 200.0),
    Passageiro("Felipe", 30.0),
    Passageiro("Camila", 150.0)
]

for motorista in motoristas_extras:
    uber.adicionar_motorista(motorista)

for passageiro in passageiros_extras:
    uber.adicionar_passageiro(passageiro)

print(f"\nTotal motoristas: {len(uber.todos_motoristas)}")
print(f"Total passageiros: {len(uber.todos_passageiros)}")

print("\n" + "="*60)

destinos = [
    (10, 10),
    (3, 5),
    (8, 2),
    (6, 7),
    (2, 9)
]

print(f"\n1. Mariana → (10, 10):")
uber.solicitar_corrida(passageiros_extras[0], destinos[0])

print(f"\n2. Ricardo → (3, 5):")
uber.solicitar_corrida(passageiros_extras[1], destinos[1])

print(f"\n3. Juliana → (8, 2):")
uber.solicitar_corrida(passageiros_extras[2], destinos[2])

print(f"\nCorridas em andamento: {len(uber.corridas_em_andamento)}")

print("\n" + "="*60)

print(f"\nFelipe tem R${passageiros_extras[3].saldo:.2f}")
uber.solicitar_corrida(passageiros_extras[3], (15, 15))

print("\n1. Camila solicita corrida...")
uber.solicitar_corrida(passageiros_extras[4], (5, 5))

print("\n2. Tentando usar motorista ocupado...")

pas_test = Passageiro("Teste", 100.0)
uber.adicionar_passageiro(pas_test)
uber.solicitar_corrida(pas_test, (2, 2))

print("\n" + "="*60)

print(f"\nTotal de corridas ativas: {len(uber.corridas_em_andamento)}")

if uber.corridas_em_andamento:
    uber.ver_corridas_em_andamento()
    
    print(f"\nESTATÍSTICAS DAS CORRIDAS:")
    total_valor = sum(c.valor for c in uber.corridas_em_andamento)
    total_distancia = sum(c.distancia for c in uber.corridas_em_andamento)
    total_tempo = sum(c.tempo for c in uber.corridas_em_andamento)
    
    print(f"   Valor total em corridas: R${total_valor:.2f}")
    print(f"   Distância total: {total_distancia:.2f}km")
    print(f"   Tempo total estimado: {total_tempo:.1f}min")
    print(f"   Passageiros ativos: {len(set(c.passageiro for c in uber.corridas_em_andamento))}")
    print(f"   Motoristas ativos: {len(set(c.motorista for c in uber.corridas_em_andamento))}")
else:
    print("Nenhuma corrida em andamento para mostrar.")
    
print("\n" + "="*60)

def concluir_corrida_test(sistema, corrida_index=0):
    if not sistema.corridas_em_andamento:
        print("Nenhuma corrida para concluir")
        return
    
    if corrida_index >= len(sistema.corridas_em_andamento):
        print("Índice inválido")
        return
    
    corrida = sistema.corridas_em_andamento[corrida_index]
    
    print(f"\nCONCLUINDO CORRIDA:")
    print(f"   ID: {corrida.id}")
    print(f"   Passageiro: {corrida.passageiro.nome}")
    print(f"   Motorista: {corrida.motorista.nome}")
    print(f"   Valor: R${corrida.valor:.2f}")
    
    corrida.motorista.disponivel = True
    print(f"   Motorista {corrida.motorista.nome} liberado!")
    
    sistema.corridas_em_andamento.remove(corrida)
    print(f"Corrida concluída com sucesso!")

print("\nConcluindo 2 corridas...")
if len(uber.corridas_em_andamento) >= 2:
    concluir_corrida_test(uber, 0)
    concluir_corrida_test(uber, 0)
    
print(f"\nCorridas restantes: {len(uber.corridas_em_andamento)}")

print("\n" + "="*60)

print("\n1. Passageiro não cadastrado:")
pas_fantasma = Passageiro("Fantasma", 100.0)
uber.solicitar_corrida(pas_fantasma, (1, 1))

print("\n2. Destino igual à origem:")
pas_test2 = Passageiro("Teste2", 100.0)
uber.adicionar_passageiro(pas_test2)
pas_test2.posicao = (5, 5)
uber.solicitar_corrida(pas_test2, (5, 5))

print("\n3. Coordenadas negativas:")
uber.solicitar_corrida(pas_test2, (-5, -10))

print("\n4. Motorista com disponibilidade None:")
motorista_estranho = Motorista("Estranho", (3, 3))
motorista_estranho.disponivel = None
uber.adicionar_motorista(motorista_estranho)

print("\n5. Passageiro com saldo negativo:")
pas_sem_grana = Passageiro("Sem Grana", -10.0)
uber.adicionar_passageiro(pas_sem_grana)
uber.solicitar_corrida(pas_sem_grana, (2, 2))

print("\n" + "="*60)

import time

print("\nTestando 10 solicitações rápidas...")

for motorista in uber.todos_motoristas:
    motorista.disponivel = True

solicitacoes_realizadas = 0
inicio = time.time()

for i in range(10):
    pas_temp = Passageiro(f"Temp{i}", 100.0)
    pas_temp.posicao = (random.randint(0, 10), random.randint(0, 10))
    uber.adicionar_passageiro(pas_temp)
    
    destino = (random.randint(0, 15), random.randint(0, 15))
    
    print(f"\n{i+1}. {pas_temp.nome} → {destino}")
    resultado = uber.solicitar_corrida(pas_temp, destino)
    
    if resultado and "SUCESSO" in str(resultado):
        solicitacoes_realizadas += 1

fim = time.time()
tempo_total = fim - inicio

print(f"\nRESULTADO DO TESTE DE PERFORMANCE:")
print(f"   Tempo total: {tempo_total:.2f} segundos")
print(f"   Solicitações: 10 tentadas")
print(f"   Sucessos: {solicitacoes_realizadas}")
print(f"   Tempo médio por solicitação: {tempo_total/10:.3f}s")
print(f"   Corridas ativas: {len(uber.corridas_em_andamento)}")

print("\n" + "="*60)

print(f"\nESTADO FINAL APÓS TODOS OS TESTES:")

print(f"\nESTATÍSTICAS GERAIS:")
print(f"   Total motoristas: {len(uber.todos_motoristas)}")
print(f"   Total passageiros: {len(uber.todos_passageiros)}")
print(f"   Corridas em andamento: {len(uber.corridas_em_andamento)}")

motoristas_disponiveis = sum(1 for m in uber.todos_motoristas if m.disponivel)
print(f"   Motoristas disponíveis: {motoristas_disponiveis}")
print(f"   Motoristas ocupados: {len(uber.todos_motoristas) - motoristas_disponiveis}")

if uber.todos_passageiros:
    saldo_medio = sum(p.saldo for p in uber.todos_passageiros) / len(uber.todos_passageiros)
    print(f"   Saldo médio passageiros: R${saldo_medio:.2f}")

print(f"\nÚLTIMA VERIFICAÇÃO DAS CORRIDAS:")
uber.ver_corridas_em_andamento()

print("\n" + "="*60)
print("TODOS OS TESTES CONCLUÍDOS!")
print("="*60)