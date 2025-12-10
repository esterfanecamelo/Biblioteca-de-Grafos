from collections import deque
import heapq

class Digrafo:
    def __init__(self, dic):
        # Dados vindos da função ler_arquivo
        self.lista_arestas = dic["arestas"]
        self.lista_adj = dic["adj"]
        self.vertices = dic.get("num_vertices", len(self.lista_adj))

        # Garante que todos os vértices (1..N) existam na lista_adj,
        # mesmo os isolados
        for v in range(1, self.vertices + 1):
            if v not in self.lista_adj:
                self.lista_adj[v] = []

        # Criar lista de adjacência reversa (entrada)
        self.lista_adj_in = {v: [] for v in self.lista_adj}
        for u, v, peso in self.lista_arestas:
            self.lista_adj_in[v].append((u, peso))

        # Graus
        self.grau_entrada = {v: len(self.lista_adj_in[v]) for v in self.lista_adj}
        self.grau_saida = {v: len(self.lista_adj[v]) for v in self.lista_adj}

    def numero_de_vertices(self):
        return self.vertices

    def numero_de_arestas(self):
        return len(self.lista_arestas)

    def retornar_vizinhos(self, v):
        if v not in self.lista_adj:
            return []

        viz_saida = [x for x, _ in self.lista_adj[v]]
        viz_entrada = [u for u, _ in self.lista_adj[v]]

        return list(set(viz_saida + viz_entrada))

    def grau_de_entrada(self, v):
        return self.grau_entrada.get(v, 0)

    def grau_de_saida(self, v):
        return self.grau_saida.get(v, 0)

    def grau_total(self, v):
        return self.grau_de_entrada(v) + self.grau_de_saida(v)

    def peso_da_aresta(self, u, v):
        if u not in self.lista_adj:
            return None
        for vizinho, peso in self.lista_adj[u]:
            if vizinho == v:
                return peso
        return None
    
    def grau_min(self):
        return min(self.grau_entrada[v] + self.grau_saida[v] for v in self.lista_adj)

    def grau_max(self):
        return max(self.grau_entrada[v] + self.grau_saida[v] for v in self.lista_adj)

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
        if s not in self.lista_adj:
            raise ValueError(f"Vértice {s} não existe no grafo.")

        visitado = {v: False for v in self.lista_adj}
        pi = {v: None for v in self.lista_adj}
        ini = {v: 0 for v in self.lista_adj}
        fim = {v: 0 for v in self.lista_adj}
        tempo = 0

        idx_proximo = [(s, 0)]  # (vértice, índice do próximo vizinho)
        visitado[s] = True
        tempo += 1
        ini[s] = tempo

        while idx_proximo:
            u, idx = idx_proximo.pop()

            # Se ainda há vizinhos a explorar
            if idx < len(self.lista_adj[u]):
                v, _ = self.lista_adj[u][idx]

                # Coloca de volta com o próximo vizinho
                idx_proximo.append((u, idx + 1))

                # Visita v se ainda não visitado
                if not visitado[v]:
                    visitado[v] = True
                    pi[v] = u
                    tempo += 1
                    ini[v] = tempo
                    idx_proximo.append((v, 0))
            else:
                # Finalizou u
                tempo += 1
                fim[u] = tempo

        return pi, ini, fim


    def bellman_ford(self, s):
        if s not in self.lista_adj:
            raise ValueError(f"Vértice {s} não existe no grafo.")
        
        d = {v: float("inf") for v in self.lista_adj}
        pi = {v: None for v in self.lista_adj}
        d[s] = 0

        for _ in range(self.vertices - 1):
            mudou = False
            for u, v, peso in self.lista_arestas:
                if d[u] != float("inf") and d[u] + peso < d[v]:
                    d[v] = d[u] + peso
                    pi[v] = u
                    mudou = True
            if not mudou:
                break
        # Verificação de ciclo negativo
        for u, v, peso in self.lista_arestas:
            if d[u] != float("inf") and d[u] + peso < d[v]:
                raise ValueError("O grafo contém ciclo de peso negativo.")

        return d, pi

    def dijkstra(self, s):
        if s not in self.lista_adj:
            raise ValueError(f"Vértice {s} não existe no grafo.")
        
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
    '''
    def caminho_com_arestas_minimas(self, minimo, origem=None):
        """
        Retorna um caminho simples contendo pelo menos "minimo" arestas.
        Se origem for fornecida, tenta iniciar por ela. Caso contrário,
        tenta todos os vértices como início.
        """
        def dfs(u, visitados, caminho):
            if len(caminho) - 1 >= minimo:
                return True
            for v, _ in self.lista_adj[u]:
                if v not in visitados:
                    visitados.add(v)
                    caminho.append(v)
                    if dfs(v, visitados, caminho):
                        return True
                    caminho.pop()
                    visitados.remove(v)
            return False


        pontos_iniciais = [origem] if origem is not None else list(self.lista_adj.keys())


        for s in pontos_iniciais:
            visitados = set([s])
            caminho = [s]
            if dfs(s, visitados, caminho):
                return caminho
        return None
    
    def ciclo_com_arestas_minimas(self, minimo):
        """
        Detecta um ciclo simples contendo pelo menos 'minimo' arestas.
        Usa DFS com detecção de arestas de retorno (back edges),
        adequado para grafos grandes.
        """


        visitado = {v: False for v in self.lista_adj}
        pai = {v: None for v in self.lista_adj}
        em_pilha = {v: False for v in self.lista_adj}


        def reconstruir_ciclo(u, v):
            ciclo = [v]
            atual = u
            while atual != v and atual is not None:
                ciclo.append(atual)
                atual = pai[atual]
            ciclo.append(v)
            ciclo.reverse()
            return ciclo


        def dfs(u):
            visitado[u] = True
            em_pilha[u] = True

            for v, _ in self.lista_adj[u]:
                if not visitado[v]:
                    pai[v] = u
                    resultado = dfs(v)
                    if resultado:
                        return resultado

                # Encontrou um ciclo (aresta para vértice ainda na pilha)
                elif em_pilha[v]:
                    ciclo = reconstruir_ciclo(u, v)
                    if len(ciclo) - 1 >= minimo:
                        return ciclo


                em_pilha[u] = False
                return None

            for v in self.lista_adj:
                if not visitado[v]:
                    resultado = dfs(v)
                    if resultado:
                        return resultado


            return None
'''