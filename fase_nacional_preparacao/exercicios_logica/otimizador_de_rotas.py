def calcular_distancia(ponto1, ponto2):
    return ((ponto1[0] - ponto2[0])**2 + (ponto1[1] - ponto2[1])**2)**0.5

def calcular_distancia_entre_cada_ponto(pontos):
    distancias = []
    for ponto in pontos:
        copia_de_pontos = pontos.copy()
        distancia_entre_pontos = []
        for copia_ponto in copia_de_pontos:
            if ponto == copia_ponto:
                continue
            distancia_entre_dois_pontos = calcular_distancia(ponto, copia_ponto)
            distancia_entre_pontos.append(
                {f'distancia entre ponto {ponto} à {copia_ponto}' : f"{distancia_entre_dois_pontos:.2f}km"}
            )
        distancias.append(
            {f"Ponto {ponto}" : distancia_entre_pontos} 
        )
    for distancia in distancias:
        for rota, distancias_rotas in distancia.items():
            print("ROTA:", rota)
            for rota in distancias_rotas:
                for rota_ponto, distancia_ponto in rota.items():
                    print(rota_ponto, '\n', f"Distância: {distancia_ponto}")
            print('-' * 40)        
            

def encontrar_rota_otimizada(pontos):
    ponto_atual = (0, 0)
    rota = [ponto_atual]
    distancia_total = 0
    pontos_restantes = pontos.copy()

    print('=== INICIANDO ENTREGAS ===')
    print(f"Ponto inicial: {ponto_atual}")
    print(f"Entregas pendentes: {pontos_restantes}")
    print("-" * 40)

    while pontos_restantes:
        mais_proximo = None
        menor_distancia = float('inf')
        
        for ponto in pontos_restantes:
            dist = calcular_distancia(ponto_atual, ponto)
            if dist < menor_distancia:
                menor_distancia = dist
                mais_proximo = ponto
        print(f"De {ponto_atual} para {mais_proximo}: {menor_distancia:.2f} km")
        
        rota.append(mais_proximo)
        distancia_total += menor_distancia
        ponto_atual = mais_proximo
        pontos_restantes.remove(mais_proximo)
        
    distancia_volta = calcular_distancia(ponto_atual, (0, 0))
    print(f"Voltando para lanchonete: {distancia_total:.2f} km")
    
    distancia_total += distancia_volta
    rota.append((0,0))
    
    print('-' * 40)
    print(f"Distância total: {distancia_total:.2f} km")
    print(f"Rota completa: {rota}")
    
    return rota, distancia_total

entregas = [(2, 3), (5, 1), (7, 2), (4, 6), (1, 4), (3, 5)]
rota, distancia = encontrar_rota_otimizada(entregas)
calcular_distancia_entre_cada_ponto(entregas)