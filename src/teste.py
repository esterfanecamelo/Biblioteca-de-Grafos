from Grafo import Grafo
from Digrafo import Digrafo
import os

def ler_arquivo(caminho_arquivo):
    dados = {
        "num_vertices": 0,
        "num_arestas": 0,
        "arestas": [],
        "adj": {}
    }

    with open(caminho_arquivo, "r") as f:
        for linha in f:
            linha = linha.strip()

            if not linha or linha.startswith("c"):
                continue

            # Linha do problema: p sp <num_vertices> <num_arestas>
            if linha.startswith("p"):
                partes = linha.split()
                # Exemplo: p sp 264346 733846
                if len(partes) >= 4:
                    dados["num_vertices"] = int(partes[2])
                    dados["num_arestas"] = int(partes[3])
                continue

            # Linha de arco: a x y p
            if linha.startswith("a"):
                _, u, v, peso = linha.split()
                u, v, peso = int(u), int(v), float(peso)

                dados["arestas"].append((u, v, peso))

                if u not in dados["adj"]:
                    dados["adj"][u] = []
                dados["adj"][u].append((v, peso))

    return dados

def grau_minimo(G):
    return min(G.grau_total(v) for v in G.lista_adj)

def grau_maximo(G):
    return max(G.grau_total(v) for v in G.lista_adj)

def encontrar_caminho_com_10(G):

    visitado = set()
    caminho = []

    def dfs(u):
        visitado.add(u)
        caminho.append(u)

        if len(caminho) >= 11:  # 11 vértices = 10 arestas
            return True

        for v, _ in G.lista_adj[u]:
            if v not in visitado:
                if dfs(v):
                    return True

        caminho.pop()
        return False

    for s in G.lista_adj:
        visitado.clear()
        caminho.clear()
        if dfs(s):
            return caminho

    return None

def encontrar_ciclo_com_5(G):

    visitado = set()
    pilha = []

    def dfs(u):
        visitado.add(u)
        pilha.append(u)

        for v, _ in G.lista_adj[u]:
            if v in pilha:
                idx = pilha.index(v)
                ciclo = pilha[idx:]
                if len(ciclo) >= 6:  # 6 vértices = 5 arestas
                    return ciclo
            elif v not in visitado:
                r = dfs(v)
                if r:
                    return r

        pilha.pop()
        return None

    for u in G.lista_adj:
        visitado.clear()
        pilha.clear()
        ciclo = dfs(u)
        if ciclo:
            return ciclo

    return None

def vertice_mais_distante(G, origem):
    d, _ = G.dijkstra(origem)
    v_max = max(d, key=lambda x: d[x] if d[x] < float("inf") else -1)
    return v_max, d[v_max]

def quantidade_de_cores(G):
    _, k = G.coloracao_propria()
    return k


# Caminho da pasta dados
base = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "dados"))

arquivo_grafo = os.path.join(base, "grafos_teste.gr")
arquivo_digrafo = os.path.join(base, "USA-road-d.NY.gr")

# Carregar grafos
grafo_dict = ler_arquivo(arquivo_grafo)
digrafo_dict = ler_arquivo(arquivo_digrafo)

#G = Grafo(grafo_dict)
D = Digrafo(digrafo_dict)

print("a) G.mind =", grau_minimo(D))
print("b) G.maxd =", grau_maximo(D))

print("c) Caminho com ≥ 10 arestas:")
print(encontrar_caminho_com_10(D))

print("d) Ciclo com ≥ 5 arestas:")
print(encontrar_ciclo_com_5(D))

v, dist = vertice_mais_distante(D, 129)
print("e) Vértice mais distante de 129 =", v, "Distância =", dist)

print("f) Qtde de cores =", quantidade_de_cores(D))