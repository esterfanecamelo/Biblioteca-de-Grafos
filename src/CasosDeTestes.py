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

def encontrar_caminho_com_10(G):
    for s in G.lista_adj:
        pi, ini, fim = G.dfs(s)

        # Ordenar por tempo de término (mais profundo primeiro)
        ordem = sorted(fim, key=lambda x: fim[x], reverse=True)

        for v in ordem:
            # Reconstruir caminho s -> v usando pi[]
            caminho = []
            u = v
            while u is not None:
                caminho.append(u)
                u = pi[u]
            caminho.reverse()

            if len(caminho) >= 11:  # 10 arestas
                return caminho

    return None

def encontrar_ciclo_com_5(G):
    for s in G.lista_adj:
        pi, ini, fim = G.dfs(s)

        for u in G.lista_adj:
            for v, _ in G.lista_adj[u]:
                if ini[v] < ini[u] < fim[v]:
                    # Reconstruir ciclo
                    ciclo = [u]
                    x = u
                    while x != v:
                        x = pi[x]
                        ciclo.append(x)
                    ciclo.reverse()

                    if len(ciclo) >= 6:  # 5 arestas, 6 vértices
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

arquivo_digrafo = os.path.join(base, "USA-road-d.NY.gr")

# Carregar grafo
digrafo_dict = ler_arquivo(arquivo_digrafo)

D = Digrafo(digrafo_dict)

print("a) D.mind =", D.grau_min())
print("b) D.maxd =", D.grau_max())

print("c) Caminho com ≥ 10 arestas:")
print(encontrar_caminho_com_10(D))

print("d) Ciclo com ≥ 5 arestas:")
print(encontrar_ciclo_com_5(D))

v, dist = vertice_mais_distante(D, 129)
print("e) Vértice mais distante de 129 =", v, "Distância =", dist)
print("f) Quantidade de cores =", quantidade_de_cores(D))