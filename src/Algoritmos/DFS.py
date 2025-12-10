def dfs(self, s):
        if s not in self.lista_adj:
            raise ValueError(f"Vértice {s} não existe no grafo.")

        visitado = {v: False for v in self.lista_adj}
        pi = {v: None for v in self.lista_adj}
        ini = {v: 0 for v in self.lista_adj}
        fim = {v: 0 for v in self.lista_adj}
        tempo = 0

        stack = [(s, 0)]  # (vértice, índice do próximo vizinho)
        visitado[s] = True
        tempo += 1
        ini[s] = tempo

        while stack:
            u, idx = stack.pop()

            # Se ainda há vizinhos a explorar
            if idx < len(self.lista_adj[u]):
                v, _ = self.lista_adj[u][idx]

                # Coloca de volta com o próximo vizinho
                stack.append((u, idx + 1))

                # Visita v se ainda não visitado
                if not visitado[v]:
                    visitado[v] = True
                    pi[v] = u
                    tempo += 1
                    ini[v] = tempo
                    stack.append((v, 0))
            else:
                # Finalizou u
                tempo += 1
                fim[u] = tempo

        return pi, ini, fim