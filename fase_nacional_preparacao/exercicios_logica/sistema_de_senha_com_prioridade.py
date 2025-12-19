from collections import deque  #uso de deque para maior desempenho em sistema de filas.
from datetime import datetime, timedelta #uso de datetime para fazer comparacao de horários no atendimento
import random #só para gerar escritórios para pacientes

class SistemaSenhas:
    
    def __init__(self):
        self.lista_grave = deque()
        self.lista_idosos = deque()
        self.lista_geral = deque()
        self.contadores = {'G' : 1, 'I': 1, 'N': 1}
        self.historico = []
        
    def nova_senha(self, tipo):
        if tipo not in ['grave', 'geral', 'idoso']:
            print('Tipo de senha inválido!')
            return None
        
        if tipo == 'grave':
            prefixo = 'G'
            contador = self.contadores['G']
            self.contadores['G'] += 1
        elif tipo == 'idoso':
            prefixo = 'I'
            contador = self.contadores['I']
            self.contadores['I'] += 1
        else:
            prefixo = 'N'
            contador = self.contadores['N']
            self.contadores['N'] += 1
        
        senha_gerada = {
            'senha' : prefixo+str(contador),
            'data_gerada' : datetime.now(),
            'data_formatada' : datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        }
        if 'G' in senha_gerada['senha']:
            self.lista_grave.append(senha_gerada)
        elif 'I' in senha_gerada['senha']:
            self.lista_idosos.append(senha_gerada)
        else:
            self.lista_geral.append(senha_gerada)
            
    def proximo_atendimento(self):
        lista_idosos_recentes = self.lista_idosos[:5] if len(self.lista_idosos) >= 5 else self.lista_idosos
        lista_geral_recentes = self.lista_geral[:5] if len(self.lista_geral) >= 5 else self.lista_geral
        tem_pacientes = not lista_geral_recentes and not lista_idosos_recentes and not self.lista_grave

        if tem_pacientes:
            print("Não há nenhum paciente a ser atendido!")
            return
        if self.lista_grave:
            senha = self.lista_grave[0]
            print(f"SENHA: {senha['senha']} PARA O ESCRITÓRIO {random.randint(1, 30)}")
            self.historico.append(self.lista_grave[0])
            self.lista_grave.popleft()
            return
        
        if not self.lista_idosos:
            senha = self.lista_geral[0]
            print(f"SENHA: {senha['senha']} PARA O ESCRITÓRIO {random.randint(1, 30)}")
            self.historico.append(senha)
            self.lista_geral.popleft()
            return
        
        data_senha_idoso = lista_idosos_recentes[0]['data_gerada']
        for paciente in lista_geral_recentes:
            data_senha_paciente = paciente['data_gerada']
            tempo_espera =  (data_senha_paciente - data_senha_idoso)
            if tempo_espera.total_seconds() > 1800:
                print(f"SENHA: {paciente['senha']} PARA O ESCRITÓRIO {random.randint(1, 30)}")
                self.historico.append(self.lista_geral[0])
                self.lista_geral.popleft()
                return
        print(f"SENHA: {self.lista_idosos[0]['senha']} PARA O ESCRITÓRIO {random.randint(1, 30)}")
        self.historico.append(self.lista_idosos[0])
        self.lista_idosos.popleft()

    def status(self):
        tem_pacientes = not self.lista_geral and not self.lista_idosos and not self.lista_grave
        if tem_pacientes:
            print("Não há nenhum paciente a ser atendido!")
            return
        todos_pacientes = []
        todos_pacientes.extend(self.lista_geral)
        todos_pacientes.extend(self.lista_grave)
        todos_pacientes.extend(self.lista_idosos)
        atendimento_organizado = {
            "GRAVES" : [],
            "IDOSOS" : [],
            "GERAL" : []
        }
        
        for senha in todos_pacientes:
            if "I" in senha['senha']:
                atendimento_organizado["IDOSOS"].append(senha)
            elif "G" in senha['senha']:
                atendimento_organizado["GRAVES"].append(senha)
            else:
                atendimento_organizado["GERAL"].append(senha)
        
        for gravidade, senhas in atendimento_organizado.items():
            print(f"{'=' * 15}{gravidade}{'=' * 15}")
            for senha in senhas:
                print(
                    f"SENHA: {senha['senha']} | DATA DE EMISSÃO: {senha['data_formatada']}"
                )

    def historico_atendimentos(self):
        if not self.historico:
            print("Nenhum histórico de atendimento encontrado!")
            return
        print(('='*10), "HISTÓRICO", ('='*10))
        for senha in self.historico:
            print(f'SENHA: {senha["senha"]} || DATA DE EMISSÃO: {senha["data_formatada"]}')
            
            
hospital = SistemaSenhas()
hospital.nova_senha('idoso')
hospital.nova_senha('grave')
hospital.nova_senha('geral')
hospital.nova_senha('geral')
hospital.status()
hospital.proximo_atendimento()
hospital.proximo_atendimento()
hospital.proximo_atendimento()
hospital.historico_atendimentos()