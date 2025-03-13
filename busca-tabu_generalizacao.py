import random

# Função para ler os dados do arquivo
def leitura_arquivo(nome_arquivo):
    with open(nome_arquivo, 'r') as arq:
        np = int(arq.readline().strip())  # Número de programadores
        nm = int(arq.readline().strip())  # Número de módulos

        custos = []
        for _ in range(np):
            custos.append(list(map(int, arq.readline().split())))

        carga_horaria = []
        for _ in range(np):
            carga_horaria.append(list(map(int, arq.readline().split())))

        ch_disponivel = list(map(int, arq.readline().split()))

    return np, nm, custos, carga_horaria, ch_disponivel

# Função para gerar uma solução inicial tentando minimizar o custo
def solucao_inicial(np, nm, custos, carga_horaria, ch_disponivel):
    solucao = [-1] * nm
    ch_restante = ch_disponivel[:]

    for j in range(nm):
        candidatos = []

        for i in range(np):
            if carga_horaria[i][j] <= ch_restante[i]:  # Verifica se pode ser alocado
                candidatos.append((i, custos[i][j]))

        if candidatos:
            candidatos.sort(key=lambda x: x[1])  # Escolhe o de menor custo
            melhor_prog = candidatos[0][0]
            solucao[j] = melhor_prog
            ch_restante[melhor_prog] -= carga_horaria[melhor_prog][j]
        else:
            # **Se não houver candidatos, escolhemos o menos sobrecarregado**
            melhor_prog = min(range(np), key=lambda i: ch_restante[i])  
            solucao[j] = melhor_prog
            ch_restante[melhor_prog] -= carga_horaria[melhor_prog][j]  # Ajusta mesmo sobrecarregando um pouco
            
    return solucao

# Função para calcular o custo total de uma solução
def calcula_custo(solucao, custos):
    return sum(custos[prog][j] for j, prog in enumerate(solucao) if prog != -1)

# Calcula a carga horária usada por cada programador
def calcula_uso(solucao, carga_horaria, np):
    uso = [0] * np
    for j, prog in enumerate(solucao):
        if prog != -1:
            uso[prog] += carga_horaria[prog][j]
    return uso

# Gera vizinhos respeitando as restrições de carga horária
def gera_vizinhos(solucao_atual, np, nm, carga_horaria, ch_disponivel, num_vizinhos=10):
    vizinhos = []
    uso_atual = calcula_uso(solucao_atual, carga_horaria, np)
    
    tentativas = 0
    while len(vizinhos) < num_vizinhos and tentativas < num_vizinhos * 10:
        tentativas += 1
        modulo = random.randint(0, nm - 1)
        prog_atual = solucao_atual[modulo]

        # Escolhe um novo programador diferente do atual
        candidatos = [i for i in range(np) if i != prog_atual and uso_atual[i] + carga_horaria[i][modulo] <= ch_disponivel[i]]
        
        if candidatos:
            novo_prog = random.choice(candidatos)
            nova_solucao = solucao_atual[:]
            nova_solucao[modulo] = novo_prog
            vizinhos.append(nova_solucao)

    return vizinhos

# Implementação da busca tabu
def busca_tabu(np, nm, custos, carga_horaria, ch_disponivel, max_interacoes=100, tamanho_tabu=10):
    solucao_atual = solucao_inicial(np, nm, custos, carga_horaria, ch_disponivel)
    melhor_solucao = solucao_atual[:]
    melhor_custo = calcula_custo(solucao_atual, custos)
    
    lista_tabu = []

    for iteracao in range(max_interacoes):
        vizinhos = gera_vizinhos(solucao_atual, np, nm, carga_horaria, ch_disponivel, num_vizinhos=10)

        if not vizinhos:
            break  # Se não houver vizinhos válidos, encerra

        melhor_vizinho = None
        menor_custo_vizinho = float('inf')

        for viz in vizinhos:
            custo_viz = calcula_custo(viz, custos)

            # Critério de aspiração: aceita um vizinho tabu se ele for melhor que o melhor encontrado
            if tuple(viz) in lista_tabu and custo_viz >= melhor_custo:
                continue

            if custo_viz < menor_custo_vizinho:
                melhor_vizinho = viz
                menor_custo_vizinho = custo_viz

        # Atualiza a solução
        if melhor_vizinho:
            solucao_atual = melhor_vizinho[:]
            lista_tabu.append(tuple(solucao_atual))

            if len(lista_tabu) > tamanho_tabu:
                lista_tabu.pop(0)  # Mantém a lista tabu com tamanho limitado

            # Atualiza melhor solução encontrada
            if menor_custo_vizinho < melhor_custo:
                melhor_solucao = melhor_vizinho[:]
                melhor_custo = menor_custo_vizinho

    return melhor_solucao, melhor_custo

# Executa a busca tabu com os dados do arquivo
if __name__ == '__main__':
    nome_arquivo = 'programadores.txt'
    np, nm, custos, carga_horaria, ch_disponivel = leitura_arquivo(nome_arquivo)

    melhor_solucao, melhor_custo = busca_tabu(np, nm, custos, carga_horaria, ch_disponivel)

    print('Melhor designação encontrada:')
    for j, prog in enumerate(melhor_solucao):
        print(f"Módulo {j+1}: Programador {prog+1}")
    print(f"\nCusto total: {melhor_custo}")
