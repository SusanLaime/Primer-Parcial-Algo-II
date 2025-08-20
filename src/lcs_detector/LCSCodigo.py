import re



def tokenizar_codigo(codigo):


    # Definición de patrones para diferentes tipos de tokens
    patrones = [
        ('palabra_clave', r'\b(if|else|while|for|int|return)\b'),
        ('operador', r'(\+|\-|\*|\/|==|=|>|<)'),
        ('delimitador', r'(\(|\)|\{|\}|\[|\]|;|,)'),
        
        ('numero', r'\b\d+\b'),
        ('identificador', r'\b[a-zA-Z_][a-zA-Z0-9_]*\b'),
    ]

    tokens = []
    i = 0

    while i < len(codigo):

        if codigo[i].isspace():
            i += 1
            continue

        if codigo[i:i+2] == "//":
            # Saltar comentarios de línea
            i = codigo.find('\n', i)
            if i == -1:
                break
            continue

        token_encontrado = False

        for tipo, patron in patrones:
            match = re.match(patron, codigo[i:])
            if match:
                tokens.append((tipo, match.group()))
                i += len(match.group())
                token_encontrado = True
                break

        if not token_encontrado:
            # Si no coincide con ningún patrón, tomar el caracter como delimitador desconocido
            tokens.append(('desconocido', codigo[i]))
            i += 1

    return tokens



def tipo_de_token(token):

    return token[0]



def lcs_pesar(seq1, seq2, pesos):

    m, n = len(seq1), len(seq2)
    dp = [[0]*(n+1) for _ in range(m+1)]

    for i in range(1, m+1):

        for j in range(1, n+1):
            if seq1[i-1][1] == seq2[j-1][1] and seq1[i-1][0] == seq2[j-1][0]:
                dp[i][j] = dp[i-1][j-1] + pesos.get(tipo_de_token(seq1[i-1]), 1)
            else:
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])

    return dp[m][n]



def calcular_similitud_codigo(codigo1, codigo2, pesos, umbral=0.4):

    print("Calculando similitud entre los códigos...")

    tokens1 = tokenizar_codigo(codigo1)
    tokens2 = tokenizar_codigo(codigo2)

    lcs_score = lcs_pesar(tokens1, tokens2, pesos)

    total_peso1 = sum(pesos.get(tipo_de_token(token), 1) for token in tokens1)
    total_peso2 = sum(pesos.get(tipo_de_token(token), 1) for token in tokens2)

    similitud = (2 * lcs_score) / (total_peso1 + total_peso2) if (total_peso1 + total_peso2) > 0 else 0

    if similitud < umbral:
        return f"No es copia (similitud: {similitud:.2%})"
    else:
        return f"Es copia (similitud: {similitud:.2%})"




def leer_txt_como_string(ruta_archivo):

    with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
        return archivo.read()





# Ejemplo de uso

pesos = {
    'palabra_clave': 5,
    'operador': 2,
    'delimitador': 1,
    'numero': 1,
    'identificador': 3,
    'desconocido': 1
}

codigo1 = leer_txt_como_string('src\lcs_detector\codigo1.txt')



codigo2 = leer_txt_como_string('src\lcs_detector\codigo2.txt')



resultado = calcular_similitud_codigo(codigo1, codigo2, pesos)
print(resultado)


print("Codigo casi igual: ->")

codigo1 = leer_txt_como_string('src\lcs_detector\similitud1.txt')

codigo2 = leer_txt_como_string('src\lcs_detector\similitud2.txt')
resultado = calcular_similitud_codigo(codigo1, codigo2, pesos)
print(resultado)


print("Codigo con poca similitud: ->")
codigo1 = leer_txt_como_string('src\lcs_detector\codigo1.txt')
codigo2 = leer_txt_como_string('src\lcs_detector\codigoDistinto.txt')
resultado = calcular_similitud_codigo(codigo1, codigo2, pesos)
print(resultado)

