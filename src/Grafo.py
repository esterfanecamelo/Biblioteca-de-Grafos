from collections import deque
import heapq

class Grafo: 
    def __init__(self, dic):

        # Arestas vindas da função ler_arquivo()
        self.lista_arestas = dic["arestas"]
        num_vertices = dic.get("num_vertices", 0)

        # Construção da lista de adjacência
        self.lista_adj = {}
        for u, v, peso in self.lista_arestas:
            if u not in self.lista_adj:
                self.lista_adj[u] = []
            if v not in self.lista_adj:
                self.lista_adj[v] = []
            # Não-direcionado
            self.lista_adj[u].append((v, peso))
            self.lista_adj[v].append((u, peso))

        # Garante que todos os vértices (1..N) existam
        if num_vertices > 0:
            for v in range(1, num_vertices + 1):
                if v not in self.lista_adj:
                    self.lista_adj[v] = []

        self.vertices = len(self.lista_adj)

    def numero_de_vertices(self):
        return self.vertices

    def numero_de_arestas(self):
        # Cada aresta aparece duas vezes
        total = sum(len(adj) for adj in self.lista_adj.values())
        return total // 2

    def retornar_vizinhos(self, v):
        if v not in self.lista_adj:
            return []
        return list(set(viz for viz, _ in self.lista_adj[v]))

    def grau_do_vertice(self, v):
        if v not in self.lista_adj:
            return 0
        return len(self.retornar_vizinhos(v))

    def peso_da_aresta(self, u, v):
        for vizinho, peso in self.lista_adj.get(u, []):
            if vizinho == v:
                return peso
        return None

    def grau_min(self):
        if not self.lista_adj:
            return 0
        return min(self.grau_do_vertice(v) for v in self.lista_adj)

    def grau_max(self):
        if not self.lista_adj:
            return 0
        return max(self.grau_do_vertice(v) for v in self.lista_adj)

    def bfs(self, s):
        if s not in self.lista_adj:
            raise ValueError(f"Vértice {s} não existe no grafo.")

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

        # Para grafo não-direcionado, cada aresta aparece como (u,v) e (v,u)
        arestas = []
        for u, v, peso in self.lista_arestas:
            arestas.append((u, v, peso))
            arestas.append((v, u, peso))

        for _ in range(self.vertices - 1):
            mudou = False
            for u, v, peso in arestas:
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

        return cores, max(cores.values())
