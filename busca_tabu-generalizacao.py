# Entrada - arquivos txt - 1a linha = NP (Numero de Programadores)
#                        - 2a linha = NM (Numero de Modulos a serem realizados)

# Primeiro ler o arquivo e pegar a matriz NP X NM

def leitura_arquivo(nome_arquivo):
    with open(nome_arquivo, 'r') as arq:
        # np = str(arq.readline().split())
        # nm = str(arq.readline().split())
        np, nm = map(int, arq.readline().split())
        return np, nm
        
np, nm = leitura_arquivo('programadores.txt')
print(np, nm)