def dfs(self, origem):
    predecessor = {v: None for v in self.lista_adj}
    tempo_inicio = {v: 0 for v in self.lista_adj}
    tempo_fim = {v: 0 for v in self.lista_adj}

    tempo = [0]  # lista só para permitir alteração dentro da função recursiva

    def visitar(u):
        tempo[0] += 1
        tempo_inicio[u] = tempo[0]

        for v, _ in self.lista_adj[u]:
            if tempo_inicio[v] == 0:
                predecessor[v] = u
                visitar(v)

        tempo[0] += 1
        tempo_fim[u] = tempo[0]

    visitar(origem)
    return predecessor, tempo_inicio, tempo_fim
