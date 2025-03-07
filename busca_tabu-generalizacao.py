import numpy as npy
import random
import copy

# Entrada - arquivos txt - 1a linha = NP (Numero de Programadores)
#                        - 2a linha = NM (Numero de Modulos a serem realizados)

# Primeiro ler o arquivo e pegar a matriz NP X NM
def leitura_arquivo(nome_arquivo):
    with open(nome_arquivo, 'r') as arq:
        np = int(arq.readline())
        nm = int(arq.readline())
        custos = npy.array([list(map(int, arq.readline().split())) for _ in range(np)])
        carga_horaria = npy.array([list(map(int, arq.readline().split())) for _ in range(np)])
        ch_disponivel = list(map(int, arq.readline().split()))
        return np, nm, custos, carga_horaria, ch_disponivel

# Gera uma solução inicial viável usando uma heurística gulosa, (menor custo disponível)
def solucao_inicial(np, nm, custos, carga_horaria, ch_disponivel):
    solucao = [-1] * nm
    ch_restante = ch_disponivel.copy()

    for j in range(nm):
        candidatos = []

        for i in range(np):
            if carga_horaria[i,j] <= ch_restante[i]:
                candidatos.append((i, custos[i,j]))

        # Ordena candidatos pelo custo (ordem crescente)
        if candidatos:
            candidatos.sort(key=lambda x: x[1])
            melhor_prog = candidatos[0][0]
            solucao[j] = melhor_prog

            # Atualiza a carga restante do programador escolhido
            ch_restante[melhor_prog] -= carga_horaria[melhor_prog, j]

        else:
            raise Exception(f"Não foi possível encontrar uma alocação viável para o módulo {j}.")
    return solucao

# Calcula o custo total da solução para ser comparada
def calcula_custo(solucao, custos):
    custo_total = 0

    for j, prog in enumerate(solucao):
        if prog != -1:
            custo_total += custos[prog, j]
    return custo_total

# Calcula o tempo total alocado para cada programador na solução
def calcula_uso(solucao, carga_horaria, np):
    uso = npy.zeros(np, dtype=int)
    for j, prog in enumerate(solucao):
        if prog != -1:
            uso[prog] += carga_horaria[prog, j]
    return uso

# Gera vizinhos para a solução atual, trocando designação dos módulos entre programadores,
# garantindo que a alocação respeite a restrição de carga horária.
def gera_vizinhos(solucao_atual, np, nm, carga_horaria, ch_disponivel, num_vizinhos=10):
    vizinhos = []
    uso_atual = calcula_uso(solucao_atual, carga_horaria, np)

    # Tentar gerar vizinhos aleatórios
    tentativa = 0
    while len(vizinhos) < num_vizinhos and tentativa < num_vizinhos * 10:
        tentativa += 1
        modulo = random.randint(0, nm -1)
        prog_atual = solucao_atual[modulo]

        # Escolher um programador diferente do atual
        novo_prog = random.choice([i for i in range(np) if i != prog_atual])

        # Verifica se é viável
        if uso_atual[novo_prog] + carga_horaria[novo_prog] <= ch_disponivel[novo_prog]:
            # Cria uma nova solução a partir da cópia da atual
            nova_solucao = solucao_atual.copy()
            nova_solucao[modulo] = novo_prog
            vizinhos.append(nova_solucao)
        return vizinhos
    
def busca_tabu(np, nm, custos, carga_horaria, ch_disponivel, max_interacoes=100, tamanho_tabu=10):
    # Gerar solução inicial
    solucao_atual = solucao_inicial(np, nm, custos, carga_horaria, ch_disponivel)
    melhor_solucao = solucao_atual.copy()
    melhor_custo = calcula_custo(solucao_atual, custos)

    # Lista tabu para armazenar as soluções 
    lista_tabu = []

    for iteracao in range(max_interacoes):
        vizinhos = gera_vizinhos(solucao_atual, np, nm, carga_horaria, ch_disponivel, num_vizinhos=10)

        # Filtra os vizinhos que já estão na lista tabu
        vizinhos_filtrados = [v for v in vizinhos if tuple(v) not in lista_tabu]

        if not vizinhos_filtrados:
            # Se não encontrar nenhum vizinho não tabu, encerra a busca
            break;

        # Seleciona o melhor dentre os filtrados
        candidato = None
        custo_candidato = float('inf')

        for viz in vizinhos_filtrados:
            custo_vizinho = calcula_custo(viz, custos) ########################
            
            # Critério de aspiração: caso encontrar um vizinho com custo melhor que o encontrado, aceita mesmo estando na tabu
            if custo_vizinho < custo_candidato:
                candidato = viz
                custo_candidato = custo_vizinho
        
        # Atualiza solução atual para melhor vizinho encontrado
        solucao_atual = candidato.copy()

        # Adiciona a solução atual na lista tabu
        lista_tabu.append(tuple(solucao_atual))
        if len(lista_tabu) > tamanho_tabu:
            lista_tabu.pop(0)

        # Atualiza melhor solução caso candidato seja melhor
        if custo_candidato < melhor_custo:
            melhor_solucao = candidato.copy()
            melhor_custo = custo_candidato
        
        return melhor_solucao, melhor_custo
    
if __name__ == '__main__':
    # Define nome do arquivo
    nome_arquivo = 'programadores.txt'
    
    # Leitura dos dados
    np, nm, custos, carga_horaria, ch_disponivel = leitura_arquivo(nome_arquivo)

    # Executar a busca
    melhor_solucao, melhor_custo = busca_tabu(np, nm, custos, carga_horaria, ch_disponivel, max_interacoes=100, tamanho_tabu=10)

    # Exibe resultados
    print('Melhor designação encontrada:')
    for j, prog in enumerate(melhor_solucao):
        print(f"Módulo {j+1}: Programador {prog+1}")
    print(f"\nCusto total: {melhor_custo}")