from abc import ABC, abstractmethod
import datetime
import random
import time

class Acoes:
    
    def __init__(self, acao, descricao, horario_aconteceu=None, rodada=None):
        self.data = datetime.datetime.now()
        self.acao = acao
        self.descricao = descricao
        self.horario_aconteceu = horario_aconteceu
        self.rodada = rodada
        
class Historico:
    def __init__(self):
        self.historicos_acoes: list[Acoes] = []
        
    def adicionar(self, acao: Acoes):
        self.historicos_acoes.append(acao)
        
    def gerar_historico(self):
        linhas = []
        for acao in self.historicos_acoes:
            if acao.acao == "batalha":
                linhas.append(f"RODADA: {acao.rodada}\n[{acao.horario_aconteceu}] {acao.acao.capitalize()} | {acao.descricao}")
            else:
                data_aconteceu = acao.data.strftime("%d/%m/%Y %H:%M:%S")
                linhas.append(
                    f"[{data_aconteceu}] {acao.acao.capitalize()} | {acao.descricao}"
                )
        return linhas

class Personagem(ABC):
    
    def __init__(self, nome: str, vida: float, vida_max: float):
        self._nome = nome
        self._vida = vida
        self._vida_max = vida_max
        self.historico = Historico()
        self._total_dano_causado = 0
        
    @property
    def vida(self):
        return self._vida
    
    @property
    def nome(self):
        return self._nome
    
    @property
    def vida_max(self):
        return self._vida_max
    
    @property
    def total_dano_causado(self):
        return self._total_dano_causado
    
    @total_dano_causado.setter
    def total_dano_causado(self, dano: float):
        self._total_dano_causado += dano
    
    def receber_dano(self, valor):
        if valor <= 0:
            return
        
        self._vida = max(0, self._vida - valor)
        
        self.historico.adicionar(
            Acoes("recebeu_dano", f"{self._nome} recebeu {valor:.2f} de dano!")
        
        )

        if not self.esta_vivo():
            self.historico.adicionar(
                Acoes("morreu", f"{self._nome} morreu!")
            )
        
    def esta_vivo(self) -> bool:
        return self._vida > 0
    
    @abstractmethod
    def atacar(self, alvo: "Personagem"):
        pass    
    
    @property
    def ver_historico_de_batalha(self):
        print(f"HISTÓRICO DE BATALHA DO PERSONAGEM: {self.nome}")
        historico = self.historico.gerar_historico()
        return "\n".join(historico)
    
class Guerreiro(Personagem):
    
    def __init__(self, nome, vida, vida_max, forca: float):
        super().__init__(nome, vida, vida_max)
        if forca < 30 and forca > 45:
            raise ValueError("A força do personagem deve ser no mínimo 30 e máximo 45.")
        self._forca = forca
    
    @property
    def forca(self):
        return self._forca
    
    @property
    def dano(self):
        return self._forca * 2

    def atacar(self, alvo: "Personagem") -> float:
        self.historico.adicionar(
            Acoes("atacou", f"Atacou o personagem: {alvo.nome} e causou {self.dano:.2f} de dano.")
        )
        
        alvo.receber_dano(self.dano)
        return self.dano


class Mago(Personagem):
    CUSTO_DE_MANA = 25
    MULTIPLICADOR_DE_DANO = 3
    RECUPERAR_MANA = 10
    
    def __init__(self, nome, vida, vida_max, mana: int, poder_magico: float):
        super().__init__(nome, vida, vida_max)
        if mana < 50 and mana > 150:
            raise ValueError("Mana mínima deve ser 50 e máxima de 150.")
        self._mana = mana
        if poder_magico < 15 and poder_magico > 20:
            raise ValueError("O poder mágico mínimo deve ser 15 e máximo de 20.")
        self._poder_magico = poder_magico
        
    
    @property
    def vida_recupera(self):
        return self._vida
    
    @vida_recupera.setter
    def vida_recupera(self):
        self._mana += self.RECUPERAR_MANA  
    
    @property
    def mana(self):
        return self._mana
    
    @property
    def dano(self):
        return self._poder_magico * self.MULTIPLICADOR_DE_DANO
    
    @property
    def recuperar_mana(self):
        self._mana += self.RECUPERAR_MANA
    
    def atacar(self, alvo: "Personagem") -> float:
        if self.mana < self.CUSTO_DE_MANA:
            print(f"{self.nome} não tem mana suficiente para atacar!.")
            return
        self._mana -= self.CUSTO_DE_MANA
        
        self.historico.adicionar(
            Acoes("atacou", f"Atacou o personagem: {alvo.nome} e causou {self.dano:.2f} de dano.")
        )
        self.total_dano_causado += self.dano

        alvo.receber_dano(self.dano)
        self.recuperar_mana
        return self.dano

class Arqueiro(Personagem):
    CHANCE_DE_CRITICO = 0.3
    DANO_CRITICO = 1.5
    
    def __init__(self, nome, vida, vida_max, dano_variavel: float):
        super().__init__(nome, vida, vida_max)
        if dano_variavel < 20 or dano_variavel > 50:
            raise ValueError("Dano mínimo deve ser 20 e no máximo 50!.")
        self._dano_variavel = dano_variavel
        
    

    @property
    def dano(self):
        valor = random.randint(-10, 10)
        chance = random.random()
        if self.CHANCE_DE_CRITICO > chance:
            return (self._dano_variavel + valor) * self.DANO_CRITICO
        return self._dano_variavel + valor
    
    def atacar(self, alvo: "Personagem") -> float:
        dano = self.dano
        self.historico.adicionar(
            Acoes("atacou", f"Atacou o personagem: {alvo.nome} causando {dano:.2f} de dano!.")
        )
        self.total_dano_causado += dano
        alvo.receber_dano(dano)
        return dano

