def valida_cpf(cpf: str) -> bool:
    cpf_limpo = ''.join(filter(str.isdigit, cpf))
    
    print('CPF limpo:', cpf_limpo) 

    if len(cpf_limpo) != 11:
        print('Erro: CPF não tem 11 dígitos')
        return False

    if cpf_limpo == cpf_limpo[0] * 11:
        print('Erro: CPF com sequência repetida')
        return False

    soma = 0
    peso = 10
    
    for i in range(9): 
        digito = int(cpf_limpo[i])
        soma += digito * peso
        peso -= 1
    
    resto = soma % 11
    if resto < 2:
        digito1_calculado = 0
    else:
        digito1_calculado = 11 - resto
    
    soma = 0
    peso = 11
    
    for i in range(10): 
        if i < 9:
            digito = int(cpf_limpo[i])  
        else:
            digito = digito1_calculado  
        
        soma += digito * peso  
        peso -= 1
    
    resto = soma % 11
    if resto < 2:
        digito2_calculado = 0
    else:
        digito2_calculado = 11 - resto
    
    print(f'Segundo dígito calculado: {digito2_calculado}')

    digito1_informado = int(cpf_limpo[9])   
    digito2_informado = int(cpf_limpo[10])  
    
    valido = (digito1_calculado == digito1_informado and 
              digito2_calculado == digito2_informado)
    
    print(f'Dígitos informados: {digito1_informado}{digito2_informado}')
    print(f'Válido? {valido}')
    
    return valido

cpf = input('digite o seu cpf: ')
valida_cpf(cpf)