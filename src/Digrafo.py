from collections import deque
import heapq

class Digrafo:
    def __init__(self, dic):
        self.lista_arestas = dic["conjunto_de_arestas"]

        self.lista_adj = {}
        for u, v, peso in self.lista_arestas:
            if u not in self.lista_adj:
                self.lista_adj[u] = []
            if v not in self.lista_adj:
                self.lista_adj[v] = []
            self.lista_adj[u].append((v, peso))

        self.vertices = len(self.lista_adj)

        self.grau_in = {v: 0 for v in self.lista_adj}
        for u, v, _ in self.lista_arestas:
            self.grau_in[v] += 1

        self.grau_out = {v: len(self.lista_adj[v]) for v in self.lista_adj}

    def numero_de_vertices(self):
        return self.vertices

    def numero_de_arestas(self):
        return len(self.lista_arestas)

    def retornar_vizinhos(self, v):
        if v not in self.lista_adj:
            return []
        viz_saida = [x for x, _ in self.lista_adj[v]]
        viz_entrada = [u for u, w, _ in self.lista_arestas if w == v]
        return list(set(viz_saida + viz_entrada))

    def grau_de_entrada(self, v):
        return self.grau_in.get(v, 0)

    def grau_de_saida(self, v):
        return self.grau_out.get(v, 0)

    def grau_total(self, v):
        return self.grau_de_entrada(v) + self.grau_de_saida(v)

    def peso_da_aresta(self, u, v):
        if u not in self.lista_adj:
            return None
        for vizinho, peso in self.lista_adj[u]:
            if vizinho == v:
                return peso
        return None

    def bfs(self, s):
        d = {v: float("inf") for v in self.lista_adj}
        pi = {v: None for v in self.lista_adj}
        d[s] = 0
        fila = deque([s])

        while fila:
            u = fila.popleft()
            for v, _ in self.lista_adj[u]:
                if d[v] == float("inf"):
                    d[v] = d[u] + 1
                    pi[v] = u
                    fila.append(v)

        return d, pi

    def dfs(self, s):
        visitado = {v: False for v in self.lista_adj}
        pi = {v: None for v in self.lista_adj}
        ini = {v: 0 for v in self.lista_adj}
        fim = {v: 0 for v in self.lista_adj}
        tempo = [0]

        def dfs_visita(u):
            visitado[u] = True
            tempo[0] += 1
            ini[u] = tempo[0]

            for v, _ in self.lista_adj[u]:
                if not visitado[v]:
                    pi[v] = u
                    dfs_visita(v)

            tempo[0] += 1
            fim[u] = tempo[0]

        dfs_visita(s)
        return pi, ini, fim

    def bellman_ford(self, s):
        d = {v: float("inf") for v in self.lista_adj}
        pi = {v: None for v in self.lista_adj}
        d[s] = 0

        for _ in range(self.vertices - 1):
            mudou = False
            for u, v, peso in self.lista_arestas:
                if d[u] + peso < d[v]:
                    d[v] = d[u] + peso
                    pi[v] = u
                    mudou = True
            if not mudou:
                break

        return d, pi

    def dijkstra(self, s):
        d = {v: float("inf") for v in self.lista_adj}
        pi = {v: None for v in self.lista_adj}
        d[s] = 0

        fila = [(0, s)]
        while fila:
            dist_u, u = heapq.heappop(fila)
            if dist_u > d[u]:
                continue
            for v, peso in self.lista_adj[u]:
                if d[u] + peso < d[v]:
                    d[v] = d[u] + peso
                    pi[v] = u
                    heapq.heappush(fila, (d[v], v))

        return d, pi

    def coloracao_propria(self):
        cores = {}

        for v in sorted(self.lista_adj):
            vizinhos = self.retornar_vizinhos(v)
            cores_ocupadas = {cores[x] for x in vizinhos if x in cores}
            cor = 1
            while cor in cores_ocupadas:
                cor += 1
            cores[v] = cor
        
        k = max(cores.values())
        return cores, k
