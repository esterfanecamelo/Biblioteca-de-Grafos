from Grafo import Grafo
from Digrafo import Digrafo

# Lê o arquivo .gr e converte para um dicionário
def le_arquivo(caminho_arquivo):
    grafo = {"conjunto_de_arestas": []}

    with open(caminho_arquivo, "r") as f:
        for linha in f:
            linha = linha.strip()

            # ignorar comentários e linhas vazias
            if not linha or linha.startswith("c"):
                continue

            # ignorar linha 'p sp ...'
            if linha.startswith("p"):
                continue

            # linha de aresta: a no1 no2 peso
            if linha.startswith("a"):
                _, no1, no2, peso = linha.split()
                grafo["conjunto_de_arestas"].append((int(no1), int(no2), float(peso)))

    return grafo

arquivo = r"USA-road-d.NY.gr"

grafo_dict = le_arquivo(arquivo)

G = Grafo(grafo_dict)


