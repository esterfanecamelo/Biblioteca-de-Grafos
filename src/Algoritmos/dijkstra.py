import heapq

def dijkstra(self, origem):
    distancia = {v: float("inf") for v in self.lista_adj}
    predecessor = {v: None for v in self.lista_adj}

    distancia[origem] = 0

    heap = [(0, origem)]

    while heap:
        dist_u, u = heapq.heappop(heap)

        if dist_u > distancia[u]:
            continue

        for v, peso in self.lista_adj[u]:
            if distancia[u] + peso < distancia[v]:
                distancia[v] = distancia[u] + peso
                predecessor[v] = u
                heapq.heappush(heap, (distancia[v], v))

    return distancia, predecessor
