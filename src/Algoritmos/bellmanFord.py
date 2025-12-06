def bellman_ford(self, origem):
    distancia = {v: float("inf") for v in self.lista_adj}
    predecessor = {v: None for v in self.lista_adj}

    distancia[origem] = 0

    # relaxa todas as arestas |V|-1 vezes
    for _ in range(len(self.lista_adj) - 1):
        mudou = False

        for u in self.lista_adj:
            for v, peso in self.lista_adj[u]:
                if distancia[u] + peso < distancia[v]:
                    distancia[v] = distancia[u] + peso
                    predecessor[v] = u
                    mudou = True

        if not mudou:
            break

    return distancia, predecessor