class Equipes:
    def __init__(self, nome,  per1, per2, per3):
        self._nome = nome
        self.equipe = [per1, per2, per3]
        self.seu_turno = False
    
    @property
    def vivos(self):
        return [p for p in self.equipe if p.esta_vivo()]
    
    @property
    def nome(self):
        return self._nome


class Batalha:
    def __init__(self, time_a, time_b):
        self.time_a = time_a
        self.time_b = time_b
        self.vencedor = None
        self._rodada = 1
        self._historico = Historico()
        self.comecou = datetime.datetime.now()
        self.quantidade_de_personagens_que_morreram = 0
        self.jogo()
        
    @property
    def rodada(self):
        return self._rodada
    
    @rodada.setter
    def rodada(self, valor: int):
        if valor <= 0 and valor > 1:
            raise ValueError("A próxima rodada deve ser incrementada em 1!")
        return self._rodada
    
    @property
    def decidir_de_quem_e_a_vez(self):
        if self._rodada == 1:
            if random.choice([True, False]):
                self.time_a.seu_turno = True
                return self.time_a, self.time_b
            else:
                self.time_b.seu_turno = True
                return self.time_b, self.time_a
        if self.time_a.seu_turno:
            return self.time_a, self.time_b
        return self.time_b, self.time_a

    def trocar_turnos(self):
        self.time_a.seu_turno = not self.time_a.seu_turno
        self.time_b.seu_turno = not self.time_b.seu_turno
    

    def historico_partida(self):
        if not self._historico.historicos_acoes:
            print("Nenhuma ação registrada")
        print(f"HISTÓRICO DA PARTIDA:")
        historico = self._historico.gerar_historico()
        print("\n".join(historico))
    
    
    def jogo(self):
        while not self.vencedor:
            quem_joga, outra_equipe = self.decidir_de_quem_e_a_vez
            personagens_atacar = quem_joga.vivos
            if not outra_equipe.vivos:
                self.vencedor = quem_joga
                self.mostrar_vencedor()
                self.historico_partida()
                break
            print(f"=== RODADA {self.rodada} ===")
            time.sleep(1)
            print(f"VEZ DA EQUIPE: {quem_joga.nome}")
            for personagem in personagens_atacar:
                if not outra_equipe.vivos:
                    self.vencedor = quem_joga
                    self.mostrar_vencedor()
                    self.historico_partida()
                    return
                alvo = random.choice(outra_equipe.vivos)
                dano = personagem.atacar(alvo)
                tempo = self.calcular_duracao_partida()
                self._historico.adicionar(
                    Acoes("batalha", f"Personagem {personagem.nome} atacou o personagem {alvo.nome} e causou {dano} de dano.", tempo, self._rodada)
                )
                print(f"Personagem {personagem.nome} atacou o personagem {alvo.nome} e causou {dano} de dano.")
                time.sleep(1)
                if not alvo.esta_vivo():
                    self._historico.adicionar(
                        Acoes("batalha", f"Personagem {alvo.nome} morreu após receber {dano} de dano", tempo, self._rodada)
                    )
                    print(f"Personagem {alvo.nome} morreu após receber {dano} de dano")
                    self.quantidade_de_personagens_que_morreram += 1
                    time.sleep(1)
                outra_equipe.vivos
                
            self.trocar_turnos()
            self._rodada += 1
    
    def mostrar_vencedor(self):
        print(f"A EQUIPE VENCEDORA FOI A EQUIPE: {self.vencedor.nome}")
        time.sleep(1)
        duracao = self.calcular_duracao_partida()
        print(f"A PARTIDA DUROU: {duracao}")
        time.sleep(1)
        print("PERSONAGENS RESTANTES:")
        restantes = self.vencedor.vivos
        for persoagens in restantes:
            print(f"NOME: {persoagens.nome} | VIDA: {persoagens.vida} | TOTAL DE DANO CAUSADO: {persoagens.total_dano_causado}")
            time.sleep(0.75)
            
            
    def calcular_duracao_partida(self) -> str:
        duracao = datetime.datetime.now() - self.comecou
        minutos = int(duracao.total_seconds() // 60)
        segundos = int(duracao.total_seconds() % 60)
        tempo = f"{minutos} minutos e {segundos} segundos"
        return tempo
    
    
try:
    guerreiro_a = Guerreiro(
    nome="Thorgar",
    vida=300,
    vida_max=300,
    forca=40
    )

    mago_a = Mago(
        nome="Eldrin",
        vida=220,
        vida_max=220,
        mana=120,
        poder_magico=18
    )

    arqueiro_a = Arqueiro(
        nome="Lyra",
        vida=240,
        vida_max=240,
        dano_variavel=35
    )

    time_a = Equipes("Equipe do Enrico", guerreiro_a, mago_a, arqueiro_a)


    guerreiro_b = Guerreiro(
        nome="Brakk",
        vida=320,
        vida_max=320,
        forca=45
    )

    mago_b = Mago(
        nome="Zaryn",
        vida=200,
        vida_max=200,
        mana=100,
        poder_magico=20
    )

    arqueiro_b = Arqueiro(
        nome="Kael",
        vida=230,
        vida_max=230,
        dano_variavel=40
    )

    time_b = Equipes("Equipe do Francisco", guerreiro_b, mago_b, arqueiro_b)

    batalha = Batalha(time_a, time_b)
    print(arqueiro_a.ver_historico_de_batalha)
    print(arqueiro_b.ver_historico_de_batalha)
    print(guerreiro_a.ver_historico_de_batalha)
    print(guerreiro_b.ver_historico_de_batalha)
    print(mago_a.ver_historico_de_batalha)
    print(mago_b.ver_historico_de_batalha)
except ValueError as e:
    print(e)