from collections import deque
import heapq

class Grafo: 
    def __init__(self, dic):
        # Recebe um dicionário contendo a lista de arestas do grafo, onde cada aresta é uma tupla (u, v, peso)
        self.lista_arestas = dic["conjunto_de_arestas"]

        self.lista_adj = {} # Cria uma lista de adjacência
        for u, v, peso in self.lista_arestas:
            if u not in self.lista_adj:
                self.lista_adj[u] = []
            if v not in self.lista_adj:
                self.lista_adj[v] = []
            self.lista_adj[u].append((v, peso))
            self.lista_adj[v].append((u, peso))
        
        # Fica contando o número de vertices e guara o valor em self.vertices
        self.vertices = len(self.lista_adj)
    
    # Retornar o número de vértices do grafo
    def numero_de_vertices(self):
        return self.vertices

    # Retornar o númeoro de arestas do grafo. Soma conta 2 vezes, u para v e v para u por isso dividir a soma por 2 para obter o número real de arestas
    def numero_de_arestas (self):
        total_arestas = sum(len(vizinhos) for vizinhos in self.lista_adj.values())
        return total_arestas // 2

    #Retornar a vizinhança do vétice v, ou seja, os vértices adjacentes a v
    def retornar_vizinhos(self, v):
        if v not in self.lista_adj:
            return []
        #Para cada (vizinho, peso) em lista_adj[v], adicione apenas o vizinho na lista final”
        return list(set(vizinho for vizinho, _ in self.lista_adj[v]))

    #Retorna o grau do vértice v, ou seja, o número de arestas incidentes a v. Em oureas palavras a quantidade de vizinhos que o vertice possui
    def grau_do_vertice (self, v):
        if v not in self.lista_adj:
            return 0
        return len(set(self.lista_adj[v]))

    #Retorna o peso da aresta uv
    def peso_da_aresta (self, u, v):
        if u not in self.lista_adj:
                return None
        for (vizinho, peso) in self.lista_adj[u]:
            if vizinho == v:
                return peso
        return None

    #Retorna o menor grau presente no grafo
    def grau_min(self):
        if not self.lista_adj:
            return 0  
        return min(len(adj) for adj in self.lista_adj.values())
        
    #Retorna o maior grau presente no grafo
    def grau_max (self):
        if not self.lista_adj:
            return 0
        return max(len(adj) for adj in self.lista_adj.values())
    
    def bfs (self, s):
        # d armazena distância de s até cada vértice
        d = {v: float("inf") for v in self.lista_adj}
        # pi armazena o predecessor
        pi = {v : None for v in self.lista_adj}
        
        d[s] = 0 # caminho de s até eele mesmo
        
        fila = deque([s]) # fila FIFO
        
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
            for u, v, peso in self.lista_arestas:
                if d[v] + peso < d[u]:
                    d[u] = d[v] + peso
                    pi[u] = v
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