from collections import deque

def bfs(self, origem):
    
    distancia = {v: float("inf") for v in self.lista_adj}

    predecessor = {v: None for v in self.lista_adj}

    distancia[origem] = 0
    fila = deque([origem])

    while fila:
        u = fila.popleft()

        for v, _ in self.lista_adj[u]:
            if distancia[v] == float("inf"):
                distancia[v] = distancia[u] + 1
                predecessor[v] = u
                fila.append(v)

    return distancia, predecessor
