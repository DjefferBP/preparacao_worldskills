from datetime import date
from collections import deque


class Vendas:
    
    def __init__(self,):        
        self.total_vendas = deque()
    
    def adicionar_venda(self, data: date, produto: str, quantidade: int, valor_unitario: float):
        self.produto = {
            "data_emitido": data,
            "produto" : produto,
            "quantidade" : quantidade,
            "valor_unitario" : valor_unitario
        }
        self.adicionar_no_total_vendas(self.produto)
        
    def adicionar_no_total_vendas(self, produto):
        self.total_vendas.append(produto)
        
    def ver_vendas(self):
        if not self.total_vendas:
            print("Nenhuma venda disponível!")
            return
        print("Total de vendas: {0}".format(len(self.total_vendas)))
        for venda in self.total_vendas:
            print(f"Data da venda: {venda['data_emitido']}\nNome do produto: {venda['produto']}\nQuantidade vendida: {venda['quantidade']}\nValor unitário: {venda['valor_unitario']}", end='\n==============\n')
    
    def calcular_total_por_dia(self):
        if not self.total_vendas:
            return
        agrupado_por_dia = {}
        
        for venda in self.total_vendas:
            data = venda["data_emitido"]
            if data not in agrupado_por_dia:
                agrupado_por_dia[data] = {
                    "vendas": [],
                    "total_valor": 0,
                    "total_quantidade": 0,
                    "contagem": 0
                }
            
            agrupado_por_dia[data]["vendas"].append(venda)
            agrupado_por_dia[data]["total_valor"] += venda["quantidade"] * venda["valor_unitario"]
            agrupado_por_dia[data]["total_quantidade"] += venda["quantidade"]
            agrupado_por_dia[data]["contagem"] += 1
        
        for data, dados in agrupado_por_dia.items():
            print(f"\nDATA: {data}")
            print(f"Total vendas: {dados['contagem']}")
            print(f"Quantidade total: {dados['total_quantidade']}")
            print(f"Valor total: R$ {dados['total_valor']:.2f}")
            
            for venda in dados["vendas"]:
                print(f"  {venda['produto']}: {venda['quantidade']} × R${venda['valor_unitario']}")
        
    def retornar_dados_de_dia_especifico(self, data_especifica, lista_com_vendas) -> tuple:
        if not lista_com_vendas:
            print("A lista está vazia!")
            return
        
        tupla_com_vendas = tuple(lista_com_vendas)
        data_requerida = data_especifica
        tupla_filtrada = tuple(item for item in tupla_com_vendas if item["data_emitido"] == data_requerida)
        return tupla_filtrada
    
    def calcular_produto_mais_vendido(self):
        if not self.total_vendas:
            print("Não há nenhuma venda!")
            return
    
        maior_vendido = None
        maior = self.total_vendas[0]["quantidade"]
        for venda in self.total_vendas:
            if venda["quantidade"] > maior:
                maior = venda["quantidade"]
                maior_vendido = venda
        
        print(f"INFORMAÇÕES SOBRE O PRODUTO MAIS VENDIDO:\nNOME DO PRODUTO: {maior_vendido['produto']}\n"\
            f"PREÇO UNITÁRIO: {maior_vendido['valor_unitario']}\nQUANTIDADE VENDIDO: {maior_vendido['quantidade']}\n"\
                f"TOTAL EM VENDAS: {int(maior_vendido['quantidade']) * float(maior_vendido['valor_unitario'])}")

    def analise_geral_vendas(self):
        if not self.total_vendas:
            print("Não há nenhuma venda!")
            return

        data_analisadas = []
        total_vendas_valor = 0
        print("===== INFORMAÇÕES GERAIS =====")
        for venda in self.total_vendas:
            total_vendas_valor += venda["valor_unitario"] * venda["quantidade"]
            data_venda = venda["data_emitido"]
            if data_venda in data_analisadas:
                continue
            vendas_dia = self.retornar_dados_de_dia_especifico(data_venda, self.total_vendas)
            lucro_total_dia = 0
            if len(vendas_dia) <= 0:
                print("NENHUMA VENDA IDENTIFICADA NO DIA:", data_venda, '')
                continue
            for dia_produto in vendas_dia:
                lucro_total_dia += dia_produto["quantidade"] * dia_produto["valor_unitario"]
            
            print(f"VENDAS TOTAIS DO DIA {data_venda}: {len(vendas_dia)} | LUCRO TOTAL: {lucro_total_dia:.2f}")
            data_analisadas.append(data_venda)
            
        print("TOTAIS DE VENDAS:", len(self.total_vendas), "| LUCROS TOTAIS:", total_vendas_valor)

vendas = Vendas()
vendas.adicionar_venda(date(2025, 12, 19), "carro", 1, 23000)
vendas.adicionar_venda(date(2025, 12, 19), "Iphone 12 Pro Max", 4, 5000)
vendas.adicionar_venda(date(2025, 9, 12), "Iphone 12 Pro Max", 1, 4500)
vendas.adicionar_venda(date(2025, 9, 12), "Iphone 16 Pro Max", 7, 10000)
vendas.calcular_total_por_dia()
vendas.calcular_produto_mais_vendido()  
vendas.analise_geral_vendas()